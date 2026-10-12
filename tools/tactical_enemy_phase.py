#!/usr/bin/env python3
"""Read-only Hard/Classic risk for distinct observed attackers in a supplied order."""
import argparse
import copy
import re
from collections import defaultdict

from common import STATS, dump, read_json
from tactical_combat import assess, known_weapon

UNIT_FIELDS = {'stats', 'current_hp', 'weapon', 'weapon_rank', 'skills',
               'weaknesses', 'terrain', 'combat_bonuses', 'remaining_uses',
               'weapon_state', 'alive'}
WEAPON_FIELDS = {'id', 'name', 'weapon_type', 'rank', 'might', 'hit', 'crit',
                 'range', 'damage_type', 'effect', 'brave', 'effectiveness'}


def fail(path, message):
    raise ValueError(path + ': ' + message)


def integer(value, path, minimum=0):
    if type(value) is not int or value < minimum:
        fail(path, 'requires an integer >= ' + str(minimum) + ' (not boolean)')


def string_list(value, path):
    if type(value) is not list or any(type(x) is not str or not x.strip() for x in value):
        fail(path, 'requires a list of nonempty strings; [] confirms none')
    if len(value) != len(set(value)):
        fail(path, 'duplicate values are ambiguous')


def unit_shape(unit, path, side):
    if type(unit) is not dict:
        fail(path, 'requires an observed unit object')
    if set(unit) - UNIT_FIELDS:
        fail(path, 'unsupported fields: ' + ', '.join(sorted(set(unit) - UNIT_FIELDS)))
    for field in UNIT_FIELDS - {'weapon_state', 'alive'}:
        if field not in unit:
            fail(path + '.' + field, 'required observed value missing')
    stats = unit['stats']
    if type(stats) is not dict or set(stats) != set(STATS):
        fail(path + '.stats', 'requires exactly the eight effective displayed stats')
    for field, value in stats.items():
        integer(value, path + '.stats.' + field, 1 if field == 'hp' else 0)
    integer(unit['current_hp'], path + '.current_hp', 1)
    if unit['current_hp'] > stats['hp']:
        fail(path + '.current_hp', 'exceeds observed maximum HP')
    integer(unit['remaining_uses'], path + '.remaining_uses')
    for field in ('skills', 'weaknesses'):
        string_list(unit[field], path + '.' + field)
    for field, allowed in (('terrain', {'def', 'res', 'avoid'}),
                           ('combat_bonuses', {'hit', 'avoid', 'crit', 'crit_avoid', 'attack'})):
        values = unit[field]
        if type(values) is not dict or set(values) - allowed:
            fail(path + '.' + field, 'requires a supported effect object; {} confirms none')
        if any(type(value) is not int for value in values.values()):
            fail(path + '.' + field, 'values must be integers (not boolean)')
    if type(unit['weapon_rank']) is not str or unit['weapon_rank'] not in ('E', 'D', 'C', 'B', 'A'):
        fail(path + '.weapon_rank', 'requires E/D/C/B/A')
    if 'alive' in unit and unit['alive'] is not True:
        fail(path + '.alive', 'only explicitly alive observed units are supported')
    weapon = unit['weapon']
    if type(weapon) is dict and set(weapon) - WEAPON_FIELDS:
        fail(path + '.weapon', 'full objects allow only documented weapon fields')
    try:
        resolved = known_weapon(unit, side)
    except (ValueError, TypeError, KeyError) as exc:
        fail(path + '.weapon', str(exc))
    if resolved is None:
        if unit['remaining_uses'] != 0:
            fail(path + '.remaining_uses', 'unequipped player requires explicit zero uses')
        return
    for field in WEAPON_FIELDS - {'id', 'name'}:
        if field not in resolved:
            fail(path + '.weapon.' + field, 'required exact weapon value missing')
    for field in ('might', 'hit', 'crit'):
        integer(resolved[field], path + '.weapon.' + field)
    if resolved['rank'] not in ('E', 'D', 'C', 'B', 'A'):
        fail(path + '.weapon.rank', 'requires E/D/C/B/A')
    distance = resolved['range']
    if type(distance) is int and distance >= 1:
        return
    if type(distance) is not str or not re.fullmatch(r'[1-9][0-9]*(?:[-~][1-9][0-9]*)?', distance):
        fail(path + '.weapon.range', 'requires a positive integer or positive range string')
    ends = re.split('[-~]', distance)
    if len(ends) == 2 and int(ends[0]) > int(ends[1]):
        fail(path + '.weapon.range', 'range endpoints are reversed')


def validate(payload):
    if type(payload) is not dict:
        fail('sequence', 'requires an object')
    expected = {'difficulty', 'mode', 'observed_inputs_complete', 'stats_basis',
                'support_state', 'partners', 'player_id', 'player', 'enemies'}
    if set(payload) - expected:
        fail('sequence', 'unsupported fields: ' + ', '.join(sorted(set(payload) - expected)))
    for field, value in (('difficulty', 'Hard'), ('mode', 'Classic'),
                         ('stats_basis', 'effective_displayed'), ('support_state', 'none')):
        if payload.get(field) != value:
            fail(field, 'requires explicit ' + value)
    if payload.get('observed_inputs_complete') is not True:
        fail('observed_inputs_complete', 'requires true confirming every supplied observation')
    if type(payload.get('partners')) is not list or payload['partners']:
        fail('partners', 'requires [] confirming neither paired nor adjacent support on any side')
    player_id = payload.get('player_id')
    if type(player_id) is not str or not player_id.strip() or player_id != player_id.strip():
        fail('player_id', 'requires a nonempty observed entity ID without outer whitespace')
    unit_shape(payload.get('player'), 'player', 'defender')
    enemies = payload.get('enemies')
    if type(enemies) is not list or not enemies:
        fail('enemies', 'requires a nonempty list of explicitly ordered distinct attackers')
    seen = {player_id}
    sequence_context = {}
    for index, entry in enumerate(enemies):
        path = 'enemies[' + str(index) + ']'
        if type(entry) is not dict or set(entry) != {'id', 'unit', 'context'}:
            fail(path, 'requires exactly id, unit and context')
        identity = entry['id']
        if type(identity) is not str or not identity.strip() or identity != identity.strip():
            fail(path + '.id', 'requires a nonempty observed entity ID without outer whitespace')
        if identity in seen:
            fail(path + '.id', 'repeated entity or player identity; only distinct attackers supported')
        seen.add(identity)
        unit_shape(entry['unit'], path + '.unit', 'attacker')
        context = entry['context']
        if type(context) is not dict or set(context) - {'distance', 'turn', 'outdoors'}:
            fail(path + '.context', 'requires a supported context object')
        integer(context.get('distance'), path + '.context.distance', 1)
        if 'turn' in context:
            integer(context['turn'], path + '.context.turn', 1)
        if 'outdoors' in context and type(context['outdoors']) is not bool:
            fail(path + '.context.outdoors', 'requires a boolean')
        for field in ('turn', 'outdoors'):
            if field in context:
                if field in sequence_context and context[field] != sequence_context[field]:
                    fail(path + '.context.' + field, 'conflicts with this fixed sequence context')
                sequence_context[field] = context[field]


def duel(payload, entry, player, index):
    battle = {key: payload[key] for key in ('difficulty', 'mode', 'observed_inputs_complete',
                                          'stats_basis', 'support_state', 'partners')}
    battle.update(attacker=entry['unit'], defender=player, context=entry['context'])
    result = assess(battle)
    if result.get('outcome') is None:
        reason = result.get('reason', str(result.get('missing', 'unsupported outcome')))
        fail('enemies[' + str(index) + '] (attacker=unit, defender=player)', reason)
    return result


def evaluate(payload):
    """Return UNKNOWN without numbers if any input or reachable duel is unsupported."""
    try:
        validate(payload)
        player = payload['player']
        # Preflight every attacker, even those after a certain player death.
        preflight = [duel(payload, entry, player, index)
                     for index, entry in enumerate(payload['enemies'])]
        maximum_uses = sum(result['forecast']['defender']['scheduled_hits'] for result in preflight)
        if player['remaining_uses'] < maximum_uses:
            fail('player.remaining_uses', 'possible cumulative retaliation breakage; requires at least '
                 + str(maximum_uses) + ' uses for conservative scheduled maximum')
        states = {player['current_hp']: 1.0}
        steps = []
        reserved = 0
        for index, entry in enumerate(payload['enemies']):
            next_states = defaultdict(float)
            enemy_death = 0.0
            for hp, probability in states.items():
                if hp == 0:
                    next_states[0] += probability
                    continue
                observed = copy.deepcopy(player)
                observed.update(current_hp=hp, remaining_uses=player['remaining_uses'] - reserved)
                result = duel(payload, entry, observed, index)
                for state in result['outcome']['states']:
                    weight = probability * state['probability']
                    if weight <= 0:
                        continue
                    next_states[state['defender_hp']] += weight
                    if state['attacker_hp'] == 0:
                        enemy_death += weight
            states = dict(next_states)
            reserved += preflight[index]['forecast']['defender']['scheduled_hits']
            steps.append({'enemy_id': entry['id'], 'player_death_probability': states.get(0, 0.0),
                          'enemy_death_probability': enemy_death,
                          'minimum_possible_player_hp': min(states),
                          'expected_player_hp': sum(hp * p for hp, p in states.items())})
        death = states.get(0, 0.0)
        outcome = {'final_hp_distribution': [{'hp': hp, 'probability': probability}
                                            for hp, probability in sorted(states.items())],
                   'player_death_probability': death, 'minimum_possible_player_hp': min(states),
                   'expected_player_hp': sum(hp * p for hp, p in states.items()),
                   'maximum_scheduled_retaliation_uses': maximum_uses, 'steps': steps}
        status = ('LETHAL' if set(states) == {0} else 'POTENTIALLY_LETHAL' if death > 0
                  else 'NO_MODELED_PLAYER_DEATH_IN_THIS_SEQUENCE')
        return {'status': status, 'outcome': outcome, 'conditional_on_observed_inputs': True,
                'safe_to_claim_survival': False, 'safe_to_claim_map_survival': False,
                'warning': 'Only this supplied sequence of distinct observed attackers. Independent uniform '
                           'RNG model; no AI order/targets/paths, unseen enemies, reinforcements, '
                           'between-duel events, healing or weapon swaps. Zero modeled player death '
                           'is conditional, never whole-map safety. Enemy death is reported per step.'}
    except (ValueError, KeyError, TypeError) as exc:
        return {'status': 'UNKNOWN', 'reason': str(exc), 'outcome': None,
                'safe_to_claim_survival': False, 'safe_to_claim_map_survival': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Observed sequence JSON file (read only)')
    args = parser.parse_args()
    try:
        payload = read_json(args.input)
    except (ValueError, OSError) as exc:
        parser.exit(2, 'Cannot read sequence JSON: ' + str(exc) + '\n')
    dump(evaluate(payload))


if __name__ == '__main__':
    main()

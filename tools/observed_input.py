#!/usr/bin/env python3
"""Collect a plain observed duel offline; never read or update a player run."""
import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path

from common import ROOT, STATS, lookup
from tactical_combat import assess

TERRAIN = ('def', 'res', 'avoid')
BONUSES = ('hit', 'avoid', 'crit', 'crit_avoid', 'attack')
WEAPON_NUMBERS = ('might', 'hit', 'crit')
WEAPON_FIELDS = {'id', 'name', 'weapon_type', 'damage_type', 'might', 'hit',
                 'crit', 'range', 'rank', 'effect', 'brave', 'effectiveness'}
UNIT_FIELDS = {'stats', 'current_hp', 'weapon', 'weapon_state', 'weapon_rank',
               'skills', 'weaknesses', 'terrain', 'combat_bonuses',
               'remaining_uses', 'forge', 'alive', 'id', 'name'}
TOP_FIELDS = {'difficulty', 'mode', 'stats_basis', 'observed_inputs_complete',
              'support_state', 'partners', 'attacker', 'defender', 'context'}


class Cancelled(Exception):
    """No payload is emitted on cancellation or EOF."""


def integer(text):
    if not re.fullmatch(r'[+-]?[0-9]+', text):
        raise ValueError('Enter an integer, not a boolean or decimal.')
    return int(text)


def boolean(text):
    if text not in ('yes', 'no'):
        raise ValueError('Enter yes or no.')
    return text == 'yes'


def choice(*values):
    def parse(text):
        if text not in values:
            raise ValueError('Choose ' + ', '.join(values) + '.')
        return text
    return parse


def strings(text):
    if text == 'none':
        return []
    parts = [part.strip() for part in text.split(',')]
    if any(not part or part == '?' or part == 'none' for part in parts):
        raise ValueError('Enter comma-separated IDs, none, or ? for unknown.')
    return parts


def numbers(keys, empty=False):
    def parse(text):
        if empty and text == 'none':
            return {}
        parts = text.split()
        if len(parts) != len(keys):
            raise ValueError('Enter ' + str(len(keys)) + ' values in the shown order.')
        return dict(zip(keys, [None if x == '?' else integer(x) for x in parts]))
    return parse


class Collector:
    def __init__(self, source, diagnostic):
        self.source = source
        self.diagnostic = diagnostic

    def ask(self, label, parse=str, old=None, present=False):
        while True:
            suffix = ('; keep=' + json.dumps(old, ensure_ascii=False)) if present else ''
            print(label + suffix + ' [blank/? unknown; cancel stops]: ',
                  file=self.diagnostic, end='', flush=True)
            line = self.source.readline()
            if not line:
                raise Cancelled('EOF')
            text = line.strip()
            if text == 'cancel':
                raise Cancelled('cancelled')
            if text in ('', '?'):
                return None
            if text == 'keep':
                if present:
                    return copy.deepcopy(old)
                print('There is no previous value to keep.', file=self.diagnostic)
                continue
            try:
                return parse(text)
            except ValueError as error:
                print(str(error), file=self.diagnostic)

    def field(self, obj, key, label, parse=str, previous=None):
        previous = previous or {}
        obj[key] = self.ask(label, parse, previous.get(key), key in previous)

    def weapon(self, previous):
        old = previous.get('weapon')
        selection = self.ask('Weapon: custom, catalog EXACT_NAME, unequipped (defender only)',
                             old=old, present='weapon' in previous)
        if selection is None:
            return None, None
        if isinstance(selection, dict):
            return selection, 'equipped'
        if selection == 'unequipped':
            return None, 'unequipped'
        if selection != 'custom':
            name = selection[8:] if selection.startswith('catalog ') else selection
            try:
                catalog = lookup('weapons', name)
            except ValueError:
                raise ValueError('Unknown catalog name; no values were guessed. Retry with custom or a known exact name.')
            # Only resolved battle values are needed; no automatic forge arithmetic.
            weapon = {key: copy.deepcopy(catalog[key]) for key in WEAPON_FIELDS if key in catalog}
            print('Catalog battle values: ' + json.dumps(weapon, sort_keys=True, ensure_ascii=False),
                  file=self.diagnostic)
            confirmed = self.ask('Confirm these exact unforged values match the observed weapon: yes/no', boolean)
            if confirmed is not True:
                return None, None
            return weapon, 'equipped'
        weapon = {}
        self.field(weapon, 'weapon_type', 'Weapon type (sword/lance/axe/bow/tome/stone/claw/breath)')
        self.field(weapon, 'damage_type', 'Damage type (physical/magical)')
        self.field(weapon, 'rank', 'Actual weapon required rank (E/D/C/B/A), separate from unit proficiency',
                   choice('E', 'D', 'C', 'B', 'A'))
        values = self.ask('Actual weapon might hit crit (including forge)', numbers(WEAPON_NUMBERS))
        weapon.update(values or dict.fromkeys(WEAPON_NUMBERS))
        self.field(weapon, 'range', 'Actual weapon range, e.g. 1 or 1-2')
        self.field(weapon, 'effect', 'Exact weapon effect; none confirms no special effect',
                   lambda value: '–' if value == 'none' else value)
        self.field(weapon, 'brave', 'Two consecutive attacks: yes/no', boolean)
        self.field(weapon, 'effectiveness', 'Weapon effectiveness IDs, comma-separated; none confirms empty', strings)
        return weapon, 'equipped'

    def collect(self, draft=None):
        draft = draft or {}
        payload = {}
        print('Observed duel only. Enter actual observations; no inferred defaults or bonus conversion.\n'
              'For an edited draft, type keep deliberately for each value; final confirmation is renewed.',
              file=self.diagnostic)
        for key, label, parse in (
            ('difficulty', 'Difficulty (Normal/Hard/Lunatic/Lunatic+)', choice('Normal', 'Hard', 'Lunatic', 'Lunatic+')),
            ('mode', 'Mode (Classic/Casual)', choice('Classic', 'Casual')),
            ('stats_basis', 'Stats basis (effective_displayed/raw_permanent); include bonuses once',
             choice('effective_displayed', 'raw_permanent')),
            ('support_state', 'Support on either side (none/adjacent/paired); none confirms both absent',
             choice('none', 'adjacent', 'paired')),
            ('partners', 'Observed partner IDs, comma-separated; none confirms empty', strings)):
            self.field(payload, key, label, parse, draft)
        for side in ('attacker', 'defender'):
            previous = draft.get(side) or {}
            unit = {}
            self.field(unit, 'stats', side + ' stats ' + ' '.join(STATS), numbers(STATS), previous)
            self.field(unit, 'current_hp', side + ' actual current HP (never defaults to max)', integer, previous)
            while True:
                try:
                    weapon, state = self.weapon(previous)
                    if side == 'attacker' and state == 'unequipped':
                        raise ValueError('Only a defender may explicitly be unequipped.')
                    unit.update(weapon=weapon, weapon_state=state)
                    if 'weapon_state' in previous:
                        self.field(unit, 'weapon_state', side + ' supplied weapon_state (equipped/unequipped)',
                                   choice('equipped', 'unequipped'), previous)
                    break
                except ValueError as error:
                    print(str(error), file=self.diagnostic)
            for key, label, parse in (
                ('weapon_rank', 'Observed weapon rank (E/D/C/B/A)', choice('E', 'D', 'C', 'B', 'A')),
                ('skills', 'All equipped skill IDs, comma-separated; none confirms empty', strings),
                ('weaknesses', 'All innate weakness IDs, comma-separated; none confirms empty', strings),
                ('terrain', 'Terrain ' + ' '.join(TERRAIN) + '; none confirms no bonuses', numbers(TERRAIN, True)),
                ('combat_bonuses', 'Combat bonuses ' + ' '.join(BONUSES) + '; none confirms no bonuses', numbers(BONUSES, True)),
                ('remaining_uses', 'Observed remaining weapon uses (explicit 0 if unequipped)', integer)):
                self.field(unit, key, side + ' ' + label, parse, previous)
            for key in ('forge', 'alive', 'id', 'name'):
                if key in previous:
                    self.field(unit, key, side + ' supplied ' + key + ' (keep preserves it)',
                               boolean if key == 'alive' else str, previous)
            payload[side] = unit
        context = {}
        old_context = draft.get('context') or {}
        self.field(context, 'distance', 'Actual attack distance', integer, old_context)
        skills = (payload['attacker']['skills'] or []) + (payload['defender']['skills'] or [])
        for key, needed, label, parse in (
            ('outdoors', {'indoor_fighter', 'outdoor_fighter'}, 'Combat outdoors: yes/no', boolean),
            ('turn', {'lucky_seven', 'even_rhythm', 'odd_rhythm'}, 'Actual turn', integer)):
            if key in old_context or set(skills) & needed:
                self.field(context, key, label, parse, old_context)
        payload['context'] = context
        confirmation = self.ask('Confirm ALL observations current and complete, including effects/support: yes/no', boolean)
        payload['observed_inputs_complete'] = confirmation is True and observations_known(payload)
        if confirmation is True and not payload['observed_inputs_complete']:
            print('Incomplete/invalid observations remain; completeness is false.', file=self.diagnostic)
        return payload


def observations_known(payload):
    """Presence is separate from supported mechanics; assess owns calculation."""
    if any(payload.get(key) is None for key in ('difficulty', 'mode', 'stats_basis', 'support_state', 'partners')):
        return False
    for key, allowed in (('difficulty', ('Normal', 'Hard', 'Lunatic', 'Lunatic+')),
                         ('mode', ('Classic', 'Casual')),
                         ('stats_basis', ('effective_displayed', 'raw_permanent')),
                         ('support_state', ('none', 'adjacent', 'paired'))):
        if payload[key] not in allowed:
            return False
    if not isinstance(payload['partners'], list) or any(type(value) is not str or not value.strip()
            or value.strip().lower() in ('?', 'unknown') for value in payload['partners']):
        return False
    if payload['support_state'] == 'none' and payload['partners']:
        return False
    if payload['support_state'] in ('paired', 'adjacent') and not payload['partners']:
        return False
    context = payload['context']
    if type(context.get('distance')) is not int or context['distance'] < 1:
        return False
    if 'outdoors' in context and type(context['outdoors']) is not bool:
        return False
    if 'turn' in context and (type(context['turn']) is not int or context['turn'] < 1):
        return False
    for side in ('attacker', 'defender'):
        unit = payload[side]
        stats = unit.get('stats')
        if not isinstance(stats, dict) or any(type(stats.get(key)) is not int or stats[key] < 0 for key in STATS):
            return False
        if type(unit['current_hp']) is not int or not 1 <= unit['current_hp'] <= stats['hp']:
            return False
        for field in ('skills', 'weaknesses'):
            if not isinstance(unit[field], list) or any(type(value) is not str or not value.strip() for value in unit[field]):
                return False
        if len(unit['skills']) > 5:
            return False
        if any(value.strip().lower() in ('?', 'unknown') for field in ('skills', 'weaknesses') for value in unit[field]):
            return False
        for field in ('terrain', 'combat_bonuses'):
            if not isinstance(unit[field], dict) or any(type(value) is not int for value in unit[field].values()):
                return False
        if unit['weapon_rank'] not in ('E', 'D', 'C', 'B', 'A'):
            return False
        if type(unit['remaining_uses']) is not int or unit['remaining_uses'] < 0:
            return False
        weapon = unit['weapon']
        unequipped = side == 'defender' and unit['weapon_state'] == 'unequipped' and weapon is None
        if unequipped and unit['remaining_uses'] != 0:
            return False
        if not unequipped:
            if unit['weapon_state'] != 'equipped':
                return False
            if not isinstance(weapon, dict):
                return False
            if any(type(weapon.get(key)) is not int or weapon[key] < 0 for key in WEAPON_NUMBERS):
                return False
            if any(type(weapon.get(key)) is not str or not weapon[key].strip()
                   for key in ('weapon_type', 'damage_type', 'effect')):
                return False
            distance = weapon.get('range')
            if type(distance) is int:
                if distance < 1:
                    return False
            elif type(distance) is str and re.fullmatch(r'[1-9][0-9]*(?:[-~][1-9][0-9]*)?', distance):
                ends = re.split('[-~]', distance)
                if len(ends) == 2 and int(ends[0]) > int(ends[1]):
                    return False
            else:
                return False
            if type(weapon.get('brave')) is not bool or not isinstance(weapon.get('effectiveness'), list):
                return False
            if weapon.get('rank') not in ('E', 'D', 'C', 'B', 'A'):
                return False
            if weapon['weapon_type'] not in ('sword', 'lance', 'axe', 'bow', 'tome', 'stone', 'claw', 'breath'):
                return False
            if weapon['damage_type'] not in ('physical', 'magical'):
                return False
            if weapon['effect'].strip().lower() in ('?', 'unknown'):
                return False
            if weapon['brave'] != (weapon['effect'] == '2 consecutive attacks'):
                return False
            if any(type(value) is not str or not value.strip() for value in weapon['effectiveness']):
                return False
            if set(weapon['effectiveness']) - {'beast', 'dragon', 'armour', 'flying'}:
                return False
        skills = set(unit['skills'])
        if skills & {'indoor_fighter', 'outdoor_fighter'} and type(context.get('outdoors')) is not bool:
            return False
        if skills & {'lucky_seven', 'even_rhythm', 'odd_rhythm'}:
            if type(context.get('turn')) is not int or context['turn'] < 1:
                return False
        # A supplied unknown effect marker must not become complete through keep.
        if any(value is None for key, value in unit.items() if key not in ('weapon',)):
            return False
    return True


def object_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('Duplicate JSON object key: ' + key)
        obj[key] = value
    return obj


def draft_shape(payload):
    def fields(value, allowed, label):
        if value is None:
            return
        if not isinstance(value, dict) or set(value) - allowed:
            raise ValueError('Incompatible ' + label + ' shape/extra fields; nothing was dropped.')
    fields(payload, TOP_FIELDS, 'duel')
    if not isinstance(payload, dict) or not {'attacker', 'defender'} <= payload.keys():
        raise ValueError('An existing plain duel draft is required; runs are refused.')
    fields(payload.get('context'), {'distance', 'outdoors', 'turn'}, 'context')
    for side in ('attacker', 'defender'):
        unit = payload[side]
        fields(unit, UNIT_FIELDS, side)
        if not isinstance(unit, dict):
            raise ValueError('Each duel side must be an object.')
        for key, allowed in (('stats', set(STATS)), ('terrain', set(TERRAIN)), ('combat_bonuses', set(BONUSES))):
            fields(unit.get(key), allowed, side + '.' + key)
        weapon = unit.get('weapon')
        if isinstance(weapon, dict):
            fields(weapon, WEAPON_FIELDS, side + '.weapon')
        elif weapon is not None and not isinstance(weapon, str):
            raise ValueError('Incompatible weapon shape; nothing was dropped.')
        for key in ('skills', 'weaknesses'):
            value = unit.get(key)
            if value is not None and (not isinstance(value, list) or any(type(x) is not str for x in value)):
                raise ValueError('Incompatible ' + side + '.' + key + ' shape.')
    if payload.get('partners') is not None and not isinstance(payload['partners'], list):
        raise ValueError('Incompatible partners shape.')


def load_draft(path):
    selected = Path(path)
    resolved = selected.resolve(strict=True)
    if selected.name == 'current_run.json' or resolved.name == 'current_run.json':
        raise ValueError('Player run files cannot be selected for editing.')
    # Hard links to the standard run location are refused without opening it.
    run = ROOT / 'state' / 'current_run.json'
    if run.exists() and os.path.samefile(resolved, run):
        raise ValueError('Player run files cannot be selected for editing.')
    payload = json.loads(resolved.read_text(encoding='utf-8'), object_pairs_hook=object_pairs,
                         parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Invalid JSON constant: ' + value)))
    draft_shape(payload)
    return payload


def create_output(destination, encoded):
    """Create only beneath this checkout, walking directories without symlinks."""
    path = Path(destination)
    if '..' in path.parts:
        raise ValueError('Output traversal is refused.')
    if not path.is_absolute():
        path = Path.cwd() / path
    base = ROOT / 'state' / 'observations'
    try:
        parts = path.relative_to(base).parts
    except ValueError:
        raise ValueError('Output must be inside this checkout state/observations.') from None
    if not parts or path.suffix != '.json' or path.name == 'current_run.json':
        raise ValueError('Output must be a new .json observation, never current_run.json.')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(ROOT, flags)
    try:
        for part in ('state', 'observations') + parts[:-1]:
            try:
                child = os.open(part, flags, dir_fd=fd)
            except FileNotFoundError:
                os.mkdir(part, mode=0o700, dir_fd=fd)
                child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        output_fd = os.open(parts[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                            0o600, dir_fd=fd)
        try:
            with os.fdopen(output_fd, 'w', encoding='utf-8') as output:
                output.write(encoded)
        except BaseException:
            os.unlink(parts[-1], dir_fd=fd)
            raise
    finally:
        os.close(fd)


def diagnostic(payload, stream):
    result = assess(payload)
    if result['status'] == 'UNKNOWN':
        detail = result.get('reason') or '; '.join(result.get('missing', []))
        print('UNKNOWN: ' + detail, file=stream)
    else:
        print(result['status'] + ': attacker death probability=' + str(result['attacker_death_probability'])
              + ', defender death probability=' + str(result['defender_death_probability']), file=stream)
    print('Supplied duel only; no whole-map survival guarantee.', file=stream)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--edit', help='Explicit prior plain duel draft; never a run')
    parser.add_argument('--output', help='CREATE a new .json in this checkout state/observations')
    args = parser.parse_args(argv)
    try:
        draft = load_draft(args.edit) if args.edit else None
        payload = Collector(sys.stdin, sys.stderr).collect(draft)
        encoded = json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
        if args.output:
            create_output(args.output, encoded)
        diagnostic(payload, sys.stderr)
        sys.stdout.write(encoded)
        return 0
    except (Cancelled, KeyboardInterrupt):
        print('Cancelled; no observation payload or file created.', file=sys.stderr)
        return 1
    except (ValueError, OSError, TypeError) as error:
        # Avoid printing private selected paths in public diagnostics.
        message = str(error) if not isinstance(error, OSError) else error.strerror
        print('Refused: ' + message, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

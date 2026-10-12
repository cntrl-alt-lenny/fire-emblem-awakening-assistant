"""Brain's synthetic numerical control, defined before helper delivery."""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
from tactical_combat import assess
from tactical_enemy_phase import evaluate


def fixtures():
    unit = {'stats': dict(zip(('hp', 'str', 'mag', 'skl', 'spd', 'lck', 'def', 'res'),
                              (20, 0, 0, 0, 0, 0, 0, 0))),
            'current_hp': 20,
            'weapon': {'weapon_type': 'tome', 'rank': 'E', 'might': 6,
                       'hit': 50, 'crit': 0, 'range': '1', 'damage_type': 'magical',
                       'effect': '–', 'brave': False, 'effectiveness': []},
            'weapon_rank': 'E', 'skills': [], 'weaknesses': [],
            'terrain': {}, 'combat_bonuses': {}, 'remaining_uses': 10}
    player = copy.deepcopy(unit)
    player.update(weapon=None, weapon_state='unequipped', remaining_uses=0, current_hp=10)
    player['stats']['hp'] = 10
    header = {'difficulty': 'Hard', 'mode': 'Classic', 'observed_inputs_complete': True,
              'stats_basis': 'effective_displayed', 'support_state': 'none', 'partners': []}
    duel = dict(header, attacker=unit, defender=player, context={'distance': 1})
    sequence = dict(header, player_id='observed_player', player=player,
                    enemies=[{'id': identity, 'unit': copy.deepcopy(unit),
                              'context': {'distance': 1}}
                             for identity in ('enemy_one', 'enemy_two')])
    return duel, sequence


def main():
    duel, sequence = fixtures()
    before = copy.deepcopy((duel, sequence))
    # Independent enumeration; no calculator hit helper or rounding helper.
    hit = sum((a + b) // 2 < 50 for a in range(100) for b in range(100)) / 10000
    expected = {10: (1 - hit) ** 2, 4: 2 * hit * (1 - hit), 0: hit * hit}
    assert hit == 0.505
    result = evaluate(sequence)
    assert {row['hp']: row['probability']
            for row in result['outcome']['final_hp_distribution']} == expected
    assert assess(duel)['worst_defender_hp'] == 4
    for field in ('skills', 'weaknesses', 'combat_bonuses', 'current_hp'):
        incomplete = copy.deepcopy(duel)
        incomplete['attacker'][field] = None
        assert assess(incomplete)['outcome'] is None
    unsupported = copy.deepcopy(sequence)
    unsupported['enemies'][-1]['unit']['skills'] = ['counter']
    assert evaluate(unsupported)['outcome'] is None
    assert (duel, sequence) == before
    print(json.dumps({'hit_probability': hit, 'expected_hp_distribution': expected,
                      'complete_gate_match': True, 'unknown_and_effect_refusal': True,
                      'synthetic_inputs_unchanged': True}, sort_keys=True))
    print('Exit 0')


if __name__ == '__main__':
    main()

"""Synthetic sequence boundary and independently derived composition controls."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from tactical_enemy_phase import evaluate

ROOT = Path(__file__).resolve().parents[1]


def unit(hp=20, damage=6, hit=50):
    return {'stats': {'hp': hp, 'str': 0, 'mag': 0, 'skl': 0, 'spd': 0,
                      'lck': 0, 'def': 0, 'res': 0}, 'current_hp': hp,
            'weapon': {'weapon_type': 'tome', 'rank': 'E', 'might': damage,
                       'hit': hit, 'crit': 0, 'range': '1', 'damage_type': 'magical',
                       'effect': '–', 'brave': False, 'effectiveness': []},
            'weapon_rank': 'E', 'skills': [], 'weaknesses': [], 'terrain': {},
            'combat_bonuses': {}, 'remaining_uses': 10}


def sequence():
    player = unit(hp=10)
    player.update(weapon=None, weapon_state='unequipped', remaining_uses=0)
    return {'difficulty': 'Hard', 'mode': 'Classic', 'observed_inputs_complete': True,
            'stats_basis': 'effective_displayed', 'support_state': 'none', 'partners': [],
            'player_id': 'player', 'player': player,
            'enemies': [{'id': 'enemy_' + str(i), 'unit': unit(), 'context': {'distance': 1}}
                        for i in range(2)]}


class ObservedSequenceTests(unittest.TestCase):
    def unknown(self, payload, diagnostic=None):
        before = copy.deepcopy(payload)
        result = evaluate(payload)
        self.assertEqual(payload, before)
        self.assertEqual(result['status'], 'UNKNOWN', result)
        self.assertIsNone(result['outcome'])
        self.assertFalse(result['safe_to_claim_map_survival'])
        if diagnostic:
            self.assertIn(diagnostic, result['reason'])
        return result

    def test_independent_two_rn_composition(self):
        # Enumerate two uniform 0..99 draws independently of calculator helpers.
        hit = sum((a + b) // 2 < 50 for a in range(100) for b in range(100)) / 10000
        p = sequence()
        before = copy.deepcopy(p)
        result = evaluate(p)
        self.assertEqual(p, before)
        self.assertEqual(result['status'], 'POTENTIALLY_LETHAL')
        distribution = {s['hp']: s['probability'] for s in result['outcome']['final_hp_distribution']}
        expected = {10: (1 - hit) ** 2, 4: 2 * hit * (1 - hit), 0: hit ** 2}
        self.assertEqual(set(distribution), set(expected))
        for hp, probability in expected.items():
            self.assertAlmostEqual(distribution[hp], probability)
        self.assertAlmostEqual(sum(distribution.values()), 1)
        self.assertFalse(result['safe_to_claim_map_survival'])

    def test_dead_player_absorption_and_full_tail_preflight(self):
        p = sequence()
        for entry in p['enemies']:
            entry['unit']['weapon'].update(might=10, hit=100)
        result = evaluate(p)
        self.assertEqual(result['status'], 'LETHAL')
        self.assertEqual(result['outcome']['final_hp_distribution'], [{'hp': 0, 'probability': 1.0}])
        self.assertEqual(result['outcome']['steps'][1]['enemy_death_probability'], 0)
        p['enemies'][1]['unit']['skills'] = ['counter']
        self.unknown(p, 'enemies[1]')
        p['enemies'][1]['unit']['skills'] = 'counter'
        self.unknown(p, 'enemies[1].unit.skills')
        p['enemies'][1]['unit']['skills'] = []
        del p['enemies'][1]['unit']['current_hp']
        self.unknown(p, 'enemies[1].unit.current_hp')

    def test_hp_dependent_vantage_and_early_kill(self):
        p = sequence()
        p['player'] = unit(hp=20, damage=10, hit=100)
        p['player'].update(current_hp=12, skills=['vantage'], remaining_uses=2)
        for entry in p['enemies']:
            entry['unit'] = unit(hp=10, damage=3, hit=100)
        result = evaluate(p)
        self.assertEqual(result['status'], 'NO_MODELED_PLAYER_DEATH_IN_THIS_SEQUENCE')
        # First attack takes 12 -> 9; second attacker dies to newly active Vantage.
        self.assertEqual(result['outcome']['final_hp_distribution'], [{'hp': 9, 'probability': 1.0}])
        self.assertEqual([s['enemy_death_probability'] for s in result['outcome']['steps']], [1, 1])
        self.assertEqual(result['outcome']['maximum_scheduled_retaliation_uses'], 2)
        self.assertFalse(result['safe_to_claim_survival'])
        p['player']['remaining_uses'] = 1
        self.unknown(p, 'cumulative retaliation breakage')

    def test_possible_breakage_even_with_guaranteed_early_kills(self):
        p = sequence()
        p['player'] = unit(hp=10, damage=20, hit=100)
        p['player'].update(skills=['vantage_plus'], remaining_uses=2)
        for entry in p['enemies']:
            entry['unit'] = unit(hp=10, damage=6, hit=100)
        result = evaluate(p)
        self.assertEqual(result['outcome']['final_hp_distribution'], [{'hp': 10, 'probability': 1.0}])
        p['player']['remaining_uses'] = 1
        self.unknown(p, 'requires at least 2')

    def test_dynamic_branch_refusal_invalidates_all_numbers(self):
        p = sequence()
        for entry in p['enemies']:
            entry['unit']['weapon']['hit'] = 100
        p['player']['stats']['lck'] = 100
        p['enemies'][0]['unit']['skills'] = ['hawkeye']
        p['enemies'][1]['unit']['skills'] = ['sol', 'hawkeye']
        p['enemies'][1]['unit']['stats']['skl'] = 100
        # Preflight Sol deals 6 <= initial 10; after first hit it overkills HP 4.
        self.unknown(p, 'Sol overkill')

    def test_complete_collection_hp_and_use_types(self):
        bad = {'skills': ['vantage', {}, None, [None], [[]], ['vantage', 'vantage']],
               'weaknesses': ['dragon', {}, None, [None], [[]]],
               'stats': [[], None, 'stats'], 'terrain': [[], None, 'terrain'],
               'combat_bonuses': [[], None, 'bonuses'],
               'current_hp': [True, False, 5.5, '10', 0, -1, None],
               'remaining_uses': [True, 1.5, '10', -1, None],
               'weapon_rank': ['ED', 'DC', '', [], None]}
        for side in ('player', 'enemy'):
            for field, values in bad.items():
                for value in values:
                    with self.subTest(side=side, field=field, value=value):
                        p = sequence()
                        target = p['player'] if side == 'player' else p['enemies'][1]['unit']
                        target[field] = value
                        self.unknown(p, field)
            for field in ('stats', 'current_hp', 'remaining_uses', 'weapon', 'weapon_rank',
                          'skills', 'weaknesses', 'terrain', 'combat_bonuses'):
                p = sequence()
                target = p['player'] if side == 'player' else p['enemies'][1]['unit']
                del target[field]
                self.unknown(p, field)

    def test_weapon_and_context_shapes(self):
        for field, values in {'range': [None, [], {}, True, 0, '0', '3-1'],
                              'rank': [None, [], {}, 'ED'], 'damage_type': [[], None],
                              'weapon_type': [[], None], 'might': [True, 1.5],
                              'effectiveness': ['dragon', None, [None]]}.items():
            for value in values:
                p = sequence(); p['enemies'][1]['unit']['weapon'][field] = value
                self.unknown(p, 'enemies[1]')
        for field, values in {'distance': [True, None, 0, 1.5],
                              'turn': [True, None, 0], 'outdoors': [1, None, 'false']}.items():
            for value in values:
                p = sequence(); p['enemies'][1]['context'][field] = value
                self.unknown(p, 'context.' + field)
        p = sequence(); p['enemies'][1]['context']['weather'] = 'unknown'
        self.unknown(p, 'context')

    def test_sequence_identity_and_completeness(self):
        for field, values in {'difficulty': ['Normal', None], 'mode': ['Casual', None],
                              'observed_inputs_complete': [1, None, False],
                              'stats_basis': ['raw', None], 'support_state': ['paired', None],
                              'partners': [None, {}, ['support']],
                              'player_id': [None, True, '', ' player '],
                              'enemies': [[], None, {}]}.items():
            for value in values:
                p = sequence(); p[field] = value
                self.unknown(p, field)
        for identity in ('enemy_0', 'player', '', None, True, ' enemy_1 '):
            p = sequence(); p['enemies'][1]['id'] = identity
            self.unknown(p, 'enemies[1].id')
        self.unknown(None, 'sequence')
        p = sequence(); p['player']['status_effects'] = ['unknown']
        self.unknown(p, 'unsupported fields')

    def test_inherited_effect_refusals_and_unknown_tail(self):
        for skills in (['counter'], ['dragonskin'], ['aether'], ['pavise', 'aegis'], ['luna', 'sol']):
            p = sequence(); p['enemies'][1]['unit']['skills'] = skills
            p['enemies'][1]['unit']['stats']['skl'] = 10
            self.unknown(p, 'enemies[1]')
        p = sequence(); p['enemies'][1]['unit']['weapon']['effect'] = 'Drains HP'
        self.unknown(p, 'enemies[1]')
        p = sequence(); p['enemies'][1]['unit']['remaining_uses'] = 0
        self.unknown(p, 'break')
        p = sequence(); p['enemies'][1]['unit']['skills'] = ['outdoor_fighter']
        self.unknown(p, 'context.outdoors')

    def test_example_and_cli_protocol_and_preservation(self):
        example = json.loads((ROOT / 'examples/observed_enemy_sequence.json').read_text())
        self.assertEqual(evaluate(example)['outcome']['minimum_possible_player_hp'], 10)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'sequence.json'
            for p, status in ((example, 'NO_MODELED_PLAYER_DEATH_IN_THIS_SEQUENCE'),
                               (sequence(), 'POTENTIALLY_LETHAL'), ({}, 'UNKNOWN')):
                original = json.dumps(p); path.write_text(original)
                result = subprocess.run([sys.executable, str(ROOT / 'tools/tactical_enemy_phase.py'),
                                         str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], status)
                self.assertEqual(path.read_text(), original)
            path.write_text('{')
            result = subprocess.run([sys.executable, str(ROOT / 'tools/tactical_enemy_phase.py'),
                                     str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Cannot read sequence JSON', result.stderr)
            self.assertEqual(path.read_text(), '{')


if __name__ == '__main__':
    unittest.main()

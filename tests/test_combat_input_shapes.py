"""Observed collection/HP boundary regressions; synthetic duels only."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from combat_calculator import calculate
from tactical_combat import assess
from test_hard import battle

SIDES = ('attacker', 'defender')


class CombatInputShapeTests(unittest.TestCase):
    def assert_unknown(self, payload, side, field):
        before = copy.deepcopy(payload)
        result = assess(payload)
        self.assertEqual(payload, before)
        self.assertEqual(result['status'], 'UNKNOWN')
        self.assertIsNone(result['outcome'])
        self.assertFalse(result['safe_to_claim_survival'])
        self.assertIn(side + ':' + field, result.get('reason', str(result.get('missing', []))))
        return result

    def test_missing_and_null_fields_both_sides(self):
        for side in SIDES:
            for field in ('skills', 'weaknesses', 'current_hp'):
                for missing in (True, False):
                    with self.subTest(side=side, field=field, missing=missing):
                        payload = battle()
                        if missing:
                            del payload[side][field]
                        else:
                            payload[side][field] = None
                        self.assert_unknown(payload, side, field)

    def test_collection_types_both_sides(self):
        for side in SIDES:
            for field in ('skills', 'weaknesses'):
                for value in ('', 'veteran', {}, {'veteran': True}, (), ('veteran',), set(), {'veteran'}, True, False, 0, 1.5):
                    with self.subTest(side=side, field=field, value=value):
                        payload = battle()
                        payload[side][field] = value
                        self.assert_unknown(payload, side, field)

    def test_collection_element_types_both_sides(self):
        for side in SIDES:
            for field in ('skills', 'weaknesses'):
                good = 'veteran' if field == 'skills' else 'flying'
                for value in (None, True, False, 0, 1, 1.5, [], {}, [good], {good: True}, (good,), {good}):
                    for elements in ([value], [good, value]):
                        with self.subTest(side=side, field=field, elements=elements):
                            payload = battle()
                            payload[side][field] = elements
                            self.assert_unknown(payload, side, field)

    def test_unknown_membership_both_sides(self):
        for side in SIDES:
            for field in ('skills', 'weaknesses'):
                for value in ('', ' ', 'UNKNOWN', 'not_an_id', 'Flying'):
                    with self.subTest(side=side, field=field, value=value):
                        payload = battle()
                        payload[side][field] = [value]
                        self.assert_unknown(payload, side, field)
            payload = battle()
            payload[side]['skills'] = ['veteran'] * 6
            self.assert_unknown(payload, side, 'skills')

    def test_hp_types_and_bounds_both_sides(self):
        for side in SIDES:
            for value in (True, False, 1.0, 1.5, 40.0, '1', '', [], {}, 0, -1, 41):
                with self.subTest(side=side, value=value):
                    payload = battle()
                    payload[side]['current_hp'] = value
                    self.assert_unknown(payload, side, 'current_hp')

    def test_supported_collections_and_hp_controls(self):
        for side in SIDES:
            for skills in ([], ['veteran'], ['hit_rate_plus_10'], ['luna']):
                for weaknesses in ([], ['beast'], ['dragon'], ['armour'], ['flying'], ['beast', 'dragon', 'armour', 'flying']):
                    for hp in (1, 40):
                        with self.subTest(side=side, skills=skills, weaknesses=weaknesses, hp=hp):
                            payload = battle()
                            payload[side].update(skills=skills, weaknesses=weaknesses, current_hp=hp)
                            before = copy.deepcopy(payload)
                            result = assess(payload)
                            self.assertIsNotNone(result['outcome'])
                            self.assertEqual(result['forecast'], calculate(payload))
                            self.assertFalse(result['safe_to_claim_map_survival'])
                            self.assertEqual(payload, before)

    def test_unequipped_defender_still_validates_observation(self):
        for field, value in (('skills', {}), ('weaknesses', ''), ('current_hp', True)):
            payload = battle()
            payload['defender'].update(weapon=None, weapon_state='unequipped', remaining_uses=0)
            payload['defender'][field] = value
            self.assert_unknown(payload, 'defender', field)
        payload = battle()
        payload['defender'].update(weapon=None, weapon_state='unequipped', remaining_uses=0)
        before = copy.deepcopy(payload)
        result = assess(payload)
        self.assertIsNotNone(result['outcome'])
        self.assertFalse(result['forecast']['defender']['can_attack'])
        self.assertEqual(result['forecast'], calculate(payload))
        self.assertEqual(payload, before)

    def test_context_and_real_effect_refusals_preserved(self):
        for side in SIDES:
            for skill, field in (('indoor_fighter', 'outdoors'), ('even_rhythm', 'turn')):
                payload = battle()
                payload[side]['skills'] = [skill]
                self.assert_unknown(payload, side, 'context.' + field)
            for skills in (['counter'], ['dragonskin'], ['aether'], ['astra'], ['luna', 'sol'], ['pavise', 'aegis']):
                payload = battle()
                payload[side]['skills'] = skills
                payload[side]['stats']['skl'] = 10
                before = copy.deepcopy(payload)
                result = assess(payload)
                self.assertEqual(result['status'], 'UNKNOWN')
                self.assertIsNone(result['outcome'])
                self.assertEqual(payload, before)
            payload = battle()
            payload[side]['weapon']['effect'] = 'Drains HP'
            self.assert_unknown(payload, side, 'weapon.effect')
        for support in ('paired', 'adjacent'):
            payload = battle()
            payload.update(support_state=support, partners=['observed_partner'])
            before = copy.deepcopy(payload)
            self.assertIsNone(assess(payload)['outcome'])
            self.assertEqual(payload, before)

    def test_public_json_cli_both_sides(self):
        with tempfile.TemporaryDirectory(prefix='combat-input-shapes-') as temp:
            path = Path(temp) / 'synthetic-battle.json'
            for side in SIDES:
                for field, values in (
                    ('skills', (None, '', {}, [None], [False], [0], [[]], [{}], ['UNKNOWN'], [])),
                    ('weaknesses', (None, '', {}, [None], [False], [0], [[]], [{}], ['UNKNOWN'], [])),
                    ('current_hp', (None, True, False, 1.0, 1.5, '1', 0, -1, 41, 1, 40)),
                ):
                    for value in values:
                        with self.subTest(side=side, field=field, value=value):
                            payload = battle()
                            payload[side][field] = value
                            encoded = json.dumps(payload)
                            path.write_text(encoded, encoding='utf-8')
                            process = subprocess.run([sys.executable, str(ROOT / 'tools/tactical_combat.py'), str(path)],
                                                     cwd=ROOT, capture_output=True, text=True)
                            self.assertEqual(process.returncode, 0, process.stderr)
                            result = json.loads(process.stdout)
                            self.assertEqual(result, assess(payload))
                            self.assertEqual(path.read_text(encoding='utf-8'), encoded)
                            valid = value == [] if field != 'current_hp' else type(value) is int and value in (1, 40)
                            if valid:
                                self.assertIsNotNone(result['outcome'])
                            else:
                                self.assertEqual(result['status'], 'UNKNOWN')
                                self.assertIsNone(result['outcome'])
                                self.assertFalse(result['safe_to_claim_survival'])
                                self.assertIn(side + ':' + field, result.get('reason', str(result.get('missing', []))))


if __name__ == '__main__':
    unittest.main()

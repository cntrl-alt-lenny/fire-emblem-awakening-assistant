"""Strict live context contract; synthetic fixtures never use player run state."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from combat_calculator import calculate
from tactical_combat import assess
from test_hard import battle

ROOT = Path(__file__).resolve().parents[1]
FIGHTERS = ('indoor_fighter', 'outdoor_fighter')
TURN_SKILLS = ('lucky_seven', 'even_rhythm', 'odd_rhythm')
SIDES = ('attacker', 'defender')


class CombatContextTests(unittest.TestCase):
    def assert_unknown(self, payload, field=None, side=None):
        before = copy.deepcopy(payload)
        result = assess(payload)
        self.assertEqual(payload, before)
        self.assertEqual(result['status'], 'UNKNOWN')
        self.assertIsNone(result['outcome'])
        self.assertFalse(result['safe_to_claim_survival'])
        if field:
            diagnostic = result.get('reason', str(result.get('missing', [])))
            self.assertIn(field, diagnostic)
            self.assertIn(side, diagnostic)
        return result

    def test_fighter_missing_and_malformed_context_refused(self):
        for side in SIDES:
            for skill in FIGHTERS:
                for value in (None, 0, 1, -1, 1.0, '', 'unknown', 'false', [], {}, [True]):
                    with self.subTest(side=side, skill=skill, value=value):
                        payload = battle()
                        payload[side]['skills'] = [skill]
                        payload['context']['outdoors'] = value
                        self.assert_unknown(payload, 'outdoors', side)
                with self.subTest(side=side, skill=skill, missing=True):
                    payload = battle()
                    payload[side]['skills'] = [skill]
                    self.assert_unknown(payload, 'outdoors', side)

    def test_turn_missing_and_malformed_context_refused(self):
        for side in SIDES:
            for skill in TURN_SKILLS:
                for value in (None, 0, -1, True, False, 1.0, 1.5, '1', 'unknown', [], {}, [1]):
                    with self.subTest(side=side, skill=skill, value=value):
                        payload = battle()
                        payload[side]['skills'] = [skill]
                        payload['context']['turn'] = value
                        self.assert_unknown(payload, 'turn', side)
                with self.subTest(side=side, skill=skill, missing=True):
                    payload = battle()
                    payload[side]['skills'] = [skill]
                    self.assert_unknown(payload, 'turn', side)

    def assert_hits_and_outcome(self, payload, skill_side, bonus):
        before = copy.deepcopy(payload)
        result = assess(payload)
        self.assertEqual(payload, before)
        self.assertIsNotNone(result['outcome'])
        other = 'defender' if skill_side == 'attacker' else 'attacker'
        self.assertEqual(result['forecast'][skill_side]['displayed_hit'], min(100, 85 + bonus))
        self.assertEqual(result['forecast'][other]['displayed_hit'], 85 - bonus)
        # A gate-only change must preserve every calculator forecast/outcome field.
        self.assertEqual(result['forecast'], calculate(payload))
        self.assertFalse(result['safe_to_claim_map_survival'])

    def test_fighter_true_false_numerical_controls(self):
        for side in SIDES:
            for skill in FIGHTERS:
                for outdoors in (True, False):
                    with self.subTest(side=side, skill=skill, outdoors=outdoors):
                        payload = battle()
                        payload[side]['skills'] = [skill]
                        payload['context']['outdoors'] = outdoors
                        active = outdoors if skill == 'outdoor_fighter' else not outdoors
                        self.assert_hits_and_outcome(payload, side, 10 if active else 0)

    def test_turn_boundaries_and_parity_numerical_controls(self):
        for side in SIDES:
            for skill in TURN_SKILLS:
                for turn in (1, 2, 7, 8):
                    with self.subTest(side=side, skill=skill, turn=turn):
                        payload = battle()
                        payload[side]['skills'] = [skill]
                        payload['context']['turn'] = turn
                        active = (turn <= 7 if skill == 'lucky_seven' else
                                  turn % 2 == (0 if skill == 'even_rhythm' else 1))
                        self.assert_hits_and_outcome(payload, side, (20 if skill == 'lucky_seven' else 10) if active else 0)

    def test_optional_fields_absent_without_relevant_skill(self):
        for side in SIDES:
            for skill in (None, 'outdoor_fighter', 'lucky_seven'):
                payload = battle()
                if skill:
                    payload[side]['skills'] = [skill]
                    field, value = ('outdoors', True) if skill == 'outdoor_fighter' else ('turn', 1)
                    payload['context'][field] = value
                with self.subTest(side=side, skill=skill):
                    before = copy.deepcopy(payload)
                    self.assertEqual(assess(payload)['forecast'], calculate(payload))
                    self.assertEqual(payload, before)

    def test_both_sides_and_both_context_fields(self):
        payload = battle()
        payload['attacker']['skills'] = ['indoor_fighter', 'lucky_seven']
        payload['defender']['skills'] = ['outdoor_fighter', 'even_rhythm']
        payload['context'].update(outdoors=False, turn=8)
        self.assertEqual(assess(payload)['forecast'], calculate(payload))
        for field in ('outdoors', 'turn'):
            bad = copy.deepcopy(payload)
            bad['context'][field] = None
            self.assert_unknown(bad, field, 'attacker')

    def test_defender_without_counterattack_still_requires_context(self):
        for skill, field in (('outdoor_fighter', 'outdoors'), ('odd_rhythm', 'turn')):
            with self.subTest(skill=skill):
                payload = battle()
                payload['defender'].update(weapon=None, weapon_state='unequipped', skills=[skill])
                self.assert_unknown(payload, field, 'defender')

    def test_paired_and_unsupported_effect_refusals_preserved(self):
        for support in ('paired', 'adjacent'):
            payload = battle()
            payload.update(support_state=support, partners=['observed_partner'])
            self.assert_unknown(payload)
        payload = battle()
        payload['partners'] = ['observed_partner']
        self.assert_unknown(payload)
        for side in SIDES:
            for skill in ('counter', 'dragonskin', 'astra'):
                payload = battle()
                payload[side]['skills'] = [skill]
                self.assert_unknown(payload)
            payload = battle()
            payload[side]['weapon']['effect'] = 'Drains HP'
            self.assert_unknown(payload)

    def test_public_json_cli_invalid_and_valid(self):
        cases = []
        for side in SIDES:
            for skill, field, value, status in (
                ('outdoor_fighter', 'outdoors', 'unknown', 'UNKNOWN'),
                ('indoor_fighter', 'outdoors', None, 'UNKNOWN'),
                ('lucky_seven', 'turn', True, 'UNKNOWN'),
                ('even_rhythm', 'turn', 0, 'UNKNOWN'),
                ('odd_rhythm', 'turn', -1, 'UNKNOWN'),
                ('outdoor_fighter', 'outdoors', False, 'NO_MODELED_DEATH_IN_THIS_DUEL'),
                ('lucky_seven', 'turn', 8, 'NO_MODELED_DEATH_IN_THIS_DUEL'),
            ):
                payload = battle()
                payload[side]['skills'] = [skill]
                payload['context'][field] = value
                cases.append((side, skill, payload, status))
        with tempfile.TemporaryDirectory(prefix='combat-context-test-') as temp:
            path = Path(temp) / 'synthetic-battle.json'
            for side, skill, payload, status in cases:
                with self.subTest(side=side, skill=skill, status=status):
                    encoded = json.dumps(payload)
                    path.write_text(encoded, encoding='utf-8')
                    result = subprocess.run(
                        [sys.executable, str(ROOT / 'tools' / 'tactical_combat.py'), str(path)],
                        cwd=ROOT, capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    output = json.loads(result.stdout)
                    self.assertEqual(output['status'], status)
                    self.assertEqual(path.read_text(encoding='utf-8'), encoded)
                    self.assertEqual(output, assess(payload))
                    self.assertEqual(output['outcome'] is None, status == 'UNKNOWN')


if __name__ == '__main__':
    unittest.main()

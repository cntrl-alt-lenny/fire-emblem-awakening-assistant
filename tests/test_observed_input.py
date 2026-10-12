"""Synthetic public entry workflows; no gameplay certification or live runs."""
import copy
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from observed_input import (Collector, Cancelled, create_output, integer,
                            load_draft, observations_known)
from tactical_combat import assess
from tactical_enemy_phase import unit_shape, evaluate


def transcript(weapon='custom', stats='40 10 10 0 10 0 5 5', skills='none',
               bonuses='none', effect='none', support='none', confirm='yes'):
    lines = ['Hard', 'Classic', 'effective_displayed', support,
             'none' if support == 'none' else 'observed_partner']
    for side in ('attacker', 'defender'):
        lines += [stats, '40', weapon]
        if weapon == 'custom':
            lines += ['sword', 'physical', 'E', '5 100 0', '1', effect, 'no', 'none']
        elif weapon.startswith('catalog '):
            lines += ['yes']
        lines += ['E' if weapon == 'custom' else 'D', skills, 'none', 'none', bonuses, '50']
    lines += ['1']
    if skills in ('indoor_fighter', 'outdoor_fighter'):
        lines += ['yes']
    if skills in ('lucky_seven', 'even_rhythm', 'odd_rhythm'):
        lines += ['1']
    return '\n'.join(lines + [confirm]) + '\n'


def collect(text, draft=None):
    stderr = io.StringIO()
    payload = Collector(io.StringIO(text), stderr).collect(draft)
    return payload, stderr.getvalue()


def edit_transcript(payload, final='yes', replacements=None):
    # Each present observation needs a separate deliberate keep; no final reuse.
    replacements = replacements or {}
    lines = ['keep'] * 5
    for side in ('attacker', 'defender'):
        keys = ['stats', 'current_hp', 'weapon']
        if 'weapon_state' in payload[side]:
            keys += ['weapon_state']
        keys += ['weapon_rank', 'skills', 'weaknesses', 'terrain', 'combat_bonuses', 'remaining_uses']
        keys += [key for key in ('forge', 'alive', 'id', 'name') if key in payload[side]]
        lines += [replacements.get((side, key), 'keep') for key in keys]
    lines += ['keep']
    lines += ['keep' for key in ('outdoors', 'turn') if key in payload['context']]
    return '\n'.join(lines + [final]) + '\n'


class ObservedInputTests(unittest.TestCase):
    def cli(self, text, *args):
        return subprocess.run([sys.executable, str(ROOT / 'tools/observed_input.py'), *args],
                              input=text, text=True, capture_output=True, cwd=ROOT)

    def test_complete_public_transcript_and_gate_equality(self):
        process = self.cli(transcript())
        self.assertEqual(process.returncode, 0, process.stderr)
        payload = json.loads(process.stdout)
        self.assertTrue(payload['observed_inputs_complete'])
        self.assertEqual(payload['context'], {'distance': 1})
        self.assertEqual(payload['attacker']['stats'], dict(zip(
            ('hp', 'str', 'mag', 'skl', 'spd', 'lck', 'def', 'res'), (40, 10, 10, 0, 10, 0, 5, 5))))
        self.assertEqual(payload['attacker']['skills'], [])
        self.assertEqual(payload['attacker']['terrain'], {})
        result = assess(payload)
        with tempfile.TemporaryDirectory() as temp:
            selected = Path(temp) / 'duel.json'
            selected.write_text(process.stdout, encoding='utf-8')
            gate = subprocess.run([sys.executable, str(ROOT / 'tools/tactical_combat.py'), str(selected)],
                                  text=True, capture_output=True)
            self.assertEqual(gate.returncode, 0)
            self.assertEqual(json.loads(gate.stdout), result)
        self.assertEqual(result['status'], 'NO_MODELED_DEATH_IN_THIS_DUEL')
        self.assertNotIn('safe', process.stderr.lower())
        self.assertEqual(process.stderr.count('[blank/? unknown; cancel stops]'), 41)

    def test_blank_question_and_partial_group_never_complete(self):
        for text in (transcript(stats='40 10 ? 0 10 0 5 5'), transcript(skills=''),
                     transcript(bonuses='?'), transcript().replace('\n40\n', '\n?\n', 1)):
            process = self.cli(text)
            self.assertEqual(process.returncode, 0, process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload['observed_inputs_complete'])
            self.assertEqual(assess(payload)['status'], 'UNKNOWN')
            self.assertNotIn('probability=', process.stderr)
            self.assertNotIn('displayed_hit', process.stderr)
        payload, _ = collect(transcript(stats='40 10 ? 0 10 0 5 5'))
        self.assertIsNone(payload['attacker']['stats']['mag'])

    def test_integer_no_boolean_float_or_rounding(self):
        for value in ('true', 'false', '1.0', '1.5', '1e2', 'NaN'):
            with self.assertRaises(ValueError):
                integer(value)
        self.assertEqual(integer('0'), 0)
        self.assertEqual(integer('-2'), -2)
        text = transcript().replace('\n40\n', '\n1.5\n40\n', 1)
        payload, stderr = collect(text)
        self.assertEqual(payload['attacker']['current_hp'], 40)
        self.assertIn('not a boolean or decimal', stderr)

    def test_unsupported_effects_and_paired_refused_without_numeric_leaks(self):
        for text in (transcript(skills='counter'), transcript(effect='Drains HP'),
                     transcript(support='paired'), transcript(support='adjacent')):
            process = self.cli(text)
            self.assertEqual(process.returncode, 0, process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload['observed_inputs_complete'])
            self.assertEqual(assess(payload)['status'], 'UNKNOWN')
            self.assertNotIn('probability=', process.stderr)
        payload, _ = collect(transcript(skills='counter'))
        self.assertEqual(payload['attacker']['skills'], ['counter'])
        payload, _ = collect(transcript(effect='Drains HP'))
        self.assertEqual(payload['attacker']['weapon']['effect'], 'Drains HP')

    def test_forge_actual_values_raw_basis_and_bonus_values_preserved(self):
        payload, _ = collect(transcript().replace('5 100 0', '8 110 3'))
        self.assertEqual(payload['attacker']['weapon']['might'], 8)
        self.assertEqual(payload['attacker']['weapon']['hit'], 110)
        self.assertIsNotNone(assess(payload)['outcome'])
        for side in ('attacker', 'defender'):
            unit_shape(payload[side], side, side)
        sequence = {key: payload[key] for key in ('difficulty', 'mode', 'observed_inputs_complete', 'stats_basis', 'support_state', 'partners')}
        sequence.update(player_id='observed_player', player=payload['defender'], enemies=[{'id': 'enemy_one', 'unit': payload['attacker'], 'context': payload['context']}])
        self.assertIsNotNone(evaluate(sequence)['outcome'])
        payload, _ = collect(transcript(bonuses='2 3 4 5 6').replace('effective_displayed', 'raw_permanent'))
        self.assertEqual(payload['attacker']['stats']['str'], 10)
        self.assertEqual(payload['attacker']['combat_bonuses']['attack'], 6)
        self.assertEqual(assess(payload)['status'], 'UNKNOWN')

    def test_catalog_requires_exact_unforged_confirmation_and_unknown_not_guessed(self):
        payload, _ = collect(transcript(weapon='catalog iron_sword'))
        self.assertEqual(payload['attacker']['weapon']['might'], 5)
        self.assertIsNotNone(assess(payload)['outcome'])
        text = transcript(weapon='catalog iron_sword').replace('catalog iron_sword\nyes', 'catalog iron_sword\n?', 1)
        payload, _ = collect(text)
        self.assertIsNone(payload['attacker']['weapon'])
        self.assertFalse(payload['observed_inputs_complete'])
        text = transcript().replace('\ncustom\n', '\ncatalog no_such_weapon\ncustom\n', 1)
        payload, stderr = collect(text)
        self.assertEqual(payload['attacker']['weapon']['might'], 5)
        self.assertIn('no values were guessed', stderr)

    def test_unarmed_defender_explicit_and_attacker_refusal(self):
        text = transcript()
        first = text.find('custom')
        second = text.find('custom', first + 1)
        text = text[:second] + text[second:].replace('custom\nsword\nphysical\nE\n5 100 0\n1\nnone\nno\nnone', 'unequipped', 1)
        text = text[:second] + text[second:].replace('50\n', '0\n', 1)
        payload, _ = collect(text)
        self.assertIsNone(payload['defender']['weapon'])
        self.assertEqual(payload['defender']['weapon_state'], 'unequipped')
        self.assertTrue(payload['observed_inputs_complete'])
        self.assertFalse(assess(payload)['forecast']['defender']['can_attack'])
        edited, _ = collect(edit_transcript(payload), payload)
        self.assertEqual(edited, payload)
        text = transcript().replace('\ncustom\n', '\nunequipped\ncustom\n', 1)
        _, stderr = collect(text)
        self.assertIn('Only a defender', stderr)

    def test_edit_deliberate_keep_renewal_unknown_and_effect_preservation(self):
        payload, _ = collect(transcript(skills='counter'))
        edited, _ = collect(edit_transcript(payload), payload)
        self.assertEqual(edited, payload)
        self.assertEqual(edited['attacker']['skills'], ['counter'])
        for final in ('', '?', 'no'):
            edited, _ = collect(edit_transcript(payload, final), payload)
            self.assertFalse(edited['observed_inputs_complete'])
        edited, _ = collect(edit_transcript(payload, replacements={('attacker', 'current_hp'): ''}), payload)
        self.assertIsNone(edited['attacker']['current_hp'])
        self.assertFalse(edited['observed_inputs_complete'])
        payload['attacker']['forge'] = {'might': 3}
        edited, _ = collect(edit_transcript(payload), payload)
        self.assertEqual(edited['attacker']['forge'], {'might': 3})
        self.assertEqual(assess(edited)['status'], 'UNKNOWN')
        payload['context']['turn'] = None
        edited, _ = collect(edit_transcript(payload), payload)
        self.assertIn('turn', edited['context'])
        self.assertIsNone(edited['context']['turn'])
        self.assertFalse(edited['observed_inputs_complete'])

    def test_conditional_context_is_explicit_unknown_not_defaulted(self):
        for skill, field in (('indoor_fighter', 'outdoors'), ('odd_rhythm', 'turn')):
            payload, _ = collect(transcript(skills=skill))
            self.assertIn(field, payload['context'])
            self.assertIsNotNone(assess(payload)['outcome'])
            text = transcript(skills=skill).rsplit('\n', 4)
            payload['context'][field] = None
            self.assertFalse(observations_known(payload))

    def test_public_edit_unknown_invalid_range_and_effectiveness_never_complete(self):
        original, _ = collect(transcript())
        with tempfile.TemporaryDirectory() as temp:
            draft = Path(temp) / 'synthetic.json'
            for side in ('attacker', 'defender'):
                for field, values in (
                    ('range', ('?', 'UNKNOWN', '0', 0, -1, '2-1', '2~1', '1-?', 'one', '', None, True, 1.0)),
                    ('effectiveness', (['?'], ['UNKNOWN'], ['not_a_category'], [None], None))):
                    for value in values:
                        with self.subTest(side=side, field=field, value=value):
                            payload = copy.deepcopy(original)
                            payload[side]['weapon'][field] = value
                            draft.write_text(json.dumps(payload), encoding='utf-8')
                            before = draft.read_bytes()
                            process = self.cli(edit_transcript(payload), '--edit', str(draft))
                            self.assertEqual(process.returncode, 0, process.stderr)
                            result = json.loads(process.stdout)
                            self.assertEqual(result[side]['weapon'][field], value)
                            self.assertFalse(result['observed_inputs_complete'])
                            self.assertEqual(assess(result)['status'], 'UNKNOWN')
                            self.assertNotIn('probability=', process.stderr)
                            self.assertEqual(draft.read_bytes(), before)
            for value in ('1', '1-2', '1~2', 1):
                payload = copy.deepcopy(original)
                payload['attacker']['weapon']['range'] = value
                draft.write_text(json.dumps(payload), encoding='utf-8')
                process = self.cli(edit_transcript(payload), '--edit', str(draft))
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertTrue(json.loads(process.stdout)['observed_inputs_complete'])

    def test_edit_rejects_run_paths_aliases_shapes_extras_duplicate_keys(self):
        payload, _ = collect(transcript())
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            run = base / 'current_run.json'
            run.write_text('DO NOT OPEN', encoding='utf-8')
            alias = base / 'alias.json'
            alias.symlink_to(run)
            for path in (run, alias):
                with patch.object(Path, 'read_text', side_effect=AssertionError('opened a run')):
                    with self.assertRaises(ValueError):
                        load_draft(path)
            draft = base / 'draft.json'
            for bad in ({'army': []}, dict(payload, events=[])):
                draft.write_text(json.dumps(bad), encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_draft(draft)
            for location in ('unit', 'weapon', 'context', 'stats', 'terrain', 'combat_bonuses'):
                bad = copy.deepcopy(payload)
                where = bad['context'] if location == 'context' else bad['attacker']
                if location not in ('unit', 'context'):
                    where = where[location]
                where['unmodeled_effect'] = 'real effect'
                draft.write_text(json.dumps(bad), encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_draft(draft)
            draft.write_text('{"attacker":{},"attacker":{},"defender":{}}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                load_draft(draft)
            draft.write_text(json.dumps(payload), encoding='utf-8')
            before = draft.read_bytes()
            process = self.cli(edit_transcript(payload), '--edit', str(draft))
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(process.stdout), payload)
            self.assertEqual(draft.read_bytes(), before)

    def test_cancel_and_eof_no_stdout_or_output_no_draft_overwrite(self):
        payload, _ = collect(transcript())
        with tempfile.TemporaryDirectory() as temp:
            draft = Path(temp) / 'draft.json'
            draft.write_text(json.dumps(payload), encoding='utf-8')
            before = draft.read_bytes()
            for text in ('', 'cancel\n', '\n'.join(['keep'] * 9) + '\n', edit_transcript(payload, 'cancel')):
                process = self.cli(text, '--edit', str(draft))
                self.assertEqual(process.returncode, 1, process.stderr)
                self.assertEqual(process.stdout, '')
                self.assertEqual(draft.read_bytes(), before)
            with patch('observed_input.create_output') as write:
                with patch('sys.stdin', io.StringIO('cancel\n')), patch('sys.stderr', io.StringIO()), patch('sys.stdout', io.StringIO()):
                    from observed_input import main
                    self.assertEqual(main(['--output', 'state/observations/new.json']), 1)
                write.assert_not_called()

    def test_create_only_output_boundaries_symlinks_and_existing_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'state').mkdir()
            with patch('observed_input.ROOT', root):
                destination = root / 'state/observations/nested/new.json'
                create_output(destination, '{"synthetic":true}\n')
                before = destination.read_bytes()
                with self.assertRaises(OSError):
                    create_output(destination, 'REPLACE')
                self.assertEqual(destination.read_bytes(), before)
                for path in (root / 'outside.json', root / 'state/observations/current_run.json',
                             root / 'state/observations/../escape.json', root / 'state/observations/new.txt'):
                    with self.assertRaises(ValueError):
                        create_output(path, 'NO')
                (root / 'state/observations/link').symlink_to(root, target_is_directory=True)
                with self.assertRaises(OSError):
                    create_output(root / 'state/observations/link/escape.json', 'NO')
                (root / 'state/observations/leaf.json').symlink_to(destination)
                with self.assertRaises(OSError):
                    create_output(root / 'state/observations/leaf.json', 'NO')
                self.assertEqual(destination.read_bytes(), before)
                self.assertFalse((root / 'escape.json').exists())
                self.assertEqual(os.stat(destination).st_mode & 0o777, 0o600)


if __name__ == '__main__':
    unittest.main()

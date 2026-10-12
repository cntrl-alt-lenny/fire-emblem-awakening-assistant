"""Synthetic assembler controls; never open or modify a live run."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from sequence_input import assemble, create_output, read_duel
from tactical_enemy_phase import evaluate
from tactical_combat import known_weapon


def fixtures():
    expected = json.loads((ROOT / 'examples/observed_enemy_sequence.json').read_text())
    duels = []
    for entry in expected['enemies']:
        duel = {key: copy.deepcopy(expected[key]) for key in
                ('difficulty', 'mode', 'stats_basis', 'support_state', 'partners',
                 'observed_inputs_complete')}
        duel.update(attacker=copy.deepcopy(entry['unit']), defender=copy.deepcopy(expected['player']),
                    context=copy.deepcopy(entry['context']))
        duels.append((entry['id'], duel))
    return expected, duels


class SequenceInputTests(unittest.TestCase):
    def test_exact_existing_sequence_and_assessment_equality(self):
        expected, duels = fixtures()
        before = copy.deepcopy(duels)
        for _, source in duels:
            source['note'] = 'Synthetic nonmechanical comment'
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertEqual(actual, expected)
        self.assertEqual(evaluate(actual), evaluate(expected))
        for (_, source), (_, original) in zip(duels, before):
            del source['note']
            self.assertEqual(source, original)
        actual['player']['stats']['hp'] = 999
        self.assertEqual(duels, before)

    def test_confirmations_are_independent_and_renewed(self):
        expected, duels = fixtures()
        for flags in ((False, True, True), (True, False, True), (True, True, False), (1, True, True)):
            actual = assemble(expected['player_id'], duels, *flags)
            self.assertFalse(actual['observed_inputs_complete'])
            self.assertIsNone(evaluate(actual)['outcome'])
        duels[1][1]['observed_inputs_complete'] = False
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertFalse(actual['observed_inputs_complete'])

    def test_mismatched_stale_missing_and_type_changed_player(self):
        for mutate, field in (
                (lambda d: d['defender'].update(current_hp=1), 'defender.current_hp'),
                (lambda d: d['defender']['stats'].update(spd=99), 'defender.stats.spd'),
                (lambda d: d['defender'].pop('terrain'), 'defender.terrain'),
                (lambda d: d['defender']['terrain'].update(defense=None), 'defender.terrain.defense'),
                (lambda d: d['defender'].update(remaining_uses=True), 'defender.remaining_uses')):
            expected, duels = fixtures()
            mutate(duels[1][1])
            with self.assertRaisesRegex(ValueError, r'entries\[1\].' + field):
                assemble(expected['player_id'], duels, True, True, True)

    def test_rulesets_support_and_identity_conflicts(self):
        for field, value in (('difficulty', 'Normal'), ('mode', 'Casual'),
                             ('stats_basis', 'raw'), ('support_state', 'paired'), ('partners', ['ally'])):
            expected, duels = fixtures()
            duels[1][1][field] = value
            with self.assertRaisesRegex(ValueError, field):
                assemble(expected['player_id'], duels, True, True, True)
        expected, duels = fixtures()
        for identity in (duels[0][0], expected['player_id'], '', ' enemy ', None):
            selected = [duels[0], (identity, duels[1][1])]
            with self.assertRaisesRegex(ValueError, 'id'):
                assemble(expected['player_id'], selected)

    def test_unknown_supplied_keys_refuse_without_disappearing(self):
        for field in ('enemy_effects', 'run', 'events'):
            expected, duels = fixtures()
            duels[1][1][field] = ['Counter']
            with self.assertRaisesRegex(ValueError, field):
                assemble(expected['player_id'], duels, True, True, True)
        for field in ('skills', 'weaknesses', 'current_hp', 'terrain', 'weapon'):
            expected, duels = fixtures()
            duels[1][1]['attacker'][field] = None
            actual = assemble(expected['player_id'], duels, True, True, True)
            self.assertIsNone(actual['enemies'][1]['unit'][field])
            self.assertIsNone(evaluate(actual)['outcome'])
        expected, duels = fixtures()
        duels[1][1]['attacker']['unknown_effect'] = 'must survive'
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertEqual(actual['enemies'][1]['unit']['unknown_effect'], 'must survive')
        self.assertIsNone(evaluate(actual)['outcome'])

    def test_unsupported_tail_forged_paired_and_unarmed(self):
        for mutate in (
                lambda d: d['attacker'].update(skills=['counter']),
                lambda d: d['attacker']['weapon'].update(effect='Drains HP'),
                lambda d: d['attacker']['weapon'].update(forge_marker='++')):
            expected, duels = fixtures()
            duels[1][1]['attacker']['weapon'] = known_weapon(duels[1][1]['attacker'], 'attacker')
            mutate(duels[1][1])
            actual = assemble(expected['player_id'], duels, True, True, True)
            self.assertEqual(actual['enemies'][1]['unit'], duels[1][1]['attacker'])
            self.assertIsNone(evaluate(actual)['outcome'])
        expected, duels = fixtures()
        for _, duel in duels:
            duel.update(support_state='paired', partners=[{'unknown': None}])
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertEqual(actual['partners'], [{'unknown': None}])
        self.assertIsNone(evaluate(actual)['outcome'])
        expected, duels = fixtures()
        for _, duel in duels:
            duel['defender'].update(weapon=None, weapon_state='unequipped', remaining_uses=0)
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertIsNotNone(evaluate(actual)['outcome'])
        duels[1][1]['attacker']['weapon'] = known_weapon(duels[1][1]['attacker'], 'attacker')
        duels[1][1]['attacker']['weapon']['might'] += 1
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertEqual(actual['enemies'][1]['unit']['weapon']['might'],
                         duels[1][1]['attacker']['weapon']['might'])

    def test_context_conflicts_and_missing_not_inherited(self):
        expected, duels = fixtures()
        duels[0][1]['context'].update(turn=1, outdoors=True)
        duels[1][1]['context'].update(turn=2, outdoors=False)
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertIn('conflicts', evaluate(actual)['reason'])
        del duels[1][1]['context']['turn']
        del duels[1][1]['context']['outdoors']
        duels[1][1]['attacker']['skills'] = ['outdoor_fighter']
        actual = assemble(expected['player_id'], duels, True, True, True)
        self.assertEqual(actual['enemies'][1]['context'], duels[1][1]['context'])
        self.assertIsNone(evaluate(actual)['outcome'])

    def run_cli(self, args, stdin=''):
        return subprocess.run([sys.executable, str(ROOT / 'tools/sequence_input.py')] + args,
                              input=stdin, capture_output=True, text=True, cwd=ROOT)

    def test_explicit_cli_order_sources_read_only_and_missing_confirmation(self):
        expected, duels = fixtures()
        with tempfile.TemporaryDirectory() as tmp:
            args = ['--player-id', expected['player_id']]
            paths = []
            for index, (identity, source) in enumerate(duels):
                path = Path(tmp) / (str(index) + '.json')
                path.write_text(json.dumps(source))
                path.chmod(0o400)
                paths.append((path, path.read_bytes()))
                args += ['--enemy', identity, str(path)]
            result = self.run_cli(args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)['observed_inputs_complete'])
            self.assertIn('UNKNOWN', result.stderr)
            result = self.run_cli(args + ['--confirm-order', '--confirm-unchanged', '--confirm-no-events'])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), expected)
            self.assertIn(evaluate(expected)['status'], result.stderr)
            rejected = self.run_cli(args + ['--confirm-order', '--confirm-unchanged',
                                            '--confirm-no-events', '--output', 'state/current_run.json'])
            self.assertEqual(rejected.returncode, 2)
            self.assertEqual(rejected.stdout, '')
            for path, original in paths:
                self.assertEqual(path.read_bytes(), original)

    def test_guided_no_json_editing_and_cancellation(self):
        expected, duels = fixtures()
        with tempfile.TemporaryDirectory() as tmp:
            answers = [expected['player_id']]
            for index, (identity, source) in enumerate(duels):
                path = Path(tmp) / (str(index) + '.json')
                path.write_text(json.dumps(source))
                answers += [str(path), identity]
            answers += ['', 'yes', 'yes', 'yes']
            self.assertEqual(len(answers), 9)  # 1 player, 4 file/ID, finish, 3 confirmations
            result = self.run_cli([], '\n'.join(answers) + '\n')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), expected)
            self.assertIn('Supplied order:', result.stderr)
            # Every EOF boundary, including after two confirmations, emits nothing.
            for stop in range(len(answers)):
                result = self.run_cli([], '\n'.join(answers[:stop]) + ('\n' if stop else ''))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, '')
            result = self.run_cli([], 'cancel\n')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            destination = 'state/observations/cancel-' + uuid.uuid4().hex + '.json'
            result = self.run_cli(['--output', destination], '\n'.join(answers[:-1]) + '\n')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertFalse((ROOT / destination).exists())
            answers[-1] = 'no'
            result = self.run_cli([], '\n'.join(answers) + '\n')
            self.assertFalse(json.loads(result.stdout)['observed_inputs_complete'])

    def test_duplicate_json_run_sources_and_same_file_aliases(self):
        expected, duels = fixtures()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            duplicate = tmp / 'duplicate.json'
            duplicate.write_text('{"attacker":{"skills":[],"skills":["counter"]}}')
            with self.assertRaisesRegex(ValueError, 'duplicate.*skills'):
                read_duel(duplicate)
            live = tmp / 'current_run.json'
            live.write_text(json.dumps(duels[0][1]))
            alias = tmp / 'alias.json'
            alias.symlink_to(live)
            for path in (live, alias):
                with self.assertRaisesRegex(ValueError, 'live run'):
                    read_duel(path)
            source = tmp / 'duel.json'
            source.write_text(json.dumps(duels[0][1]))
            # A selected run-like basename also refuses a symlink to an ordinary duel.
            live.unlink()
            live.symlink_to(source)
            with self.assertRaisesRegex(ValueError, 'live run'):
                read_duel(live)
            live.unlink()
            (tmp / 'state').mkdir()
            live = tmp / 'state/current_run.json'
            live.write_text('private: must never be decoded')
            hardlink = tmp / 'hardlink.json'
            os.link(live, hardlink)
            with patch('sequence_input.ROOT', tmp):
                with self.assertRaisesRegex(ValueError, 'live run file aliases'):
                    read_duel(hardlink)
            alias.unlink()
            alias.symlink_to(source)
            result = self.run_cli(['--player-id', expected['player_id'], '--enemy', 'a', str(source),
                                   '--enemy', 'b', str(alias)])
            self.assertEqual(result.returncode, 2)
            self.assertIn('same source file', result.stderr)
            self.assertEqual(result.stdout, '')
            source.write_text('{"difficulty":"Hard","mode":"Classic","stats_basis":"effective_displayed",'
                              '"roster":[],"events":[]}')
            result = self.run_cli(['--player-id', 'player', '--enemy', 'enemy', str(source)])
            self.assertEqual(result.returncode, 2)
            self.assertIn('unsupported duel fields', result.stderr)

    def test_output_create_only_traversal_symlinks_and_live_run_protection(self):
        expected, _ = fixtures()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            filename = 'state/observations/nested/sequence.json'
            create_output(filename, expected, root)
            saved = root / filename
            before = saved.read_bytes()
            self.assertEqual(json.loads(before), expected)
            with self.assertRaises(FileExistsError):
                create_output(filename, {}, root)
            self.assertEqual(saved.read_bytes(), before)
            for invalid in ('state/current_run.json', 'state/observations/../current_run.json',
                            'state/observations/current_run.json',
                            '/state/observations/sequence.json', 'state/observations/a.txt'):
                with self.assertRaises(ValueError):
                    create_output(invalid, expected, root)
            outside = root / 'outside'
            outside.mkdir()
            linked = root / 'state/observations/link'
            linked.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(OSError):
                create_output('state/observations/link/a.json', expected, root)
            final_link = root / 'state/observations/final.json'
            final_link.symlink_to(outside / 'target.json')
            with self.assertRaises(OSError):
                create_output('state/observations/final.json', expected, root)
            self.assertEqual(list(outside.iterdir()), [])
            # Reject a symlink even when it points within the allowed subtree.
            linked.unlink()
            linked.symlink_to(saved.parent, target_is_directory=True)
            with self.assertRaises(OSError):
                create_output('state/observations/link/other.json', expected, root)

    def test_malformed_sources_and_nonmechanical_note(self):
        expected, duels = fixtures()
        duels[1][1]['note'] = {'counter': True}
        with self.assertRaisesRegex(ValueError, 'note'):
            assemble(expected['player_id'], duels, True, True, True)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'invalid.json'
            for content in ('{', '{"attacker":NaN}', '[]', '{}'):
                path.write_text(content)
                result = self.run_cli(['--player-id', 'player', '--enemy', 'enemy', str(path)])
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, '')
                self.assertEqual(path.read_text(), content)


if __name__ == '__main__':
    unittest.main()

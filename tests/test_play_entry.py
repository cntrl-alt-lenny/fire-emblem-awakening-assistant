"""Public CLI replay against unchanged tools, using synthetic observations only."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from play import assessment_path
from test_observed_input import transcript, edit_transcript
from test_sequence_input import fixtures


def cli(tool, answers='', args=()):
    return subprocess.run([sys.executable, str(ROOT / 'tools' / tool), *args],
                          cwd=ROOT, input=answers, text=True, capture_output=True)


class PlayEntryTests(unittest.TestCase):
    def compare(self, label, menu, tool, answers='', args=(), expected=0):
        direct = cli(tool, answers, args)
        launched = cli('play.py', menu + answers)
        self.assertEqual(direct.returncode, expected, direct.stderr)
        self.assertEqual(launched.returncode, direct.returncode, launched.stderr)
        self.assertEqual(launched.stdout, direct.stdout, label)
        # Delegated prompts, warnings and errors remain an exact stderr suffix.
        self.assertTrue(launched.stderr.endswith(direct.stderr), label)
        if os.environ.get('PLAY_ENTRY_EVIDENCE'):
            print('\nCASE:', label, '\nDIRECT:', tool, list(args),
                  '\nSTDIN:', repr(menu + answers), '\nEXIT:', launched.returncode,
                  '\nSTDOUT:', launched.stdout, '\nDELEGATED STDERR:', direct.stderr)
        return launched

    def test_map_views_phase_spoilers_and_refusal(self):
        for label, difficulty, phase, spoilers, view in (
                ('map tactical', 'hard', 'player', '', ''),
                ('map enemy phase details', 'hard', 'enemy', 'Tactical spoilers', 'details'),
                ('map no spoilers', 'hard', 'player', 'No spoilers', 'details'),
                ('map full provenance', 'hard', 'player', 'Full information', 'provenance'),
                ('unsupported map difficulty', 'normal', 'player', '', ''),
                ('invalid phase', 'hard', 'unknown', '', '')):
            args = ['--chapter', '7', '--difficulty', difficulty, '--turn', '5',
                    '--phase', phase, '--spoilers', spoilers or 'Tactical spoilers']
            if view:
                args += ['--' + view]
            menu = '\n'.join(['1', '7', difficulty, '5', phase, spoilers, view]) + '\n'
            self.compare(label, menu, 'play_briefing.py', args=args,
                         expected=2 if difficulty == 'normal' or phase == 'unknown' else 0)

    def test_collection_and_cancellation_preserve_batched_stdin(self):
        for label, answers in (
                ('complete collection', transcript()),
                ('partial collection', transcript(stats='40 10 ? 0 10 0 5 5')),
                ('unsupported Counter', transcript(skills='counter')),
                ('paired collection', transcript(support='paired')),
                ('collector cancellation', 'cancel\n'),
                ('collector EOF', 'Hard\n')):
            self.compare(label, '2\n\n', 'observed_input.py', answers,
                         expected=1 if label.startswith('collector') else 0)
        self.compare('protected output', '2\nstate/current_run.json\n',
                     'observed_input.py', transcript(), ['--output', 'state/current_run.json'], 2)

    def test_edit_assessment_sequence_and_sources_unchanged(self):
        expected, duels = fixtures()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            paths = []
            for index, (_, source) in enumerate(duels):
                path = tmp / (str(index) + '.json')
                path.write_text(json.dumps(source))
                paths.append(path)
            seq = tmp / 'sequence.json'
            seq.write_text(json.dumps(expected))
            originals = {p: p.read_bytes() for p in paths + [seq]}
            custom = json.loads(cli('observed_input.py', transcript()).stdout)
            edit_path = tmp / 'custom.json'
            edit_path.write_text(json.dumps(custom))
            originals[edit_path] = edit_path.read_bytes()
            for confirmation in ('yes', ''):
                self.compare('edit confirmation ' + repr(confirmation),
                             '3\n' + str(edit_path) + '\n\n', 'observed_input.py',
                             edit_transcript(custom, final=confirmation), ['--edit', str(edit_path)])
            answers = expected['player_id'] + '\n'
            for path, (identity, _) in zip(paths, duels):
                answers += str(path) + '\n' + identity + '\n'
            answers += '\nyes\nyes\nyes\n'
            self.compare('guided sequence', '4\n\n', 'sequence_input.py', answers)
            self.compare('sequence cancellation', '4\n\n', 'sequence_input.py',
                         answers.rsplit('yes\n', 1)[0] + 'cancel\n', expected=2)
            for menu, tool, path in (('5', 'tactical_combat.py', paths[0]),
                                     ('6', 'tactical_enemy_phase.py', seq)):
                self.compare('assessment ' + menu, menu + '\n' + str(path) + '\n', tool, args=[str(path)])
            for path, original in originals.items():
                self.assertEqual(path.read_bytes(), original)
            payload = duels[0][1]
            for label, mutate in (
                    ('partial assessment', lambda p: p.update(observed_inputs_complete=False)),
                    ('unsupported assessment', lambda p: p['attacker'].update(skills=['counter']))):
                mutate(payload)
                if label.startswith('unsupported'):
                    payload['observed_inputs_complete'] = True
                paths[0].write_text(json.dumps(payload))
                self.compare(label, '5\n' + str(paths[0]) + '\n', 'tactical_combat.py', args=[str(paths[0])])

    def test_selection_eof_cancel_invalid_and_no_second_action(self):
        for answers in ('', 'cancel\n', 'bad\n2\n\n' + transcript(),
                        '1\n7\nhard\n5\n', '1\n\n', '3\ncancel\n', '5\ncancel\n'):
            result = cli('play.py', answers)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(result.stdout, '')
        result = cli('play.py', '7\n2\n\n' + transcript())
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')

    def test_protected_run_aliases_before_open_and_wrong_kind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'state').mkdir()
            live = root / 'state/current_run.json'
            live.write_text('synthetic sentinel; must not be decoded')
            symbolic = root / 'symbolic.json'
            symbolic.symlink_to(live)
            hard = root / 'hard.json'
            os.link(live, hard)
            with patch('play.ROOT', root), patch.object(Path, 'read_text', side_effect=AssertionError('opened run')):
                for path in (live, symbolic, hard):
                    with self.assertRaises(ValueError):
                        assessment_path(str(path), 'duel')
            expected, duels = fixtures()
            source = root / 'selected.json'
            for payload, kind in ((expected, 'duel'), (duels[0][1], 'sequence'),
                                  (dict(duels[0][1], roster=[], events=[]), 'duel')):
                source.write_text(json.dumps(payload))
                with self.assertRaises(ValueError):
                    assessment_path(str(source), kind)
                result = cli('play.py', ('5' if kind == 'duel' else '6') + '\n' + str(source) + '\n')
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')

    def test_isolated_public_saving_and_run_alias_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'tools', root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
            (root / 'data').symlink_to(ROOT / 'data', target_is_directory=True)
            def run(tool, answers, args=()):
                return subprocess.run([sys.executable, str(root / 'tools' / tool), *args],
                                      cwd=root, input=answers, text=True, capture_output=True)
            destination = 'state/observations/new.json'
            direct = run('observed_input.py', transcript(), ['--output', destination])
            self.assertEqual(direct.returncode, 0, direct.stderr)
            saved = root / destination
            original = saved.read_bytes()
            saved.unlink()
            launched = run('play.py', '2\n' + destination + '\n' + transcript())
            self.assertEqual(launched.returncode, direct.returncode, launched.stderr)
            self.assertEqual(launched.stdout, direct.stdout)
            self.assertEqual(saved.read_bytes(), original)
            rejected = run('play.py', '2\n' + destination + '\n' + transcript())
            self.assertEqual(rejected.returncode, 2)
            self.assertEqual(rejected.stdout, '')
            self.assertEqual(saved.read_bytes(), original)
            other = root / 'outside'
            other.mkdir()
            (root / 'state/observations/link').symlink_to(other, target_is_directory=True)
            for output in ('state/observations/../current_run.json',
                           'state/observations/link/new.json'):
                rejected = run('play.py', '2\n' + output + '\n' + transcript())
                self.assertEqual(rejected.returncode, 2)
                self.assertEqual(rejected.stdout, '')
            self.assertEqual(list(other.iterdir()), [])
            live = root / 'state/current_run.json'
            live.write_text('synthetic sentinel')
            alias = root / 'alias.json'
            os.link(live, alias)
            for action in ('5', '6'):
                rejected = run('play.py', action + '\n' + str(alias) + '\n')
                self.assertEqual(rejected.returncode, 2)
                self.assertEqual(rejected.stdout, '')
                self.assertIn('aliases', rejected.stderr)
            self.assertEqual(live.read_text(), 'synthetic sentinel')

    def test_terminal_stream(self):
        # A PTY-backed stdin exercises terminal input without touching a real run.
        import pty
        master, slave = pty.openpty()
        try:
            process = subprocess.Popen([sys.executable, str(ROOT / 'tools/play.py')],
                                       stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            os.close(slave)
            slave = None
            os.write(master, b'2\n\ncancel\n')
            out, err = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 1, err)
            self.assertEqual(out, '')
            self.assertIn('Cancelled', err)
        finally:
            os.close(master)
            if slave is not None:
                os.close(slave)


if __name__ == '__main__':
    unittest.main()

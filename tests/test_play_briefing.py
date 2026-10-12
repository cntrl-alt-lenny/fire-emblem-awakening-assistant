"""Presentation/context controls; these tests do not certify gameplay facts."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import map_info
from play_briefing import briefing, render, _value


def cli(*args):
    return subprocess.run([sys.executable, str(ROOT / 'tools/play_briefing.py'), *args],
                          text=True, capture_output=True)


def manifest(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file()}


class BriefingTests(unittest.TestCase):
    def test_baseline_concise_but_complete(self):
        result = briefing(7, 'Hard', 5, 'player')
        text = render(result)
        self.assertLessEqual(len(text.splitlines()), 30)
        self.assertIn('Current: player phase 5 -> target: enemy phase 5', text)
        for fragment in ['Western map edge', 'count: 3', 'level: 7', 'steel_axe',
                         'Flying enemies cross', 'can_kill_on_spawn: yes',
                         'scripted phase/exceptions uncertain',
                         'no fixed match is not no spawn',
                         'Roster/positions/stats/forges/skills incomplete', 'skills: UNKNOWN']:
            self.assertIn(fragment, text)
        self.assertEqual(text, render(result))

    def test_all_maps_retain_all_claim_values_notes_confidence_and_sources(self):
        # Full information must preserve the complete map_info contract, even
        # a long conflicted note. No line budget is allowed to discard a claim.
        for m in map_info.load()[0]:
            for phase in ['player', 'enemy']:
                with self.subTest(chapter=m['chapter_id'], phase=phase):
                    raw = map_info.query(m['chapter_id'], 'hard', 5, phase, 'Full information')
                    result = briefing(m['chapter_id'], 'hard', 5, phase, 'Full information')
                    self.assertEqual(result, raw)
                    text = render(result, provenance=True)
                    for c in raw['known_verified_supported'] + raw['uncertain_partial_conflicted_unknown']:
                        self.assertIn('[' + c['confidence'] + ']', text)
                        self.assertIn(_value(c['value']), text)
                        if c['notes']:
                            self.assertIn(_value(c['notes']), text)
                        for source in c['source_ids']:
                            self.assertIn(source, text)

    def test_fixed_turn_and_phase_controls(self):
        for chapter, expected in [(7, {5}), (10, {6}), (16, {4, 5, 6})]:
            for target in range(1, 10):
                for turn, phase in [(target, 'player')] + ([(target - 1, 'enemy')] if target > 1 else []):
                    with self.subTest(chapter=chapter, target=target, phase=phase):
                        q = briefing(chapter, 'hard', turn, phase)
                        self.assertEqual(q['target_enemy_phase_turn'], target)
                        self.assertEqual(bool(q['candidate_reinforcements']), target in expected)
                        text = render(q)
                        self.assertFalse(q['schedule_complete'])
                        self.assertFalse(q['safe_to_conclude_no_reinforcements'])
                        if target not in expected:
                            self.assertIn('does not establish no arrivals', text)

    def test_chapter11_family_is_candidate_not_recurrence(self):
        for target in [1, 2, 3, 4, 5, 99]:
            for turn, phase in [(target, 'player')] + ([(target - 1, 'enemy')] if target > 1 else []):
                q = briefing(11, 'hard', turn, phase)
                ids = {w['id'] for w in q['candidate_reinforcements']}
                self.assertEqual('hard_chapter_11_t3_forts' in ids, target >= 3)
                self.assertEqual('hard_chapter_11_t4_nw' in ids, target == 4)
                text = render(q)
                self.assertIn('not predictions', text)
                if target >= 3:
                    for part in ['subsequent timing unresolved', 'not a prediction of arrivals on every later turn',
                                 'units: UNKNOWN', 'spawn_phase: UNKNOWN']:
                        self.assertIn(part, text)

    def test_events_unknown_and_repeating_retained(self):
        for chapter in [19, 'para10', 'para14', 'endgame']:
            for turn in [1, 3, 99]:
                for phase in ['player', 'enemy']:
                    q = briefing(chapter, 'hard', turn, phase)
                    self.assertTrue(q['candidate_reinforcements'])
                    self.assertIn('not predictions', render(q))
        text = render(briefing('para10', 'hard', 99, 'player'))
        self.assertIn('Killing Holland can turn her hostile', text)
        self.assertIn('NOT a fixed turn', text)
        self.assertIn('single guide claim, precise tiles unknown', text)

    def test_conflicts_and_terrain_dangers_not_truncated(self):
        for chapter in [5, 17, 20]:
            q = briefing(chapter, 'hard', 99, 'enemy')
            text = render(q)
            self.assertIn('[CONFLICTED]', text)
            self.assertIn('UNKNOWN', text)
            for c in q['uncertain_partial_conflicted_unknown']:
                if c['confidence'] == 'CONFLICTED':
                    self.assertIn(_value(c['value']), text)
                    if c.get('notes'):
                        self.assertIn(_value(c['notes']), text)
        self.assertIn('Exact phase unknown', render(briefing(18, 'hard', 7, 'player')))
        self.assertIn('Walls', render(briefing('para16', 'hard', 7, 'player')))

    def test_absence_is_supported_not_certain_and_silence_is_unknown(self):
        for chapter in [15, 22]:
            q = briefing(chapter, 'hard', 99, 'player')
            text = render(q)
            self.assertTrue(q['absence_reasonably_supported'])
            self.assertFalse(q['safe_to_conclude_no_reinforcements'])
            self.assertIn('absence certain: no', text)
            self.assertIn('[SUPPORTED] reinforcements / Explicit reported absence', text)
        text = render(briefing(3, 'hard', 99, 'player'))
        self.assertIn('Arrival status: unknown', text)
        self.assertIn('Silence does not establish absence', text)

    def test_no_spoilers_in_every_output_mode(self):
        for chapter in [7, 17, 'para10']:
            for option in [[], ['--provenance'], ['--details']]:
                p = cli('--chapter', str(chapter), '--difficulty', 'hard', '--turn', '5',
                        '--phase', 'player', '--spoilers', 'No spoilers', *option)
                self.assertEqual(p.returncode, 0, p.stderr)
                for leak in ['Cordelia', 'Vasto', 'Holland', 'Severa', 'Say', 'candidate_reinforcements',
                             'source_ids', 'p2_guide', 'beginning', 'can_attack', 'immediate', 'SUPPORTED']:
                    self.assertNotIn(leak, p.stdout)
                self.assertIn('incomplete', p.stdout)
                self.assertIn('withheld', p.stdout)

    def test_tactical_cross_map_references_abridged_full_original_retained(self):
        for chapter, future in [(4, 'Chapter 5'), (15, 'Chapter 16')]:
            tactical = briefing(chapter, 'hard', 5, 'player')
            for text in [render(tactical), render(tactical, True), json.dumps(tactical)]:
                self.assertNotIn(future, text)
                self.assertIn('another map', text)
                self.assertIn('abridges other-map references', text)
            full = briefing(chapter, 'hard', 5, 'player', 'Full information')
            self.assertIn(future, json.dumps(full))
        text = render(briefing(7, 'hard', 5, 'player'), True)
        for leak in ['Gangrel', 'Tiki', 'hard_chapter_16', 'Chapter 11']:
            self.assertNotIn(leak, text)

    def test_query_inputs_and_result_are_not_mutated(self):
        original = map_info.query(7, 'hard', 5, 'player')
        before = copy.deepcopy(original)
        with patch('play_briefing.map_info.query', return_value=original):
            q = briefing(7, 'hard', 5, 'player')
            render(q, True)
            self.assertEqual(original, before)
            self.assertIsNot(q, original)

    def test_context_refusals_cli_do_not_emit_tactical_output(self):
        valid = ['--chapter', '7', '--difficulty', 'hard', '--turn', '5', '--phase', 'player']
        cases = [[], ['--chapter', '7'], valid[:-2],
                 ['--chapter', '7', '--difficulty', 'hard', '--phase', 'player']]
        for difficulty in ['normal', 'lunatic', 'Lunatic+', 'bogus']:
            cases.append([x if x != 'hard' else difficulty for x in valid])
        for chapter in ['premonition', 'para18', 'DLC', 'nonsense']:
            cases.append([x if x != '7' else chapter for x in valid])
        for turn in ['0', '-1', 'abc']:
            cases.append([x if x != '5' else turn for x in valid])
        for args in cases:
            p = cli(*args)
            self.assertEqual(p.returncode, 2, args)
            self.assertEqual(p.stdout, '', args)
            self.assertNotIn('Traceback', p.stderr)
        for bad in [True, [], {}, None, 0, 1.5, '5']:
            with self.assertRaises(ValueError):
                briefing(7, 'hard', bad, 'player')


class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'synthetic.json'
        self.run = {'chapter': 'Chapter 7', 'turn': 5, 'difficulty': 'Hard', 'mode': 'Classic',
                    'spoiler_mode': 'No spoilers', 'events': [{'synthetic': True}],
                    'units': {'synthetic': {'stats_basis': 'raw', 'stats': None, 'alive': False}}}
        self.write()

    def write(self):
        self.path.write_text(json.dumps(self.run) + '\n', encoding='utf-8')

    def test_state_aliases_and_explicit_spoiler_override(self):
        q = briefing('7', 'hard', 5, 'player', state=self.path)
        self.assertNotIn('candidate_reinforcements', q)
        q = briefing(phase='player', spoilers='Tactical spoilers', state=self.path)
        self.assertIn('candidate_reinforcements', q)
        self.assertEqual(q['chapter_id'], 'chapter_7')
        self.run['chapter'] = 'paralogue_10'
        self.write()
        self.assertEqual(briefing('para10', phase='enemy', state=self.path)['chapter_id'], 'paralogue_10')

    def test_context_mismatch_and_missing_phase_refuse(self):
        for kwargs in [{'chapter': '8'}, {'turn': 6}, {'difficulty': 'normal'}, {'phase': None}]:
            args = dict(phase='player', state=self.path)
            args.update(kwargs)
            with self.assertRaises(ValueError):
                briefing(**args)
        self.run['phase'] = 'enemy'
        self.write()
        p = cli('--state', str(self.path))
        self.assertEqual(p.returncode, 2)
        self.assertIn('phase', p.stderr)

    def test_malformed_missing_and_unknown_state_refuse(self):
        valid = copy.deepcopy(self.run)
        for key, value in [('chapter', []), ('chapter', True), ('turn', True), ('turn', '5'),
                           ('difficulty', 'Lunatic'), ('difficulty', {}), ('mode', 'Casual'),
                           ('mode', None), ('spoiler_mode', 'bogus'), ('spoiler_mode', [])]:
            self.run = dict(valid, **{key: value})
            self.write()
            p = cli('--state', str(self.path), '--phase', 'player')
            self.assertEqual(p.returncode, 2, (key, value, p.stderr))
            self.assertEqual(p.stdout, '')
            self.assertNotIn('Traceback', p.stderr)
        for value in ['{', '[]', 'null', 'true']:
            self.path.write_text(value)
            self.assertEqual(cli('--state', str(self.path), '--phase', 'player').returncode, 2)
        self.path.write_bytes(b'\xff')
        self.assertEqual(cli('--state', str(self.path), '--phase', 'player').returncode, 2)
        self.path.unlink()
        self.assertEqual(cli('--state', str(self.path), '--phase', 'player').returncode, 2)
        self.assertFalse(self.path.exists())
        for key in ['chapter', 'turn', 'difficulty']:
            self.run = dict(valid, **{key: None})
            self.write()
            with self.assertRaises(ValueError):
                briefing(phase='player', state=self.path)

    def test_read_only_bytes_files_and_canonical_inputs(self):
        before = manifest(Path(self.temp.name))
        data = manifest(ROOT / 'data')
        # No real run is opened: this fixture includes a death/history marker
        # and nonsensical stats, neither of which is consulted or changed.
        for extra in [[], ['--details'], ['--provenance'], ['--spoilers', 'Tactical spoilers'], ['--turn', '6']]:
            p = cli('--state', str(self.path), '--phase', 'player', *extra)
            self.assertIn(p.returncode, [0, 2])
            self.assertEqual(manifest(Path(self.temp.name)), before)
            self.assertEqual(manifest(ROOT / 'data'), data)
        self.assertEqual(json.loads(self.path.read_text()), self.run)


if __name__ == '__main__':
    unittest.main()

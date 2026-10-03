"""Inventory attribution, uncertainty and authoring round-trip regressions."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from map_info import query


def chapter17_waves(path):
    data = json.loads(path.read_text())
    rows = data['records'] if 'records' in data else next(
        m for m in data['maps'] if m['id'] == 'chapter_17')['waves']
    return {w['id']: w for w in rows if w['chapter_id'] == 'chapter_17'}


class Chapter17ProvenanceTests(unittest.TestCase):
    def test_inventory_attribution_and_unresolved_central(self):
        waves = chapter17_waves(ROOT / 'data/chapters/hard_reinforcements.json')
        for suffix in ('first', 'second'):
            units = waves['hard_chapter_17_' + suffix]['units']
            self.assertEqual(units['source_ids'], ['hr_fandom17'])
            self.assertEqual(units['confidence'], 'SUPPORTED')
            self.assertEqual({u['class_id']: (u['count'], u['equipment'])
                              for u in units['value']}, {
                'hero': (2, ['silver_sword']), 'war_monk': (1, ['silver_axe']),
                'sniper': (1, ['silver_bow'])})
            self.assertIn('single-source', units['notes'])
        units = waves['hard_chapter_17_central']['units']
        self.assertIsNone(units['value'])
        self.assertEqual(units['confidence'], 'CONFLICTED')
        self.assertEqual(units['source_ids'], ['hr_fandom17'])
        self.assertIn('Inherited six-unit alternative', units['notes'])
        self.assertIn('indexed two-unit alternative', units['notes'])

    def test_query_does_not_promote_central_inventory(self):
        for turn, phase in ((8, 'player'), (8, 'enemy'), (9, 'player'), (10, 'player')):
            with self.subTest(turn=turn, phase=phase):
                result = query(17, turn=turn, phase=phase)
                central = next(w for w in result['candidate_reinforcements']
                               if w['id'] == 'hard_chapter_17_central')
                self.assertIsNone(central['units']['value'])
                self.assertFalse(any(r['label'] == 'hard_chapter_17_central:units'
                                     for r in result['known_verified_supported']))
                self.assertTrue(any(r['label'] == 'hard_chapter_17_central:units'
                                    and r['confidence'] == 'CONFLICTED'
                                    for r in result['uncertain_partial_conflicted_unknown']))
                self.assertEqual(len(result['candidate_reinforcements']), 3)
                self.assertFalse(result['safe_to_conclude_no_reinforcements'])
                for wave in result['candidate_reinforcements']:
                    self.assertIsNone(wave['timing']['value']['turns'])
                    self.assertEqual(wave['spawn_phase']['confidence'], 'UNKNOWN')

    def test_fresh_authoring_preserves_inventory_notes_and_claims(self):
        # Execute the real author in an isolated input tree; never touch a run.
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for relative in ('data/sources.json', 'data/chapters/chapters.json',
                             'data/chapters/reinforcements.json',
                             'research/hard_verification/additional_sources.json',
                             'research/hard_verification/author_review.py'):
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, destination)
            subprocess.run([sys.executable, str(target / 'research/hard_verification/author_review.py')],
                           cwd=target, check=True, capture_output=True, text=True)
            generated = chapter17_waves(target / 'research/hard_verification/reviewed.json')
            canonical = chapter17_waves(ROOT / 'data/chapters/hard_reinforcements.json')
            for key in canonical:
                self.assertEqual(generated[key]['units'], canonical[key]['units'])
                self.assertEqual(generated[key]['units']['source_ids'], ['hr_fandom17'])
            self.assertIsNone(generated['hard_chapter_17_central']['units']['value'])


if __name__ == '__main__':
    unittest.main()

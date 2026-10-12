"""Synthetic direct-boundary probes; never open or mutate a player run."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import tactical_combat as gate
from common import lookup


def battle():
    return json.loads((ROOT / 'examples/battle.json').read_text())


def controls():
    base = battle()
    yield 'catalog', base
    for name in ('custom', 'forged'):
        p = battle()
        for side in ('attacker', 'defender'):
            w = lookup('weapons', p[side]['weapon'])
            p[side]['weapon'] = {k: copy.deepcopy(v) for k, v in w.items() if k in gate.WEAPON_FIELDS}
            if name == 'forged':
                p[side]['weapon']['might'] += 2
                p[side]['weapon']['hit'] += 5
                p[side]['weapon']['crit'] += 1
        yield name, p
    p = battle()
    p['defender'].update(weapon=None, weapon_state='unequipped', remaining_uses=0)
    yield 'unarmed', p
    for skill, context in [('lucky_seven', {'turn': 2}), ('indoor_fighter', {'outdoors': False}),
                           ('odd_rhythm', {'turn': 3}), ('vantage', {}), ('ignis', {})]:
        p = battle()
        p['attacker']['skills'] = [skill]
        p['defender']['skills'] = ['hit_rate_plus_10']
        p['context'].update(context)
        yield skill, p
    p = battle()
    p['attacker'].update(alive=True, id='observed_a', name='Observed A')
    p['context'].update(turn=1, outdoors=True)
    yield 'optional', p


class DuelBoundary(unittest.TestCase):
    def unknown(self, payload):
        before = copy.deepcopy(payload)
        r = gate.assess(payload)
        self.assertEqual(payload, before)
        self.assertEqual(r['status'], 'UNKNOWN', r)
        self.assertIsNone(r['outcome'])
        self.assertIs(r['safe_to_claim_survival'], False)
        self.assertTrue(r.get('reason') or r.get('missing'))
        self.assertFalse(set(r) & {'forecast', 'states', 'attacker_death_probability',
                                  'defender_death_probability', 'worst_attacker_hp', 'worst_defender_hp'})
        return r

    def test_baseline_full_output_equality(self):
        source = subprocess.check_output(['git', 'show',
            'ec3bceca1d70a4da240a490601602e97c2466de2:tools/tactical_combat.py'], cwd=ROOT, text=True)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'baseline.py'; path.write_text(source)
            spec = importlib.util.spec_from_file_location('baseline_duel', path)
            baseline = importlib.util.module_from_spec(spec); spec.loader.exec_module(baseline)
            for name, p in controls():
                with self.subTest(name=name):
                    before = copy.deepcopy(p)
                    expected = baseline.assess(p)
                    self.assertIsNotNone(expected['outcome'], expected)
                    self.assertEqual(gate.assess(p), expected)
                    self.assertEqual(p, before)

    def test_independent_deterministic_control(self):
        p = battle()
        p['defender'].update(weapon=None, weapon_state='unequipped', remaining_uses=0)
        for side in ('attacker', 'defender'):
            p[side]['stats'].update(hp=30, str=0, mag=0, skl=0, spd=0, lck=0, def_=0)
            del p[side]['stats']['def_']
            p[side]['stats']['def'] = 0
            p[side]['current_hp'] = 30
        p['attacker']['weapon'] = {'weapon_type': 'tome', 'damage_type': 'magical',
            'rank': 'E', 'might': 6, 'hit': 100, 'crit': 0, 'range': 1,
            'effect': '–', 'brave': False, 'effectiveness': []}
        p['defender']['stats']['res'] = 0
        r = gate.assess(p)
        self.assertEqual(r['forecast']['attacker']['damage'], 6)
        self.assertEqual(r['worst_attacker_hp'], 30)
        self.assertEqual(r['worst_defender_hp'], 24)
        self.assertEqual(r['attacker_death_probability'], 0)
        self.assertEqual(r['defender_death_probability'], 0)
        self.assertEqual(r['status'], 'NO_MODELED_DEATH_IN_THIS_DUEL')
        p['attacker']['weapon']['might'] = 30
        r = gate.assess(p)
        self.assertEqual(r['status'], 'LETHAL')
        self.assertEqual(r['defender_death_probability'], 1)

    def test_both_side_unknown_matrix(self):
        mutations = [('alive', x) for x in ('?', 'false', False, None, 0, 1, [], {})]
        mutations += [('forge', x) for x in ({}, [], None, '', '?', {'might': None},
                                            {'might': 2}, '++', False, 0)]
        mutations += [('status_effects', x) for x in (['unknown'], [], None)]
        mutations += [('weapon_state', x) for x in (None, '', '?', True, {})]
        mutations += [('remaining_uses', x) for x in (None, True, 2.0, -1, '40')]
        mutations += [('weapon_rank', x) for x in ('', 'ED', 'Z', None, True, [])]
        mutations += [('id', x) for x in (None, '?', '', 1)]
        mutations += [('name', x) for x in (False, {}, [])]
        for side in ('attacker', 'defender'):
            for field, value in mutations:
                with self.subTest(side=side, field=field, value=value):
                    p = battle(); p[side][field] = value; self.unknown(p)
            for field in ('stats', 'terrain', 'combat_bonuses'):
                p = battle(); p[side][field]['unknown_effect'] = 0; self.unknown(p)
            for stat in gate.STATS:
                for value in (True, 1.0, -1, None, '?'):
                    p = battle(); p[side]['stats'][stat] = value; self.unknown(p)
                p = battle(); del p[side]['stats'][stat]; self.unknown(p)
            for value in (True, 1.0, 0, -1, 999, None):
                p = battle(); p[side]['current_hp'] = value; self.unknown(p)
            for field in ('terrain', 'combat_bonuses'):
                key = 'def' if field == 'terrain' else 'attack'
                for value in (True, 1.0, None, '?'):
                    p = battle(); p[side][field][key] = value; self.unknown(p)

    def test_weapons_and_nested_effects(self):
        for side in ('attacker', 'defender'):
            p = dict(controls())['custom']
            w = p[side]['weapon']
            for field, values in [('range', (True, 1.0, 0, '0', '2-1', '?', [], None)),
                                  ('rank', ('', 'ED', '?', None, True)),
                                  ('might', (True, 1.0, -1, None)),
                                  ('effect', (None, 'unknown', 'HP drain')),
                                  ('brave', (None, 1, 'false')),
                                  ('effectiveness', (None, 'flying', ['unknown']))]:
                for value in values:
                    q = copy.deepcopy(p); q[side]['weapon'][field] = value; self.unknown(q)
            for field in gate.WEAPON_FIELDS - {'id', 'name'}:
                q = copy.deepcopy(p); del q[side]['weapon'][field]; self.unknown(q)
            for field in ('forge', 'status_effects', 'skills', 'source_ids', 'durability'):
                q = copy.deepcopy(p); q[side]['weapon'][field] = []; self.unknown(q)
            q = copy.deepcopy(p); q[side]['weapon']['name'] = None; self.unknown(q)
            self.assertEqual(gate.known_weapon(p[side], side), w)
        # Catalog metadata is resolved internally and never treated as caller effects.
        self.assertIsNotNone(gate.assess(battle())['outcome'])

    def test_context_root_and_existing_refusals(self):
        for field, values in [('distance', (True, 1.0, None, 0, -1, '1')),
                              ('turn', (True, 1.0, None, 0, -1, '1')),
                              ('outdoors', (1, 0, 'false', None, [])),
                              ('weather', ('unknown',))]:
            for value in values:
                p = battle(); p['context'][field] = value; self.unknown(p)
        for field in ('status_effects', 'roster', 'events', 'history', 'state'):
            p = battle(); p[field] = []; self.unknown(p)
        p = battle(); p['note'] = {}; self.unknown(p)
        p = battle(); p['partners'] = ['someone']; self.unknown(p)
        for side in ('attacker', 'defender'):
            for skills in (['counter'], ['dragonskin'], ['aether'], ['luna', 'ignis'], ['pavise', 'aegis']):
                p = battle(); p[side]['skills'] = skills; self.unknown(p)
            p = battle(); p[side]['remaining_uses'] = 0; self.unknown(p)
        p = battle(); p['support_state'] = 'paired'; p['partners'] = ['other']; self.unknown(p)

    def cli(self, path):
        return subprocess.run([sys.executable, str(ROOT/'tools/tactical_combat.py'), str(path)],
                              capture_output=True, text=True)

    def test_cli_malformed_and_semantic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'battle.json'
            for text in ('{', '{"attacker":1,"attacker":2}', '{"context":{"distance":1,"distance":2}}',
                         '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
                path.write_text(text); r = self.cli(path)
                self.assertEqual(r.returncode, 2); self.assertFalse(r.stdout)
                self.assertNotIn('Traceback', r.stderr)
            path.write_bytes(b'\xff'); self.assertEqual(self.cli(path).returncode, 2)
            self.assertEqual(self.cli(Path(tmp)/'absent.json').returncode, 2)
            self.assertEqual(self.cli(Path(tmp)).returncode, 2)
            for side in ('attacker', 'defender'):
                for field, value in [('alive', '?'), ('forge', {}), ('status_effects', ['unknown'])]:
                    p = battle(); p[side][field] = value; path.write_text(json.dumps(p))
                    r = self.cli(path); self.assertEqual(r.returncode, 0)
                    self.assertEqual(json.loads(r.stdout), gate.assess(p))
            for name, p in controls():
                path.write_text(json.dumps(p)); r = self.cli(path)
                self.assertEqual(r.returncode, 0); self.assertEqual(json.loads(r.stdout), gate.assess(p))

    def test_run_paths_refused_before_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root/'state').mkdir()
            run = root/'state/current_run.json'; run.write_text('private sentinel')
            sym = root/'alias.json'; sym.symlink_to(run)
            hard = root/'hard.json'; os.link(run, hard)
            with patch.object(gate, 'ROOT', root), patch.object(Path, 'read_text', side_effect=AssertionError('opened')):
                for path in (run, sym, hard, root/'current_run.json'):
                    with self.assertRaises(ValueError): gate.load_battle(path)
            self.assertEqual(run.read_text(), 'private sentinel')
        self.unknown({'roster': [], 'events': [], 'history': []})


if __name__ == '__main__':
    unittest.main()

"""Regressions for the strict live boundary, not new gameplay certification."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from common import ROOT, lookup
from tactical_combat import assess
from test_hard import battle


def lethal(side):
    p = battle()
    killer = 'defender' if side == 'attacker' else 'attacker'
    p[killer]['skills'] = ['hawkeye']
    p[killer]['weapon'].update(brave=True, effect='2 consecutive attacks')
    p[side]['current_hp'] = 20
    if side == 'attacker':p[killer]['skills'].append('vantage_plus')
    return p


class CombatGateTests(unittest.TestCase):
    def unknown(self, p, diagnostic=None):
        r = assess(p)
        self.assertEqual(r['status'], 'UNKNOWN')
        self.assertIsNone(r['outcome'])
        self.assertFalse(r['safe_to_claim_survival'])
        if diagnostic:self.assertIn(diagnostic, r.get('reason', str(r.get('missing'))))

    def test_missing_properties_both_sides(self):
        for side in ('attacker', 'defender'):
            for field in ('effect', 'brave', 'effectiveness'):
                with self.subTest(side=side, field=field):
                    p = battle();del p[side]['weapon'][field]
                    self.unknown(p, side + ':weapon.' + field)

    def test_null_and_malformed_properties_both_sides(self):
        bad = {'effect':[None, '', ' ', 'UNKNOWN', [], {}, False],
               'brave':[None, 0, 1, 'false', [], {}],
               'effectiveness':[None, '', 'flying', {}, [None], [[]], ['unknown']]}
        for side in ('attacker', 'defender'):
            for field, values in bad.items():
                for value in values:
                    with self.subTest(side=side, field=field, value=value):
                        p=battle();p[side]['weapon'][field]=value
                        self.unknown(p, side + ':weapon.' + field)

    def test_explicit_absence_and_input_unchanged(self):
        p=battle();before=copy.deepcopy(p)
        r=assess(p)
        self.assertEqual(r['status'], 'NO_MODELED_DEATH_IN_THIS_DUEL')
        self.assertEqual(r['at_risk_sides'], [])
        self.assertEqual(r['certain_death_sides'], [])
        self.assertEqual(p,before)

    def test_weapon_presence_both_sides(self):
        for side in ('attacker','defender'):
            for value in (None, '', {}, [], False):
                with self.subTest(side=side,value=value):
                    p=battle();p[side]['weapon']=value;self.unknown(p, side+':weapon')
        p=battle();del p['defender']['weapon'];self.unknown(p,'defender:weapon')

    def test_explicit_unequipped_defender(self):
        p=battle();p['defender'].update(weapon=None,weapon_state='unequipped',remaining_uses=0)
        r=assess(p)
        self.assertEqual(r['status'],'NO_MODELED_DEATH_IN_THIS_DUEL')
        self.assertFalse(r['forecast']['defender']['can_attack'])
        self.assertEqual(r['outcome']['order'],['a'])
        for side in ('attacker','defender'):
            p=battle();p[side]['weapon_state']='unequipped';self.unknown(p,side+':weapon')
        p=battle();p['attacker'].update(weapon=None,weapon_state='unequipped');self.unknown(p,'attacker:weapon')

    def test_canonical_ids_and_incomplete_resolution(self):
        for side in ('attacker','defender'):
            p=battle();p[side].update(weapon='iron_sword',weapon_rank='D')
            self.assertIsNotNone(assess(p)['outcome'])
            p[side]['weapon']='not_a_weapon';self.unknown(p,side+':weapon')
            for field in ('effect','brave','effectiveness'):
                p[side]['weapon']='iron_sword'
                record=copy.deepcopy(lookup('weapons','iron_sword'));del record[field]
                with patch('tactical_combat.lookup',return_value=record):
                    self.unknown(p,side+':weapon.'+field)

    def test_brave_contradictions_both_sides(self):
        for side in ('attacker','defender'):
            for effect,brave in [('2 consecutive attacks',False),('–',True),('Str +5',True)]:
                p=battle();p[side]['weapon'].update(effect=effect,brave=brave)
                self.unknown(p,side+':weapon.brave')

    def test_forged_values_and_ambiguous_markers(self):
        for side in ('attacker','defender'):
            p=battle();p[side]['weapon'].update(might=8,hit=110,crit=3)
            self.assertIsNotNone(assess(p)['outcome'])
            for forge in ('+', '++', {'might':3}):
                p[side]['forge']=forge;self.unknown(p,'forge')

    def test_certain_death_both_sides(self):
        for side in ('attacker','defender'):
            with self.subTest(side=side):
                r=assess(lethal(side))
                self.assertEqual(r['status'],'LETHAL')
                self.assertEqual(r['certain_death_sides'],[side])
                self.assertEqual(r['at_risk_sides'],[side])
                self.assertEqual(r[side+'_death_probability'],1)
                self.assertEqual(r['worst_'+side+'_hp'],0)
                self.assertFalse(r['safe_to_claim_map_survival'])

    def test_possible_death_both_sides(self):
        for side in ('attacker','defender'):
            p=battle();other='defender' if side=='attacker' else 'attacker'
            p[side]['current_hp']=20;p[other]['weapon']['crit']=1
            r=assess(p)
            self.assertEqual(r['status'],'POTENTIALLY_LETHAL')
            self.assertIn(side,r['at_risk_sides'])
            self.assertEqual(r['certain_death_sides'],[])
            self.assertGreater(r[side+'_death_probability'],0)
            self.assertLess(r[side+'_death_probability'],1)

    def test_near_one_probability_not_rounded(self):
        r=assess(battle())['forecast']
        r['outcome']['defender_death_probability']=0.9999999999999999
        with patch('tactical_combat.calculate',return_value=r):
            result=assess(battle())
        self.assertEqual(result['status'],'POTENTIALLY_LETHAL')
        self.assertEqual(result['certain_death_sides'],[])

    def test_existing_refusals(self):
        for field in ('partners','support_state'):
            for action in ('missing','null'):
                p=battle()
                if action=='missing':del p[field]
                else:p[field]=None
                self.unknown(p)
        for state in ('adjacent','paired'):
            p=battle();p['support_state']=state;self.unknown(p)
        for side in ('attacker','defender'):
            for skills in (['counter'],['dragonskin'],['aether'],['luna','sol'],['pavise','aegis']):
                p=battle();p[side]['skills']=skills
                if skills==['luna','sol']:p[side]['stats']['skl']=10
                self.unknown(p)
            p=battle();p[side]['weapon']['effect']='Drains HP';self.unknown(p)
            p=battle();p[side].update(weapon='nosferatu',weapon_rank='D');self.unknown(p)
            p=battle();p[side]['remaining_uses']=0;self.unknown(p,'break')

    def test_public_cli(self):
        cases=[(battle(),'NO_MODELED_DEATH_IN_THIS_DUEL'),(lethal('attacker'),'LETHAL'),(lethal('defender'),'LETHAL')]
        missing=battle();del missing['defender']['weapon']['effect'];cases.append((missing,'UNKNOWN'))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'battle.json'
            for p,status in cases:
                path.write_text(json.dumps(p))
                r=subprocess.run([sys.executable,str(ROOT/'tools/tactical_combat.py'),str(path)],capture_output=True,text=True)
                self.assertEqual(r.returncode,0,r.stderr)
                self.assertEqual(json.loads(r.stdout)['status'],status)


if __name__=='__main__':unittest.main()

import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from common import ROOT,STATS,lookup
from combat_calculator import calculate
from experience import battle,staff
from healing import heal
from tactical_query import query
from enemy_phase import evaluate

def unit(speed=10):
 return {'stats':dict(zip(STATS,[40,10,10,0,speed,0,5,5])),'weapon':{'id':'test_sword','weapon_type':'sword','damage_type':'physical','might':5,'hit':100,'crit':0,'range':'1','rank':'E','effect':'–','brave':False},'weapon_rank':'E','skills':['hawkeye']}
class ProcTests(unittest.TestCase):
 def test_vantage_half_boundary(self):
  a,b=unit(),unit();b['skills']+=['vantage'];b['current_hp']=20
  self.assertEqual(calculate({'attacker':a,'defender':b})['outcome']['order'],['b','a'])
  b['current_hp']=21;self.assertEqual(calculate({'attacker':a,'defender':b})['outcome']['order'],['a','b'])
 def test_vantage_range_and_lethal_stop(self):
  a,b=unit(),unit();a['current_hp']=1;b['skills']+=['vantage_plus']
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['attacker_death_probability'],1);self.assertEqual(r['outcome']['expected_defender_hp'],40)
 def test_luna_plus_floor_and_crit(self):
  a,b=unit(),unit();a['skills']+=['luna_plus'];a['weapon']['crit']=100;b['weapon']=None
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['expected_defender_hp'],1) # (15-floor(5/2))*3=39
 def test_ignis_before_crit(self):
  a,b=unit(),unit();a['skills']+=['ignis'];a['stats']['skl']=100;a['weapon']['crit']=100;b['stats']['hp']=100;b['weapon']=None
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['expected_defender_hp'],55) # (15+5-5)*3
 def test_pavise_after_crit(self):
  a,b=unit(),unit();a['weapon']['crit']=100;b['skills']=['pavise_plus'];b['stats']['def']=4;b['weapon']=None
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['expected_defender_hp'],24) # floor(11*3/2)=16
 def test_dragonstone_uses_aegis(self):
  a,b=unit(),unit();a['weapon']=lookup('weapons','dragonstone');b['weapon']=None;b['skills']=['aegis_plus'];r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['expected_defender_hp'],40-r['attacker']['damage']//2)
 def test_miracle_only_above_one_hp(self):
  a,b=unit(),unit();a['stats']['str']=100;b['skills']=['miracle'];b['stats']['lck']=100;b['weapon']=None
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['expected_defender_hp'],1)
  b['current_hp']=1;self.assertEqual(calculate({'attacker':a,'defender':b})['outcome']['defender_death_probability'],1)
 def test_miracle_brave_can_still_die(self):
  a,b=unit(),unit();a['stats']['str']=100;a['weapon']['brave']=True;b['skills']=['miracle'];b['stats']['lck']=100;b['weapon']=None
  self.assertEqual(calculate({'attacker':a,'defender':b})['outcome']['defender_death_probability'],1)
 def test_wrath_raw_negative_crit(self):
  a,b=unit(),unit();a['skills']+=['wrath'];a['current_hp']=20;b['stats']['lck']=15;b['weapon']=None
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['attacker']['crit_percent'],5);self.assertAlmostEqual(r['outcome']['expected_defender_hp'],29)
 def test_vengeance_rechecks_after_damage(self):
  a,b=unit(15),unit();a['skills']+=['vengeance'];a['stats']['skl']=50;b['stats']['hp']=100
  r=calculate({'attacker':a,'defender':b});self.assertAlmostEqual(sum(x['probability'] for x in r['outcome']['states']),1);self.assertLess(r['outcome']['minimum_possible_defender_hp'],80)
 def test_offensive_proc_priority(self):
  a,b=unit(),unit();a['skills']+=['ignis','vengeance'];a['stats']['skl']=100;a['current_hp']=10;b['weapon']=None;b['stats']['hp']=100
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['expected_defender_hp'],70) # Ignis 15 damage, crit50% =>30; never stacks Vengeance
 def test_sol_heals_non_overkill(self):
  a,b=unit(),unit();a['skills']+=['sol'];a['stats']['skl']=100;a['current_hp']=20;b['stats']['hp']=100;b['weapon']=None
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['expected_attacker_hp'],30) # crit50%: heal5 or15
 def test_ambiguous_combinations_refuse(self):
  a,b=unit(),unit();b['skills']=['pavise','miracle']
  with self.assertRaises(ValueError):calculate({'attacker':a,'defender':b})
  b=unit();a['skills']+=['luna'];b['terrain']={'def':1}
  with self.assertRaises(ValueError):calculate({'attacker':a,'defender':b})
 def test_brave_tome_import(self):
  self.assertTrue(lookup('weapons','Celica’s Gale')['brave']);self.assertTrue(lookup('weapons','Waste')['brave'])
 def test_player_durability_whole_enemy_phase(self):
  p=unit();p['remaining_uses']=1
  with self.assertRaises(ValueError):evaluate({'player':p,'enemies':[{'unit':unit()},{'unit':unit()}]})
class MoreSafetyTests(unittest.TestCase):
 def test_invalid_damage_category_refuses(self):
  a,b=unit(),unit();a['weapon']['damage_type']='magic'
  with self.assertRaises(ValueError):calculate({'attacker':a,'defender':b})
 def test_invalid_or_unknown_bonus_refuses(self):
  for bonus in ({'attack':1.5},{'unknown_effect':10}):
   a,b=unit(),unit();a['combat_bonuses']=bonus
   with self.assertRaises(ValueError):calculate({'attacker':a,'defender':b})
 def test_multiple_probabilistic_offensive_procs_refuse(self):
  a,b=unit(),unit();a['skills']+=['ignis','luna'];a['stats']['skl']=25
  with self.assertRaises(ValueError):calculate({'attacker':a,'defender':b})
 def test_weapon_combined_stat_bonus(self):
  self.assertEqual(lookup('weapons','Micaiah’s Pyre')['stat_bonuses'],{'def':2,'res':2})
  self.assertEqual(lookup('weapons','Mjolnir')['stat_bonuses']['skl'],5)
 def test_paired_preview_is_explicitly_partial(self):
  from paired_forecast import preview
  p={'leader':unit(),'partner':{**unit(),'class_id':'great_knight'},'partner_raw_stats':unit()['stats'],'enemy':unit(),'support_rank':'C','leader_stats_include_pair_up':False}
  r=preview(p);self.assertEqual(r['full_paired_outcome'],'UNKNOWN');self.assertIsNone(r['forecast']['outcome']);self.assertGreater(r['leader_effective_stats_after_pair_up']['str'],p['leader']['stats']['str'])
  p['leader_stats_include_pair_up']=True
  with self.assertRaises(ValueError):preview(p)
class ExpTests(unittest.TestCase):
 def base(self,level):return {'difficulty':'Normal','internal_level':level,'enemy_level':7,'enemy_promoted':False,'engagement_count':1,'damaged':True,'killed':True,'unit_bonus':20,'enemy_class':'cavalier','boss':False}
 def test_observed_coy_sequence(self):
  known={1:70,2:67,3:63,4:60,5:57,6:53,7:50,8:50,9:50,10:47,11:43,12:40,13:37,14:33,15:30,16:27,17:23,18:20,19:17,20:13,21:13,22:13,23:12,24:12,25:12,26:11,27:11,28:11,29:10,30:10,31:10,32:9,33:9,34:9,35:8}
  for lv,xp in known.items():
   with self.subTest(level=lv):self.assertEqual(battle(self.base(lv))['exp'],xp)
 def test_damage_and_boss(self):
  p=self.base(7);p['unit_bonus']=None;p['boss']=True;self.assertEqual(battle(p)['exp'],50);p['killed']=False;self.assertEqual(battle(p)['exp'],10);p['damaged']=False;self.assertEqual(battle(p)['exp'],0)
 def test_category_cap(self):
  p=self.base(7);p['enemy_class']='thief';self.assertEqual(battle(p)['character_bonus'],20);p['unit_bonus']=0;self.assertEqual(battle(p)['character_bonus'],0)
 def test_lunatic_sign_refusal(self):
  p=self.base(7);p['difficulty']='Lunatic';p['engagement_count']=4
  with self.assertRaises(ValueError):battle(p)
  p['allow_interpreted_lunatic_penalty']=True;self.assertEqual(battle(p)['damage_component'],9)
 def test_support_fraction_rounding_refusal(self):
  p=self.base(4);p['role']='support'
  with self.assertRaises(ValueError):battle(p)
 def test_observed_rescue_sequence(self):
  for level,xp in zip(range(26,34),[33,32,32,32,32,31,31,30]):self.assertEqual(staff({'kind':'staff','difficulty':'Normal','internal_level':level,'ordinary_unpromoted':False,'base_exp':40})['exp'],xp)
 def test_staff_exceptions_modes_and_dancer(self):
  for il in [8,11]:self.assertEqual(staff({'kind':'staff','difficulty':'Hard','internal_level':il,'ordinary_unpromoted':True,'base_exp':17})['exception'],-1)
  self.assertEqual(staff({'kind':'dance','difficulty':'Normal','internal_level':1,'ordinary_unpromoted':False})['exp'],17)
class DataSafetyTests(unittest.TestCase):
 def test_full_coverage_matrix(self):
  rs=json.loads((ROOT/'data/chapters/coverage.json').read_text())['records'];self.assertEqual(len(rs),204);self.assertEqual(len({(r['map_id'],r['difficulty']) for r in rs}),204)
 def test_missing_wave_never_means_safe(self):
  r=query('chapter_7','Hard',99);self.assertFalse(r['safe_to_conclude_no_reinforcements']);self.assertFalse(r['schedule_complete'])
 def test_next_turn_mode_separation(self):
  r=query('chapter_7','Hard',4);self.assertTrue(r['possible_reported_waves']);self.assertEqual(r['possible_reported_waves'][0]['units'][0]['count'],3);self.assertTrue(all(w['difficulty']=='Hard' for w in r['possible_reported_waves']))
  self.assertEqual(query('chapter_7','Lunatic+',4)['possible_reported_waves'],[])
 def test_event_wave_remains_candidate(self):
  r=query('paralogue_10','Hard',3);self.assertEqual(r['waves_with_unknown_timing'][0]['timing_type'],'event_triggered')
 def test_hazard_lists_unsupported_skills(self):
  from tactical_query import hazards
  e=unit();e['skills']=['counter'];r=hazards(e,unit());self.assertIn('counter',r['unsupported_combat_skills'])
 def test_no_spoilers(self):
  r=query('chapter_7','Hard',4,'No spoilers');self.assertNotIn('possible_reported_waves',r)
 def test_enemy_forges_unknown(self):
  es=json.loads((ROOT/'data/enemies/enemies.json').read_text())['records'];forged=[w for e in es for w in e['equipment'] if w['enemy_forge_marker']];self.assertTrue(forged);self.assertTrue(all(w['effective_weapon_stats']=='UNKNOWN' for w in forged))
 def test_mend_and_physic(self):
  p={'staff':'mend','magic':11,'weapon_rank':'A','skills':['healtouch'],'current_hp':10,'max_hp':40,'distance':1,'remaining_uses':1};self.assertEqual(heal(p)['hp_restored'],28)
  p.update(staff='physic',distance=5);self.assertEqual(heal(p)['hp_restored'],21)
  p['distance']=6
  with self.assertRaises(ValueError):heal(p)

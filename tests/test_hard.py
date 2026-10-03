import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from common import ROOT,STATS
from map_info import query,load
from tactical_query import query as legacy
from tactical_combat import assess
from audit_hard import audit

def unit():
 return {'stats':dict(zip(STATS,[40,10,10,0,10,0,5,5])),'current_hp':40,'weapon':{'id':'test','weapon_type':'sword','damage_type':'physical','might':5,'hit':100,'crit':0,'range':'1','rank':'E','effect':'–','brave':False},'weapon_rank':'E','skills':[],'weaknesses':[],'terrain':{},'combat_bonuses':{},'remaining_uses':50}
def battle():return {'attacker':unit(),'defender':unit(),'context':{'distance':1},'partners':[],'support_state':'none','difficulty':'Hard','mode':'Classic','stats_basis':'effective_displayed','observed_inputs_complete':True}
class HardDataTests(unittest.TestCase):
 def test_complete_campaign_inventory(self):self.assertEqual(len(load()[0]),44);self.assertTrue(audit()['passed'])
 def test_every_map_explicit_presence(self):
  for m in load()[0]:self.assertIn(m['reinforcements']['status'],['present','none_supported','none_verified','unknown'])
 def test_hard_scope(self):
  for m in load()[0]:self.assertEqual((m['difficulty'],m['mode']),('Hard','Classic'))
  for w in load()[1].values():self.assertEqual((w['difficulty'],w['mode']),('Hard','Classic'))
 def test_source_resolution(self):
  ss={s['id'] for s in json.loads((ROOT/'data/sources.json').read_text())}
  for w in load()[1].values():self.assertTrue(set(w['source_ids'])<=ss)
 def test_null_coordinates(self):self.assertTrue(all(w['coordinates']['value'] is None for w in load()[1].values()))
 def test_player_phase_same_turn(self):
  q=query(7,turn=5,phase='player');self.assertEqual(q['target_enemy_phase_turn'],5);self.assertEqual(q['candidate_reinforcements'][0]['units']['value'][0]['count'],3)
 def test_enemy_phase_following_turn(self):self.assertEqual(query(7,turn=4,phase='enemy')['target_enemy_phase_turn'],5)
 def test_phase_required(self):
  with self.assertRaises(ValueError):query(7,turn=5)
 def test_negative_turn_rejected(self):
  with self.assertRaises(ValueError):query(7,turn=0,phase='player')
 def test_other_difficulties_rejected(self):
  for d in ['normal','lunatic','Lunatic+']:
   with self.assertRaises(ValueError):query(7,d)
 def test_bonus_content_separated(self):
  for c in ['paralogue_18','premonition','champions_of_yore_1']:
   with self.assertRaises(ValueError):query(c)
 def test_chapter_alias(self):self.assertEqual(query('para10')['chapter_id'],'paralogue_10')
 def test_missing_wave_never_proves_absence(self):
  q=query(7,turn=99,phase='player');self.assertEqual(q['candidate_reinforcements'],[]);self.assertFalse(q['safe_to_conclude_no_reinforcements']);self.assertTrue(any(r['kind']=='schedule' for r in q['uncertain_partial_conflicted_unknown']))
 def test_silence_unknown(self):self.assertEqual(query('prologue')['reinforcement_status'],'unknown')
 def test_single_source_absence_exposed_not_certainty(self):
  for n in [15,22]:
   q=query(n);self.assertTrue(q['absence_reasonably_supported']);self.assertFalse(q['safe_to_conclude_no_reinforcements']);self.assertEqual(q['reinforcement_absence_confidence'],'SUPPORTED')
 def test_quarantine_old_queries(self):
  for n in [3,4,5]:self.assertEqual(legacy('chapter_15','Hard',n)['possible_reported_waves'],[])
 def test_chapter16_not_lunatic_counts(self):
  for turn,count in [(4,8),(5,4),(6,4)]:
   q=query(16,turn=turn,phase='player');self.assertEqual(sum(u['count'] for u in q['candidate_reinforcements'][0]['units']['value']),count)
 def test_chapter19_no_lunatic_turn8(self):
  for w in query(19,turn=8,phase='player')['candidate_reinforcements']:self.assertIsNone(w['timing']['value']['turns'])
 def test_event_not_fixed(self):
  q=query('para10',turn=99,phase='player');w=q['candidate_reinforcements'][0];self.assertEqual(w['timing']['value']['kind'],'event');self.assertIsNone(w['timing']['value']['turns'])
 def test_village_event_retained(self):self.assertTrue(query('para14',turn=99,phase='player')['candidate_reinforcements'])
 def test_repeat_start_unknown(self):
  w=query('endgame',turn=1,phase='player')['candidate_reinforcements'][0];self.assertIsNone(w['timing']['value']['repeat']['first_turn'])
 def test_conflicted_wave_not_known_schedule(self):
  q=query(17);self.assertTrue(any(r['confidence']=='CONFLICTED' for r in q['uncertain_partial_conflicted_unknown']));self.assertFalse(any(r['label'].endswith(':location') and 'first' in r['label'] for r in q['known_verified_supported']))
 def test_recruitment_not_vague(self):
  q=query('para10');r=next(r for r in q['known_verified_supported'] if r['kind']=='recruitment');self.assertIn('Holland',r['value'])
 def test_no_spoilers(self):
  q=query(7,spoilers='No spoilers');self.assertNotIn('candidate_reinforcements',q);self.assertNotIn('Cordelia',json.dumps(q))
 def test_no_other_map_leak(self):self.assertNotIn('hard_chapter_16',json.dumps(query(7)))
class LiveCombatSafetyTests(unittest.TestCase):
 def test_missing_partner_knowledge_refuses(self):
  p=battle();del p['partners'];self.assertEqual(assess(p)['status'],'UNKNOWN')
 def test_adjacent_support_outcome_refuses(self):
  p=battle();p['support_state']='adjacent';self.assertEqual(assess(p)['status'],'UNKNOWN')
 def test_support_state_required(self):
  p=battle();del p['support_state'];self.assertEqual(assess(p)['status'],'UNKNOWN')
 def test_null_partners_refuse(self):
  p=battle();p['partners']=None;self.assertEqual(assess(p)['status'],'UNKNOWN')
 def test_malformed_context_refuses(self):
  p=battle();p['context']=None;self.assertEqual(assess(p)['status'],'UNKNOWN')
 def test_malformed_unit_refuses(self):
  p=battle();p['attacker']=None;self.assertEqual(assess(p)['status'],'UNKNOWN')
 def test_missing_enemy_skill_inspection_refuses(self):
  p=battle();del p['attacker']['skills'];self.assertIsNone(assess(p)['outcome'])
 def test_counter_refuses(self):
  p=battle();p['defender']['skills']=['counter'];self.assertEqual(assess(p)['status'],'UNKNOWN');self.assertIn('counter',assess(p)['reason'])
 def test_unknown_enemy_forge_refuses(self):
  p=battle();p['attacker']['forge']='++';self.assertEqual(assess(p)['status'],'UNKNOWN')
 def test_paired_probability_not_certified(self):
  p=battle();p['partners']=['unknown_partner'];self.assertIsNone(assess(p)['outcome'])
 def test_crit_risk_worst_not_expected(self):
  p=battle();p['attacker']['weapon']['crit']=1;p['defender']['current_hp']=20
  r=assess(p);self.assertTrue(r['defender_can_die']);self.assertEqual(r['worst_defender_hp'],0);self.assertGreater(r['outcome']['expected_defender_hp'],0)
 def test_speed_threshold_five(self):
  p=battle();p['attacker']['stats']['spd']=14;self.assertFalse(assess(p)['forecast']['attacker']['doubles'])
  p['attacker']['stats']['spd']=15;self.assertTrue(assess(p)['forecast']['attacker']['doubles'])
 def test_brave_lethal_second_hit(self):
  p=battle();p['attacker']['weapon']['brave']=True;p['attacker']['skills']=['hawkeye'];p['defender']['current_hp']=20
  self.assertEqual(assess(p)['outcome']['defender_death_probability'],1)
 def test_vantage_can_stop_brave(self):
  p=battle();p['attacker']['current_hp']=1;p['attacker']['weapon']['brave']=True;p['defender']['current_hp']=20;p['defender']['skills']=['vantage','hawkeye']
  r=assess(p);self.assertEqual(r['outcome']['attacker_death_probability'],1);self.assertEqual(r['outcome']['expected_defender_hp'],20)
 def test_effective_damage_lethal(self):
  p=battle();p['attacker']['weapon']['effectiveness']=['flying'];p['defender']['weaknesses']=['flying'];p['defender']['current_hp']=20;p['attacker']['skills']=['hawkeye']
  r=assess(p);self.assertEqual(r['forecast']['attacker']['damage'],20);self.assertEqual(r['outcome']['defender_death_probability'],1)
 def test_never_claim_map_survival(self):self.assertFalse(assess(battle())['safe_to_claim_map_survival'])
if __name__=='__main__':unittest.main()

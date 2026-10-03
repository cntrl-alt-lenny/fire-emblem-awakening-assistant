import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from common import ROOT,STATS,lookup
from combat_calculator import calculate,true_hit,rank_bonus,triangle
from pair_up import pair_bonus,dual_bonus,dual_rates
from average_stats import project,growths,internal_level,second_seal_cumulative
from inheritance import avatar,child
from roster_tracker import initial,upsert,death,consume,mutate,class_change
from level_tracker import level_up

def unit(speed=10):
 return {'stats':dict(zip(STATS,[30,10,5,10,speed,0,5,3])),'weapon':'iron_sword','weapon_rank':'D','skills':[]}
def rosterunit():
 c=lookup('characters','Chrom')
 return {'id':'chrom','class_id':'lord_m','level':1,'stats':copy.deepcopy(c['starting_stats_by_difficulty']['Hard']['raw']),'inventory':[{'instance_id':'v1','item_id':'vulnerary','remaining_uses':3}]}
class CombatTests(unittest.TestCase):
 def test_basic_damage_and_doubling_boundary(self):
  a,b=unit(14),unit(10);r=calculate({'attacker':a,'defender':b})
  self.assertEqual(r['attacker']['damage'],10);self.assertFalse(r['attacker']['doubles'])
  a['stats']['spd']=15;r=calculate({'attacker':a,'defender':b});self.assertTrue(r['attacker']['doubles']);self.assertEqual(r['attacker']['scheduled_hits'],2)
 def test_rank_and_triangle(self):
  self.assertEqual(rank_bonus('axe','A'),(1,10))
  a={'weapon_type':'sword','rank':'A'};b={'weapon_type':'axe','rank':'E'}
  self.assertEqual(triangle(a,b),((1,15),(-1,-15)))
  x,y=unit(),unit();x['weapon']='iron_axe';x['weapon_rank']='A';r=calculate({'attacker':x,'defender':y})
  self.assertEqual(r['attacker']['damage'],12) # 10+8-1-5: disadvantaged rank bonus removed
 def test_magic_targets_res(self):
  a,b=unit(),unit();a['weapon']='thunder';b['weapon']=None
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['attacker']['damage'],5)
 def test_effective_triples_might(self):
  a,b=unit(),unit();a['weapon']='iron_bow';b['weaknesses']=['flying'];b['weapon']=None
  r=calculate({'attacker':a,'defender':b,'context':{'distance':2}});self.assertEqual(r['attacker']['damage'],23)
 def test_probability_and_early_death(self):
  a,b=unit(),unit();a['weapon_rank']='A';a['weapon']='brave_sword';a['stats']['skl']=100;b['current_hp']=1
  r=calculate({'attacker':a,'defender':b});self.assertEqual(r['outcome']['defender_death_probability'],1);self.assertEqual(r['outcome']['expected_attacker_hp'],30)
  self.assertAlmostEqual(sum(s['probability'] for s in r['outcome']['states']),1)
 def test_true_hit(self):
  self.assertEqual(true_hit(0),0);self.assertEqual(true_hit(100),1);self.assertEqual(true_hit(50),.505);self.assertEqual(true_hit(80),.922)
 def test_unsupported_and_invalid(self):
  for skill in ['counter','aether','astra','lethality','lifetaker','dragonskin']:
   a=unit();a['skills']=[skill]
   with self.assertRaises(ValueError):calculate({'attacker':a,'defender':unit()})
  with self.assertRaises(ValueError):calculate({'attacker':unit(),'defender':unit(),'context':{'distance':2}})
  a=unit();a['alive']=False
  with self.assertRaises(ValueError):calculate({'attacker':a,'defender':unit()})
 def test_dual_explicitly_partial(self):
  r=calculate({'attacker':unit(),'defender':unit(),'partners':['frederick']});self.assertIsNone(r['outcome'])
class PairTests(unittest.TestCase):
 def test_threshold_support(self):
  r={s:9 for s in STATS};a=pair_bonus('cavalier',r,'none');r['str']=10;b=pair_bonus('cavalier',r,'none');self.assertEqual(b['str'],a['str']+1)
  c=pair_bonus('cavalier',r,'A');self.assertEqual(c['str'],b['str']+2);self.assertEqual(c['mov'],b['mov'])
 def test_dual(self):
  self.assertEqual(dual_bonus(['S'])['hit'],15);self.assertEqual(dual_bonus([])['hit'],0)
  self.assertEqual(dual_rates({'skl':20,'def':16,'res':8},{'skl':20,'def':16,'res':8},'S'),{'strike':70,'physical_guard':18,'magical_guard':14})
class GrowthTests(unittest.TestCase):
 def test_growth_and_projection(self):
  c=lookup('characters','chrom');self.assertEqual(growths('chrom','lord_m')['str'],60)
  d={'character':'chrom','starting_class':'lord_m','starting_raw_stats':c['starting_stats_by_difficulty']['Hard']['raw'],'segments':[{'class_id':'lord_m','level_ups':2}]}
  self.assertAlmostEqual(project(d)['stats']['str']['mean'],8.2)
  d['segments']=[{'class_id':'great_lord_m','change':'promotion','level_ups':0}]
  self.assertEqual(project(d)['stats']['str']['mean'],11)
 def test_cap(self):
  c=lookup('characters','chrom');stats=copy.deepcopy(c['starting_stats_by_difficulty']['Hard']['raw']);stats['str']=26
  d={'character':'chrom','starting_class':'lord_m','starting_raw_stats':stats,'segments':[{'class_id':'lord_m','level_ups':2}]};self.assertEqual(project(d)['stats']['str']['mean'],26)
 def test_internal(self):
  self.assertEqual(internal_level(5,True,10),35);self.assertEqual(second_seal_cumulative(20,True,29,'Hard'),30)
 def test_avatar(self):
  a=avatar('spd','lck');self.assertEqual(a['starting_raw_stats']['spd'],8);self.assertEqual(a['starting_raw_stats']['lck'],2)
  with self.assertRaises(ValueError):avatar('spd','spd')
  with self.assertRaises(ValueError):growths('robin','tactician')
 def test_child(self):
  p={'base_growths':{s:30 for s in STATS},'cap_modifiers':{s:1 for s in STATS[1:]}}
  r=child({'child':'lucina','parents':[p,p]});self.assertEqual(r['base_growths']['hp'],35);self.assertEqual(r['cap_modifiers']['str'],3)
class StateTests(unittest.TestCase):
 def test_death_and_no_resurrection(self):
  r=upsert(initial('Hard','Classic'),rosterunit());death(r,'chrom');self.assertFalse(r['units']['chrom']['alive'])
  u=rosterunit();u['alive']=True
  with self.assertRaises(ValueError):upsert(r,u)
  upsert(r,u,True,'Player explicitly reset');self.assertTrue(r['units']['chrom']['alive'])
 def test_casual(self):
  r=upsert(initial('Hard','Casual'),rosterunit());death(r,'chrom');self.assertTrue(r['units']['chrom']['alive']);self.assertFalse(r['units']['chrom']['available_this_map'])
 def test_consumption(self):
  r=upsert(initial('Hard','Classic'),rosterunit());consume(r,'chrom','v1',3);self.assertEqual(r['units']['chrom']['inventory'],[])
  with self.assertRaises(ValueError):consume(r,'chrom','v1',1)
 def test_level_history(self):
  r=upsert(initial('Hard','Classic'),rosterunit());level_up(r,'chrom',{'hp':1,'str':1,'skl':1,'spd':1});self.assertEqual(r['units']['chrom']['level'],2);self.assertEqual(r['units']['chrom']['stats']['str'],8)
  self.assertEqual(r['units']['chrom']['history'][-1]['gains']['mag'],0)
 def test_atomic_failure(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'state') as tmp:
   p=Path(tmp)/'run.json';mutate(p,'init','test',lambda _:initial('Hard','Classic'));mutate(p,'upsert','test',lambda r:upsert(r,rosterunit()));before=p.read_bytes()
   with self.assertRaises(ValueError):mutate(p,'consume','test',lambda r:consume(r,'chrom','v1',4))
   self.assertEqual(p.read_bytes(),before);self.assertEqual(len(json.loads(before)['events']),2)
 def test_class_history(self):
  r=upsert(initial('Hard','Classic'),rosterunit());r['units']['chrom']['level']=10;class_change(r,'chrom','great_lord_m',rosterunit()['stats'],'promotion');self.assertEqual(r['units']['chrom']['history'][-1]['from_level'],10)

class ExtraToolsTests(unittest.TestCase):
 def test_forge(self):
  from forge import quote
  self.assertEqual(quote('steel_sword',[2,3,1])['cost'],4200)
  with self.assertRaises(ValueError):quote('steel_sword',[5,4,0])
  with self.assertRaises(ValueError):quote('mire',[1,0,0])
 def test_enemy_phase_accumulates_damage(self):
  from enemy_phase import evaluate
  a,b=unit(),unit();b['stats']['str']=20;b['stats']['skl']=100;b['stats']['lck']=100;b['stats']['spd']=10;a['weapon']=None
  r=evaluate({'player':a,'enemies':[{'unit':b},{'unit':b}]})
  self.assertEqual(r['death_probability'],1);self.assertEqual(r['minimum_possible_hp'],0)
 def test_comparison_rejects_wrong_level(self):
  from unit_compare import compare
  c=rosterunit();c.update(stats_basis='raw',alive=True)
  d={'character':'chrom','starting_class':'lord_m','starting_level':1,'starting_raw_stats':c['stats'],'segments':[{'class_id':'lord_m','level_ups':1}]}
  with self.assertRaises(ValueError):compare(c,project(d))
 def test_low_level_promotion_refused(self):
  r=upsert(initial('Hard','Classic'),rosterunit())
  with self.assertRaises(ValueError):class_change(r,'chrom','great_lord_m',rosterunit()['stats'],'promotion')

if __name__=='__main__':unittest.main()

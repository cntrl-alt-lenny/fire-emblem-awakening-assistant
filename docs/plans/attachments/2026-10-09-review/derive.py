import sys,json,copy,subprocess,types,hashlib
from pathlib import Path
root=Path(sys.argv[1]).resolve();batch=sys.argv[2];base="d3b646975a5f0686a798aaf12c0e541ed396da08"
sys.path.insert(0,str(root/'tools'))
def old(path):return subprocess.check_output(['git','show',base+':'+path],cwd=root,text=True)
def module(path):
 m=types.ModuleType('baseline');m.__file__=str(root/path);exec(old(path),m.__dict__);return m
private=lambda:{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).digest() for p in [root/'CURRENT_RUN.md',*sorted((root/'state').rglob('*'))] if p.is_file()}
before=private()
if batch=='08':
 from map_info import query,load
 baseline=module('tools/map_info.py')
 maps=json.loads(old('data/chapters/hard_tactics.json'))['records'];waves=json.loads(old('data/chapters/hard_reinforcements.json'))['records']
 baseline.load=lambda:(maps,{w['id']:w for w in waves})
 changed=json.loads((root/'data/chapters/hard_reinforcements.json').read_text())['records']
 deltas=[(a,b) for a,b in zip(waves,changed) if a!=b]
 assert len(deltas)==1 and deltas[0][0]['id']=='hard_chapter_11_t3_forts'
 a,b=map(copy.deepcopy,deltas[0]);a.pop('timing');b.pop('timing');assert a==b
 baseline_misses=0;cases=0
 for turn in list(range(1,13))+[99]:
  for phase in ('player','enemy'):
   ep=turn+(phase=='enemy');r=query(11,turn=turn,phase=phase)
   ids={w['id'] for w in r['candidate_reinforcements']}
   assert ('hard_chapter_11_t3_forts' in ids)==(ep>=3)
   prior={w['id'] for w in baseline.query(11,turn=turn,phase=phase)['candidate_reinforcements']}
   baseline_misses+=('hard_chapter_11_t3_forts' in prior)!=(ep>=3)
   assert not r['schedule_complete'] and not r['safe_to_claim_move_safe'] and not r['safe_to_conclude_no_reinforcements']
   cases+=1
 assert baseline_misses>0
 controls=0
 for m in maps:
  if m['chapter_id']=='chapter_11':continue
  for turn in (1,4,5,6,99):
   for phase in ('player','enemy'):
    assert query(m['chapter_id'],turn=turn,phase=phase)==baseline.query(m['chapter_id'],turn=turn,phase=phase);controls+=1
 for f in (root/'data').rglob('*.json'):
  rel=str(f.relative_to(root))
  if rel!='data/chapters/hard_reinforcements.json':assert f.read_text()==old(rel),rel
 print('Chapter 11 phase cases:',cases,'; original baseline mismatches:',baseline_misses,'; unchanged other-map queries:',controls)
 print('Only the fort timing claim changes in canonical JSON; all other records/fields preserved')
 def hashes():return {str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).digest() for f in (root/'data').rglob('*.json')}
 initial=hashes()
 for n in (1,2):
  r=subprocess.run(['make','rebuild'],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);print(r.stdout);print('make rebuild',n,'exit',r.returncode);assert r.returncode==0;assert hashes()==initial
 print('Two rebuilds preserve',len(initial),'canonical JSON files byte-for-byte')
else:
 from tactical_combat import assess
 from common import STATS
 baseline=module('tools/tactical_combat.py')
 def unit():return {'stats':dict(zip(STATS,[39,12,9,11,14,8,7,6])),'current_hp':39,'weapon':{'id':'brain_synthetic','weapon_type':'sword','damage_type':'physical','might':4,'hit':88,'crit':0,'range':'1','rank':'E','effect':'–','brave':False,'effectiveness':[]},'weapon_rank':'E','skills':[],'weaknesses':[],'terrain':{},'combat_bonuses':{},'remaining_uses':40}
 def battle():return {'attacker':unit(),'defender':unit(),'context':{'distance':1},'partners':[],'support_state':'none','difficulty':'Hard','mode':'Classic','stats_basis':'effective_displayed','observed_inputs_complete':True}
 refusals=controls=misses=0
 for side in ('attacker','defender'):
  for skill,field,valid in [('indoor_fighter','outdoors',[True,False]),('outdoor_fighter','outdoors',[True,False]),('lucky_seven','turn',[1,7,8,11]),('even_rhythm','turn',[1,2,7,8]),('odd_rhythm','turn',[1,2,7,8])]:
   for value in valid:
    p=battle();p[side]['skills']=[skill];p['context'][field]=value;snapshot=copy.deepcopy(p);assert assess(p)==baseline.assess(p);assert p==snapshot;controls+=1
   for value in ['MISSING',None,'unknown',True if field=='turn' else 1,False if field=='turn' else 0,1.0,{},[]]:
    p=battle();p[side]['skills']=[skill]
    if value!='MISSING':p['context'][field]=value
    snapshot=copy.deepcopy(p);r=assess(p);assert r['status']=='UNKNOWN' and r['outcome'] is None and r['safe_to_claim_survival'] is False;assert p==snapshot
    misses+=baseline.assess(p)['outcome'] is not None;refusals+=1
 assert misses>0
 p=battle();assert assess(p)==baseline.assess(p);controls+=1
 for f in (root/'data').rglob('*.json'):
  rel=str(f.relative_to(root));ref=('718bb7620605665a7db68c0c8e67094bc7deba55' if '--combined' in sys.argv else base)
  expected=subprocess.check_output(['git','show',ref+':'+rel],cwd=root,text=True);assert f.read_text()==expected

 print('Malformed required-context refusals:',refusals,'; original baseline numerical leaks:',misses,'; unchanged complete controls:',controls)
 print('Canonical data equals batch 08 when combined, or main when isolated; synthetic inputs immutable')
assert private()==before
print('Private state regular-file set and contents unchanged; no private values recorded')

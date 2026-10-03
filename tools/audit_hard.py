#!/usr/bin/env python3
"""Hard forensic structural/semantic audit. Source truth requires manual audit too."""
import json,sys
from common import ROOT,records
from hard_data import CAMPAIGN_IDS,CONFIDENCES
from map_info import load,query

def audit():
 maps,wm=load();errors=[];ss=json.loads((ROOT/'data/sources.json').read_text());sm={s['id']:s for s in ss};waves=list(wm.values())
 def check(ok,msg):
  if not ok:errors.append(msg)
 def refs(v,path):
  if isinstance(v,dict):
   for k,val in v.items():
    if k=='source_ids':
     for sid in val:check(sid in sm,path+': broken source '+sid)
    elif k=='confidence':check(val in CONFIDENCES,path+': invalid confidence')
    else:refs(val,path+'/'+k)
   if v.get('confidence')=='UNKNOWN' and 'value' in v and not (isinstance(v['value'],dict) and v['value'].get('kind')=='unknown'):check(v['value'] is None,path+': UNKNOWN must be null')
  elif isinstance(v,list):
   for n,val in enumerate(v):refs(val,path+'/'+str(n))
 refs(maps,'maps');refs(waves,'waves')
 check({m['chapter_id'] for m in maps}==set(CAMPAIGN_IDS),'Missing ordinary campaign map')
 check(len(maps)==44,'Campaign count or duplicate')
 cm={c['id'] for c in records('classes')};weapons={w['id'] for w in records('weapons')};items={x['id'] for x in records('items')};chars={x['id'] for x in records('characters')}
 for m in maps:
  check(m['difficulty']=='Hard' and m['mode']=='Classic' and m['scope']=='ordinary_campaign',m['id']+': scope contamination')
  check(m['reinforcements']['status'] in ('present','none_verified','none_supported','unknown'),m['id']+': invalid presence')
  check(m['reinforcements']['schedule_complete'] is False,m['id']+': premature full schedule')
  for r in m['recruitments']:check(r['unit_id'] in chars,m['id']+': invalid recruit')
  for wid in m['reinforcements']['wave_ids']:check(wid in wm and wm[wid]['chapter_id']==m['chapter_id'],m['id']+': wrong wave map')
  if m['reinforcements']['status'].startswith('none_'):check(bool(m['reinforcements']['absence']) and not m['reinforcements']['wave_ids'],m['id']+': false absence')
 for w in waves:
  check(w['difficulty']=='Hard' and w['mode']=='Classic',w['id']+': mode contamination')
  t=w['timing']['value'];check(t['kind'] in ('fixed','event','relative','repeating','conditional_report','unknown'),w['id']+': invalid timing kind')
  turns=t['turns'];check(turns is None or isinstance(turns,list) and turns==sorted(set(turns)) and all(type(n)is int and n>0 for n in turns),w['id']+': invalid turns')
  check(t['kind']!='fixed' or bool(turns),w['id']+': fixed timing missing turns')
  check(t['kind']=='fixed' or turns is None,w['id']+': conditional event wrongly fixed')
  check(w['coordinates']['value'] is None,w['id']+': invented coordinates')
  for u in w['units']['value'] or []:
   check(u['class_id'] is None or u['class_id'] in cm,w['id']+': invalid class')
   check(u['count'] is None or type(u['count'])is int and u['count']>0,w['id']+': invalid count')
   for item in u.get('equipment') or []:check(item in weapons or item in items,w['id']+': bad equipment '+item)
   check(u.get('skills') is None,w['id']+': unsupported guaranteed skill roll')
 check(sum(u['count'] for u in wm['hard_chapter_16_t4']['units']['value'])==8,'Chapter16 Hard count must be8, not Lunatic10')
 check(sum(u['count'] for u in wm['hard_chapter_16_t5']['units']['value'])==4,'Chapter16 Hard falcons4, not Lunatic6')
 check(sum(u['count'] for u in wm['hard_chapter_16_t6']['units']['value'])==4,'Chapter16 Hard Bow Knights4, not Lunatic6')
 check(not any(w['chapter_id']=='chapter_15' for w in waves),'Quarantined Chapter15 contaminated waves returned')
 q=query(7,turn=5,phase='player');check(q['target_enemy_phase_turn']==5 and len(q['candidate_reinforcements'])==1,'Player phase off-by-one')
 check(query(7,turn=4,phase='enemy')['target_enemy_phase_turn']==5,'Enemy phase off-by-one')
 legacy=json.loads((ROOT/'data/chapters/reinforcements.json').read_text())['records']
 check(all(w.get('quarantined') for w in legacy if w['id'] in ('p2_reviewed_wave_2','p2_reviewed_wave_3','p2_reviewed_wave_4')),'Legacy quarantine missing')
 result={'passed':not errors,'errors':errors,'campaign_maps':len(maps),'reinforcement_records':len(waves),'registered_sources':len(sm),'source_refs_resolve':not any('source' in e for e in errors),'source_truth_not_proven_by_tests':True,'readiness_requires':'Evidence-aware claims, no unconditional route-safety advice, complete observed inputs and refusal for unsupported interactions.'}
 (ROOT/'research/hard_verification/validation.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 r=audit();print(json.dumps(r,indent=2));sys.exit(0 if r['passed'] else 1)

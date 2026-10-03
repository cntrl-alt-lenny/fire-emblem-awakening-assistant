#!/usr/bin/env python3
"""Validate references/values and emit explicit coverage gaps; no claims of source truth."""
import json,sys
from common import ROOT,STATS,DIFFICULTIES,records

def audit():
 errors=[];warnings=[];counts={};catalog={}
 sources=json.loads((ROOT/'data/sources.json').read_text());source_ids={s['id'] for s in sources}
 if len(source_ids)!=len(sources):errors.append('Duplicate source IDs')
 def check(ok,msg):
  if not ok:errors.append(msg)
 def refs(value,where):
  if isinstance(value,dict):
   for k,v in value.items():
    if k=='source_ids':
     for sid in v:check(sid in source_ids,f'{where}: broken source {sid}')
    else:refs(v,where)
  elif isinstance(value,list):
   for v in value:refs(v,where)
 for path in sorted((ROOT/'data').rglob('*.json')):
  v=json.loads(path.read_text());refs(v,str(path.relative_to(ROOT)))
  if isinstance(v,dict) and 'records' in v:
   rs=v['records'];ids=[r['id'] for r in rs];check(len(ids)==len(set(ids)),f'{path}: duplicate IDs')
   for r in rs:check(bool(r.get('source_ids')),f'{path}:{r["id"]}: missing provenance')
 for category in ['characters','classes','weapons','items','skills','chapters','enemies']:
  catalog[category]={r['id']:r for r in records(category)};counts[category]=len(catalog[category])
 def resolve(cat,key,where):check(key in catalog[cat],f'{where}: unknown {cat} {key}')
 def stats(value,where,negative=False):
  check(set(value)==set(STATS),f'{where}: stat keys')
  check(all(type(v) is int and (negative or v>=0) for v in value.values()),f'{where}: invalid stats')
 for c in catalog['classes'].values():
  stats(c['base_stats'],c['id']);stats(c['caps'],c['id']+' caps')
  for f in ['promotes_to','promotes_from']:
   for k in c[f]:
    resolve('classes',k,c['id'])
    if k in catalog['classes']:check(c['id'] in catalog['classes'][k]['promotes_from' if f=='promotes_to' else 'promotes_to'],f'{c["id"]}: asymmetric promotion {k}')
  for entry in c['skills']:
   resolve('skills',entry['skill_id'],c['id']);check(1<=entry['level']<=c['level_cap'],c['id']+' skill level')
  if c['growth_modifiers'] is None and c['id']!='taguel':warnings.append(c['id']+': missing class growths (enemy/NPC)')
 for c in catalog['characters'].values():
  if c['starting_class_id']:resolve('classes',c['starting_class_id'],c['id'])
  for k in c['class_set'] or []:resolve('classes',k,c['id'])
  for k in c['starting_skills']:resolve('skills',k,c['id'])
  for k in c['starting_inventory']:check(k in catalog['weapons'] or k in catalog['items'],f'{c["id"]}: unknown inventory {k}')
  for difficulty,v in c['starting_stats_by_difficulty'].items():
   check(difficulty in DIFFICULTIES,c['id']+' difficulty')
   if v['raw'] is not None:stats(v['raw'],c['id']+' '+difficulty)
  if c['base_growths'] is not None:stats(c['base_growths'],c['id']+' growths')
  check(c['recruitment'] is not None,c['id']+' recruitment missing')
 for w in catalog['weapons'].values():
  check(w['weapon_type'] in ['sword','lance','axe','bow','tome','stone','claw','breath'],w['id']+' type')
  check(w['rank'] in ['E','D','C','B','A',None],w['id']+' rank')
  for k in ['might','hit','crit']:check(type(w[k]) is int and 0<=w[k]<=200,w['id']+' '+k)
  if w['uses'] is not None:check(w['uses']>0,w['id']+' uses')
 for ch in catalog['chapters'].values():
  check(set(ch['difficulty_data'])==set(DIFFICULTIES),ch['id']+' modes mixed/missing')
  for k in ch['recruitable_units']:resolve('characters',k,ch['id'])
  for d,v in ch['difficulty_data'].items():
   if v['enemies'] is not None:
    for k in v['enemies']:
     resolve('enemies',k,ch['id'])
     if k in catalog['enemies']:check(catalog['enemies'][k]['difficulty']==d and catalog['enemies'][k]['chapter_id']==ch['id'],ch['id']+' enemy difficulty contamination')
   for r in v['reinforcements'] or []:
    for k in r['enemy_ids']:
     resolve('enemies',k,ch['id'])
     if k in catalog['enemies']:check(catalog['enemies'][k]['difficulty']==d,ch['id']+' reinforcement mode contamination')
 for n in range(1,26):check('chapter_'+str(n) in catalog['chapters'],f'Missing chapter {n}')
 for n in range(1,24):check('paralogue_'+str(n) in catalog['chapters'],f'Missing paralogue {n}')
 for e in catalog['enemies'].values():
  resolve('classes',e['class_id'],e['id']);resolve('chapters',e['chapter_id'],e['id']);stats(e['stats'],e['id'])
  check(e['difficulty'] in DIFFICULTIES,e['id']+' difficulty')
  for k in e['inventory']:resolve('weapons',k,e['id'])
  for k in e['skills_known']:resolve('skills',k,e['id'])
 supports=json.loads((ROOT/'data/supports/compatibility.json').read_text())['records'];counts['support_edges']=len(supports)
 aliases={'avatar_m':'robin','avatar_f':'robin','morgan_m':'morgan','morgan_f':'morgan','lonqu':'lon_qu','sayri':'say_ri','yenfay':'yen_fay'}
 for edge in supports:
  for k in edge['units']:resolve('characters',aliases.get(k,k),edge['id'])
  for rank,t in edge['thresholds'].items():check(t is None or type(t) is int and t>0,edge['id']+' threshold')
 for filename in ['shops','merchants','renown','merchant_rare_pool']:
  rs=json.loads((ROOT/'data/items'/f'{filename}.json').read_text())['records'];counts[filename]=len(rs)
  for row in rs:
   if row.get('chapter_id'):resolve('chapters',row['chapter_id'],filename)
   for k in row.get('item_ids',[row.get('reward_id')]):
    if k and k!='rare_item':check(k in catalog['weapons'] or k in catalog['items'],filename+': unknown inventory '+k)
 counts['sources']=len(sources)
 coverage={'chapters_by_kind':{k:sum(c['kind']==k for c in catalog['chapters'].values()) for k in ['main','paralogue','DLC']},'map_difficulty_slots':len(catalog['chapters'])*4,'unresolved_map_difficulty_slots':sum(v['status']=='unresolved' for c in catalog['chapters'].values() for v in c['difficulty_data'].values()),'partially_verified_map_difficulty_slots':sum(v['status']=='partially_verified' for c in catalog['chapters'].values() for v in c['difficulty_data'].values()),'unresearched_map_difficulty_slots':sum(v['status']=='not_researched' for c in catalog['chapters'].values() for v in c['difficulty_data'].values()),'verified_safe_reinforcement_schedules':sum(r.get('safe_for_tactical_certainty') is True for c in catalog['chapters'].values() for v in c['difficulty_data'].values() for r in v['reinforcements'] or []),'weapons_with_obtainability':sum('obtainability' in w for w in catalog['weapons'].values())}
 warnings+=['Most facts are single-source transcriptions; validation cannot prove game accuracy.','All map schedules lack complete tactical verification.','Conditional child recruitment stats/classes/caps require actual parents.','Legacy SpotPass/DLC bonus character catalogs are incomplete.','Economy/world tables retained as unreviewed factual rows.']
 report={'passed':not errors,'counts':counts,'coverage':coverage,'errors':errors,'warnings':warnings}
 (ROOT/'research/audit.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 r=audit();print(json.dumps(r,indent=2));sys.exit(0 if r['passed'] else 1)

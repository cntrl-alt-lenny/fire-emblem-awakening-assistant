#!/usr/bin/env python3
"""Semantic cross-checks, complete coverage matrix and dangerous ambiguity checks."""
import ast,json,sys
from collections import Counter
from common import ROOT,STATS,DIFFICULTIES,records,lookup

def audit():
 errors=[];warnings=[]
 def check(cond,msg):
  if not cond:errors.append(msg)
 cover=json.loads((ROOT/'data/chapters/coverage.json').read_text())['records'];waves=json.loads((ROOT/'data/chapters/reinforcements.json').read_text())['records'];cs={c['id']:c for c in records('chapters')}
 maps=[c for c in cs.values() if c['kind'] in ('main','paralogue')]
 check({(r['map_id'],r['difficulty']) for r in cover}=={(m['id'],d) for m in maps for d in DIFFICULTIES},'Incomplete/contaminated 51-map four-mode coverage matrix')
 checks=json.loads((ROOT/'research/phase2/reviewed_additions.json').read_text())['numeric_crosschecks']
 for item in checks:
  record=lookup(item['category'],item['id'])
  for k,v in item['expected'].items():check(record[k]==v,f"Independent cross-check mismatch: {item['id']} {k}")
 check({'class_id':'general','level':15} in lookup('skills','pavise')['learned_in'],'Pavise General level15 cross-check')
 for r in records('weapons'):
  check(r['brave']==('Brave' in r['name'] or '2 consecutive attacks' in r['effect'] or 'twice' in r['effect'].lower()),r['id']+' dropped Brave property')
  if r['id'] in ('beaststone','beaststone_plus','dragonstone','dragonstone_plus'):check(bool(r['stat_bonuses']),r['id']+' lost stone bonuses')
 for skill in ('vantage','wrath'):check('at most half' in lookup('skills',skill)['effect'],skill+' inclusive HP boundary lost')
 em={e['id']:e for e in records('enemies')}
 for e in em.values():
  check(e['difficulty']=='Lunatic','Lunatic templates leaked into other difficulty')
  for w in e['equipment']:
   if w['enemy_forge_marker']:check(w['effective_weapon_stats']=='UNKNOWN',e['id']+' enemy forge guessed')
  check(e['position'] is None,e['id']+' unsupported coordinates')
 for w in waves:
  check(w['difficulty'] in DIFFICULTIES,w['id']+' invalid mode')
  check(bool(w['source_ids']),w['id']+' unsourced')
  check(w['safe_for_tactical_certainty'] is False,w['id']+' premature certification')
  for eid in w['enemy_ids']:check(em[eid]['difficulty']==w['difficulty'] and em[eid]['chapter_id']==w['chapter_id'],w['id']+' enemy identity/mode mismatch')
  if w['timing_type']=='event_triggered':check(w['turns'] is None,w['id']+' event mislabeled fixed turn')
 sources={s['id'] for s in json.loads((ROOT/'data/sources.json').read_text())}
 def literals(node):
  if isinstance(node,ast.Constant) and isinstance(node.value,str):yield node.value
  elif isinstance(node,(ast.List,ast.Tuple)):
   for item in node.elts:yield from literals(item)
  elif isinstance(node,ast.IfExp):
   yield from literals(node.body);yield from literals(node.orelse)
 for path in (ROOT/'tools').glob('*.py'):
  tree=ast.parse(path.read_text())
  for node in ast.walk(tree):
   if isinstance(node,ast.Dict):
    for k,v in zip(node.keys,node.values):
     if isinstance(k,ast.Constant) and k.value=='source_ids':
      for sid in literals(v):check(sid in sources,str(path.name)+': unregistered literal source '+sid)
 counts={d:{k:sum(r['difficulty']==d and r['map_status']==k for r in cover) for k in ('verified','partially_verified','unresolved')} for d in DIFFICULTIES}
 reinforcements={d:{k:sum(r['difficulty']==d and r['reinforcement_status']==k for r in cover) for k in ('verified','partially_verified','unresolved')} for d in DIFFICULTIES}
 warnings=['No map has a completely verified tactical schedule. Coordinates, AI geometry and Lunatic+ random skills remain unknown.','Independent numeric spot checks are limited; this is not an exhaustive numerical audit of all character/class/gender/child/DLC data.','Template multiplicities are source rows; identical stat rows can represent distinct enemies and must not be deduplicated by stats.','Parser output gaps and empty source headings prevent certification of starting positions or complete enemy lists.']
 result={'passed':not errors,'errors':errors,'warnings':warnings,'coverage_by_difficulty':counts,'reinforcements_by_difficulty':reinforcements,'enemy_templates':len(em),'partial_wave_records':len(waves),'independent_numeric_fields_checked':sum(len(r['expected']) for r in checks),'fully_verified_schedules':0,'Hard_Classic_ready_without_unverified_tactical_data':False}
 (ROOT/'research/phase2/final_audit.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 report=audit();print(json.dumps(report,indent=2));sys.exit(0 if report['passed'] else 1)

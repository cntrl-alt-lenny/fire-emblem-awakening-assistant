import sys,json,re,tempfile
from pathlib import Path
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'tools'))
from play_briefing import briefing,render,GENERAL_WARNING
from map_info import query,load
cases=0
for m in load()[0]:
 for turn in (1,3,4,99):
  for phase in ('player','enemy'):
   q=query(m['chapter_id'],turn=turn,phase=phase,spoilers='Full information');b=briefing(m['chapter_id'],'hard',turn,phase,'Full information');assert b==q;cases+=1
   n=briefing(m['chapter_id'],'hard',turn,phase,'No spoilers');assert set(n)=={'chapter_id','difficulty','mode','current_turn','current_phase','target_enemy_phase_turn','schedule_complete','safe_to_claim_move_safe','warning'}
   assert n['schedule_complete'] is False and n['safe_to_claim_move_safe'] is False
   assert len(render(n).splitlines())==3 and 'Detailed material withheld' in render(n)
   for provenance in (False,True):assert render(n,provenance)==render(n)
   t=briefing(m['chapter_id'],'hard',turn,phase,'Tactical spoilers');assert [w['id'] for w in t['candidate_reinforcements']]==[w['id'] for w in q['candidate_reinforcements']]
   assert t['absence_reasonably_supported']==q['absence_reasonably_supported'];assert t['safe_to_conclude_no_reinforcements']==q['safe_to_conclude_no_reinforcements']
   for arr in ('known_verified_supported','uncertain_partial_conflicted_unknown'):
    assert [(c['kind'],c['label'],c['confidence']) for c in t[arr]]==[(c['kind'],c['label'],c['confidence']) for c in q[arr]]
with tempfile.TemporaryDirectory() as folder:
 p=Path(folder)/'synthetic-context.json';p.write_text(json.dumps({'chapter':'chapter_7','difficulty':'Hard','mode':'Classic','turn':5,'spoiler_mode':'No spoilers'}));before=p.read_bytes()
 assert briefing(7,'hard',5,'player',state=p)['warning'].startswith(GENERAL_WARNING)
 assert 'candidate_reinforcements' in briefing(7,'hard',5,'player','Tactical spoilers',p)
 for kw in ({'chapter':8},{'turn':6},{'phase':None},{'difficulty':'Lunatic'}):
  args=dict(chapter=7,difficulty='hard',turn=5,phase='player',state=p);args.update(kw)
  try:briefing(**args)
  except ValueError:pass
  else:raise AssertionError(kw)
 assert p.read_bytes()==before
example=render(briefing(7,'hard',5,'player'))
print('Brain full-query/claim/candidate/absence/spoiler controls:',cases,'; all 44 maps; synthetic state unchanged')
print('Chapter 7 player phase 5: concise physical lines',len(example.splitlines()),'; unknowns retained')

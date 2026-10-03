#!/usr/bin/env python3
"""Evidence-aware current-map Hard/Classic reference and next-enemy-phase warnings."""
import argparse,json,re
from common import ROOT,dump,slug
GOOD={'VERIFIED','SUPPORTED'}
def load():
 maps=json.loads((ROOT/'data/chapters/hard_tactics.json').read_text())['records']
 waves=json.loads((ROOT/'data/chapters/hard_reinforcements.json').read_text())['records']
 return maps,{w['id']:w for w in waves}
def resolve(chapter,maps):
 text=slug(str(chapter));text='chapter_'+text if text.isdigit() else text
 text=re.sub(r'^(?:para|sidequest)_?(\d+)$',r'paralogue_\1',text)
 for m in maps:
  if text in (m['chapter_id'],m['id'],slug(m['name'])):return m
 raise ValueError('No reviewed ordinary Hard campaign map: '+str(chapter)+'. Premonition/tutorial, DLC and SpotPass are separate.')
def eligible(w,ep):
 t=w['timing']['value']
 if ep is None or t['turns'] is None:return True
 return ep in t['turns']
def query(chapter,difficulty='hard',turn=None,phase=None,spoilers='Tactical spoilers'):
 if str(difficulty).lower()!='hard':raise ValueError('This forensic query supports Hard only; other difficulties require separate datasets.')
 if turn is not None:
  if type(turn) is not int or turn<1:raise ValueError('Turn must be a positive integer')
  if phase not in ('player','enemy'):raise ValueError('Specify current --phase player or enemy when supplying turn; phase cannot be inferred.')
 elif phase is not None:raise ValueError('Phase requires a turn')
 if spoilers not in ('No spoilers','Tactical spoilers','Full information'):raise ValueError('Invalid spoiler mode')
 maps,wm=load();m=resolve(chapter,maps);ep=turn+(phase=='enemy') if turn is not None else None
 result={'chapter_id':m['chapter_id'],'difficulty':'Hard','mode':'Classic','current_turn':turn,'current_phase':phase,'target_enemy_phase_turn':ep,'map_confidence':m['confidence'],'schedule_complete':False,'safe_to_claim_move_safe':False}
 if spoilers=='No spoilers':
  result['warning']='Map safety cannot be guaranteed. Immediate reinforcement action is possible on Hard; detailed events/recruits withheld under No spoilers. Use observed enemy combat inputs.'
  return result
 known=[];uncertain=[]
 def add(kind,label,claim):
  target=known if claim['confidence'] in GOOD else uncertain
  target.append({'kind':kind,'label':label,**claim})
 for f in ('objective','deployment','starting_area','initial_enemies','bosses','shops'):add('map',f,m[f])
 for f in ('hazards','activation','interactables','conflicts'):
  for n,c in enumerate(m[f],1):add(f,str(n),c)
 for r in m['recruitments']:add('recruitment',r['unit_id'],r['condition'])
 absent=m['reinforcements']['absence']
 if absent:add('reinforcements','Explicit reported absence',absent)
 elif m['reinforcements']['status']=='unknown':
  uncertain.append({'kind':'reinforcements','label':'Existence/absence','value':None,'confidence':'UNKNOWN','source_ids':m['source_ids'],'notes':'Sources checked but no reliable explicit presence or absence statement. Silence does not establish absence.'})
 selected=[]
 for wid in m['reinforcements']['wave_ids']:
  w=wm[wid]
  if not eligible(w,ep):continue
  selected.append(w)
  # A conflicted wave must not be split into apparently safe known schedule parts.
  for f in ('timing','location','units','spawn_phase','immediate_action','coordinates','skills','suppression'):
   c=dict(w[f])
   if w['confidence']=='CONFLICTED' and f in ('timing','location','units'):c['confidence']='CONFLICTED';c['notes']=(c.get('notes') or '')+' Wave contains an unresolved disagreement; values are alternatives, not a chosen schedule.'
   add('reinforcement',wid+':'+f,c)
 if not absent:
  uncertain.append({'kind':'schedule','label':'Additional arrivals/events','value':None,'confidence':'UNKNOWN','source_ids':m['source_ids'],'notes':'Complete schedule not established. No matching fixed-turn wave does NOT mean no spawn. Conditional and unknown-time families are always retained as possible.'})
 uncertain.append({'kind':'safety','label':'Complete threat geometry','value':None,'confidence':'UNKNOWN','source_ids':m['source_ids'],'notes':'Exact positions, all enemy stats/equipment/skills and event boundaries are not complete. No empty list or zero modeled death chance certifies a move without observed inputs.'})
 result.update(known_verified_supported=known,uncertain_partial_conflicted_unknown=uncertain,candidate_reinforcements=selected,reinforcement_status=m['reinforcements']['status'],reinforcement_absence_confidence=absent['confidence'] if absent else None,
 absence_reasonably_supported=bool(absent and absent['confidence'] in GOOD),safe_to_conclude_no_reinforcements=bool(absent and absent['confidence']=='VERIFIED'),warning='Known facts are source-supported, not a complete threat map. Hard beginning-enemy-phase spawns can move/attack immediately. Never rely on enemy-phasing an unknown wave.',absence_limitations=absent.get('notes') if absent else None)
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--chapter',required=True);p.add_argument('--difficulty',required=True);p.add_argument('--turn',type=int);p.add_argument('--phase',choices=['player','enemy']);p.add_argument('--spoilers',default='Tactical spoilers',choices=['No spoilers','Tactical spoilers','Full information']);a=p.parse_args()
 try:dump(query(a.chapter,a.difficulty,a.turn,a.phase,a.spoilers))
 except ValueError as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

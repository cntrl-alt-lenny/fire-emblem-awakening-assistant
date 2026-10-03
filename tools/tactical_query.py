#!/usr/bin/env python3
"""Spoiler-scoped current-map warnings and conservative next-turn wave candidates."""
import argparse,json
from common import ROOT,DIFFICULTIES,lookup,dump,slug

def query(map_name,difficulty,turn,spoiler='Tactical spoilers'):
 if difficulty not in DIFFICULTIES:raise ValueError('Explicit supported difficulty required')
 if type(turn) is not int or turn<1:raise ValueError('Turn must be positive integer')
 c=lookup('chapters',map_name);slot=c['difficulty_data'][difficulty]
 rows=json.loads((ROOT/'data/enemies/enemies.json').read_text())['records'];em={e['id']:e for e in rows}
 next_turn=turn+1;certain=[];possible=[];unknown=[]
 for w in slot['reinforcements'] or []:
  if w.get('quarantined'):continue
  # UNKNOWN triggers can postpone/suppress/enable a reported-turn wave; do not remove them from risk.
  report={**w,'enemy_templates':[{'class_id':em[k]['class_id'],'equipment':em[k].get('equipment',[]),'skills_known':em[k]['skills_known'],'skills_unresolved':em[k].get('skills_unresolved',[])} for k in w['enemy_ids']]}
  if 'units' not in report:report['units']=report['enemy_templates']
  if w.get('turns') is None:unknown.append(report)
  elif next_turn in w['turns']:
   (certain if w.get('safe_for_tactical_certainty') else possible).append(report)
 result={'map_id':c['id'],'difficulty':difficulty,'next_turn':next_turn,'coverage':slot['status'],'certain_waves':certain,'possible_reported_waves':possible,'waves_with_unknown_timing':unknown,'schedule_complete':False,'safe_to_conclude_no_reinforcements':False,'warning':'UNKNOWN: schedule is not certified. No candidate for this turn does not establish that no enemies spawn. Check current-map evidence and in-game warnings.','activation_zones':'UNKNOWN; no reliable coordinate/AI-trigger geometry has been imported.','hazard_claims':[h for h in slot.get('hazard_claims',[]) if not h.get('quarantined')],'conflicts':slot.get('conflicts',[]),'reported_absence':slot.get('reported_absence'),'source_ids':list(dict.fromkeys(s for w in slot['reinforcements'] or [] for s in w['source_ids']))}
 if difficulty=='Hard':
  result['hard_reference_notice']='Legacy API targets turn N+1. Prefer map_info.py --chapter MAP --difficulty hard --turn N --phase player|enemy for phase-aware reviewed claims; legacy schedules are not authoritative.'
 if spoiler=='No spoilers':
  result={'map_id':c['id'],'difficulty':difficulty,'next_turn':next_turn,'schedule_complete':False,'warning':'Current-map reinforcement safety cannot be certified from local data. Ask for tactical details if needed.'}
 elif spoiler not in ('Tactical spoilers','Full information'):raise ValueError('Invalid spoiler mode')
 return result

def hazards(enemy,player):
 """Flag referenced observed unit weaknesses and skills; never synthesize missing rolls."""
 from combat_calculator import SAFE_SKILLS
 from combat_events import EVENT_SKILLS
 e=enemy;weapon=e.get('weapon')
 if isinstance(weapon,str):weapon=lookup('weapons',weapon)
 effective=set((weapon or {}).get('effectiveness',[]))&set(player.get('weaknesses',[]))
 if 'conquest' in player.get('skills',[]):effective-={'beast','armour'}
 if 'iotes_shield' in player.get('skills',[]):effective-={'flying'}
 return {'effective_against':sorted(effective),'enemy_skills':e.get('skills',[]),'unsupported_combat_skills':sorted(set(e.get('skills',[]))-SAFE_SKILLS-EVENT_SKILLS),'doubles_player':e['stats']['spd']-player['stats']['spd']>=5,'warning':'Requires observed effective stats, full skill list, actual weapon/forge and current HP. Template stats do not certify safety.'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('map');p.add_argument('--difficulty',required=True,choices=DIFFICULTIES);p.add_argument('--turn',type=int,required=True);p.add_argument('--spoilers',default='Tactical spoilers',choices=['No spoilers','Tactical spoilers','Full information']);a=p.parse_args()
 try:dump(query(a.map,a.difficulty,a.turn,a.spoilers))
 except (ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Strict live-tactical gate around the existing supported combat calculator.
Unknown input completeness or unsupported effects produce UNKNOWN, never reassurance.
"""
import argparse
from common import read_json,dump
from combat_calculator import calculate
REQUIRED=('stats','current_hp','weapon','weapon_rank','skills','weaknesses','terrain','combat_bonuses','remaining_uses')
def assess(payload):
 missing=[]
 if not isinstance(payload,dict):return {'status':'UNKNOWN','reason':'Battle input must be an object','outcome':None,'safe_to_claim_survival':False}
 if not isinstance(payload.get('context',{}),dict):return {'status':'UNKNOWN','reason':'Context must be an object','outcome':None,'safe_to_claim_survival':False}
 if payload.get('difficulty')!='Hard' or payload.get('mode')!='Classic':missing.append('Explicit Hard/Classic ruleset')
 if payload.get('observed_inputs_complete') is not True:missing.append('Observed stats, equipment/forge, skills, weaknesses and support completeness must be confirmed')
 if payload.get('stats_basis')!='effective_displayed':missing.append('Stats must explicitly be effective_displayed (include active bonuses exactly once)')
 if payload.get('support_state') not in ('none','adjacent','paired'):missing.append('Explicit support_state: none only when neither side has a paired/adjacent support combatant')
 if not isinstance(payload.get('partners'),list):missing.append('Explicit partners list: [] for none; missing/null does not mean unpaired')
 for side in ('attacker','defender'):
  u=payload.get(side,{})
  if not isinstance(u,dict):
   missing.append(side+': observed unit object required');continue
  for k in REQUIRED:
   if k not in u or (k!='weapon' and u[k] is None):missing.append(side+':'+k)
 if 'distance' not in payload.get('context',{}):missing.append('Actual attack distance')
 if missing:return {'status':'UNKNOWN','missing':missing,'safe_to_claim_survival':False,'outcome':None}
 if payload['support_state']!='none':return {'status':'UNKNOWN','reason':'Full paired/adjacent Dual Strike and Dual Guard outcome is unsupported; use pair_up/paired_forecast for supported bonuses and rates.','safe_to_claim_survival':False,'outcome':None}
 try:r=calculate(payload)
 except (ValueError,KeyError,TypeError) as e:return {'status':'UNKNOWN','reason':str(e),'safe_to_claim_survival':False,'outcome':None}
 if r.get('outcome') is None:return {'status':'UNKNOWN','reason':r['limitation'],'safe_to_claim_survival':False,'forecast':r,'outcome':None}
 o=r['outcome'];risk=o['attacker_death_probability']>0 or o['defender_death_probability']>0
 return {'status':'POTENTIALLY_LETHAL' if risk else 'NO_MODELED_DEATH_IN_THIS_DUEL','conditional_on_observed_inputs':True,'safe_to_claim_map_survival':False,'attacker_can_die':o['attacker_death_probability']>0,'defender_can_die':o['defender_death_probability']>0,'worst_attacker_hp':o['minimum_possible_attacker_hp'],'worst_defender_hp':o['minimum_possible_defender_hp'],'forecast':r,'outcome':o,'warning':'Supported duel only. No prediction of AI order, unseen enemies, reinforcements or future movement. Expected HP is not a guarantee.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args();dump(assess(read_json(a.input)))
if __name__=='__main__':main()

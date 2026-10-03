#!/usr/bin/env python3
"""Strict live-tactical gate around the existing supported combat calculator.
Unknown input completeness or unsupported effects produce UNKNOWN, never reassurance.
"""
import argparse,copy
from common import read_json,dump,lookup
from combat_calculator import calculate,SAFE_WEAPON_EFFECTS
REQUIRED=('stats','current_hp','weapon','weapon_rank','skills','weaknesses','terrain','combat_bonuses','remaining_uses')

def known_weapon(unit, side):
 """Resolve IDs, then enforce the live input contract without changing mechanics."""
 weapon = unit['weapon']
 state = unit.get('weapon_state')
 if state not in (None, 'equipped', 'unequipped'):
  raise ValueError(side+':weapon_state must be equipped or unequipped')
 if weapon is None:
  if side == 'defender' and state == 'unequipped':return None
  raise ValueError(side+':weapon is unknown; only an explicitly unequipped defender may use null')
 if state == 'unequipped':raise ValueError(side+':weapon contradicts weapon_state unequipped')
 if isinstance(weapon, str):
  try:weapon = lookup('weapons', weapon)
  except ValueError as e:raise ValueError(side+':weapon: '+str(e)) from e
 if not isinstance(weapon, dict) or not weapon:
  raise ValueError(side+':weapon must be a known canonical ID or complete object')
 effect = weapon.get('effect')
 if not isinstance(effect, str) or effect not in SAFE_WEAPON_EFFECTS:
  raise ValueError(side+':weapon.effect missing, unknown or unsupported; use explicit – for no special effect')
 if type(weapon.get('brave')) is not bool:
  raise ValueError(side+':weapon.brave requires an explicit boolean')
 effectiveness = weapon.get('effectiveness')
 if not isinstance(effectiveness, list) or any(type(x) is not str or x not in ('beast','dragon','armour','flying') for x in effectiveness):
  raise ValueError(side+':weapon.effectiveness requires a known category list; [] means confirmed none')
 if weapon['brave'] != (effect == '2 consecutive attacks'):
  raise ValueError(side+':weapon.brave contradicts weapon.effect (2 consecutive attacks)')
 return copy.deepcopy(weapon)

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
 try:
  prepared=copy.deepcopy(payload)
  for side in ('attacker','defender'):prepared[side]['weapon']=known_weapon(prepared[side],side)
  r=calculate(prepared)
 except (ValueError,KeyError,TypeError) as e:return {'status':'UNKNOWN','reason':str(e),'safe_to_claim_survival':False,'outcome':None}
 if r.get('outcome') is None:return {'status':'UNKNOWN','reason':r['limitation'],'safe_to_claim_survival':False,'forecast':r,'outcome':None}
 o=r['outcome']
 probabilities={side:o[side+'_death_probability'] for side in ('attacker','defender')}
 at_risk=[side for side,p in probabilities.items() if p>0]
 certain=[side for side,p in probabilities.items() if p==1]
 return {'status':'LETHAL' if certain else 'POTENTIALLY_LETHAL' if at_risk else 'NO_MODELED_DEATH_IN_THIS_DUEL','at_risk_sides':at_risk,'certain_death_sides':certain,'attacker_death_probability':probabilities['attacker'],'defender_death_probability':probabilities['defender'],'conditional_on_observed_inputs':True,'safe_to_claim_map_survival':False,'attacker_can_die':o['attacker_death_probability']>0,'defender_can_die':o['defender_death_probability']>0,'worst_attacker_hp':o['minimum_possible_attacker_hp'],'worst_defender_hp':o['minimum_possible_defender_hp'],'forecast':r,'outcome':o,'warning':'Supported duel only. Side names describe attack roles, not player/enemy allegiance. No prediction of AI order, unseen enemies, reinforcements or future movement. Expected HP is not a guarantee.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args();dump(assess(read_json(a.input)))
if __name__=='__main__':main()

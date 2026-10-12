#!/usr/bin/env python3
"""Strict live-tactical gate around the existing supported combat calculator.
Unknown input completeness or unsupported effects produce UNKNOWN, never reassurance.
"""
import argparse,copy,json,os,re
from pathlib import Path
from common import dump,lookup,STATS,ROOT
from combat_calculator import calculate,SAFE_WEAPON_EFFECTS,SAFE_SKILLS
from combat_events import EVENT_SKILLS
REQUIRED=('stats','current_hp','weapon','weapon_rank','skills','weaknesses','terrain','combat_bonuses','remaining_uses')

UNIT_FIELDS=set(REQUIRED)|{'weapon_state','alive','forge','id','name'}
WEAPON_FIELDS={'id','name','weapon_type','damage_type','might','hit','crit','range',
               'rank','effect','brave','effectiveness'}
ROOT_FIELDS={'difficulty','mode','stats_basis','observed_inputs_complete',
             'support_state','partners','attacker','defender','context','note'}

def fields(value, allowed, path):
 if type(value) is not dict or set(value)-allowed:
  raise ValueError(path+': unsupported fields or object shape; effects cannot be omitted')

def integer(value, path, minimum=0):
 if type(value) is not int or value<minimum:
  raise ValueError(path+': requires an integer >= '+str(minimum)+' (not boolean or float)')

def label(value, path):
 if type(value) is not str or not value.strip() or value.strip().lower() in ('?', 'unknown'):
  raise ValueError(path+': requires a known nonempty string')

def boundary(payload):
 fields(payload,ROOT_FIELDS,'battle')
 if 'note' in payload and type(payload['note']) is not str:
  raise ValueError('note: requires a string')
 context=payload['context']
 fields(context,{'distance','outdoors','turn'},'context')
 integer(context['distance'],'context.distance',1)
 if 'turn' in context:integer(context['turn'],'context.turn',1)
 if 'outdoors' in context and type(context['outdoors']) is not bool:
  raise ValueError('context.outdoors requires a boolean')
 for partner in payload['partners']:label(partner,'partners')
 if payload['support_state']=='none' and payload['partners']:
  raise ValueError('partners contradict support_state none')
 for side in ('attacker','defender'):
  unit=payload[side]
  fields(unit,UNIT_FIELDS,side)
  for key in ('id','name'):
   if key in unit:label(unit[key],side+'.'+key)
  if 'alive' in unit and unit['alive'] is not True:
   raise ValueError(side+':alive requires true; unknown or dead units are refused')
  if 'forge' in unit:
   raise ValueError(side+':forge markers are unsupported; supply exact forged weapon values as a complete object')
  if 'weapon_state' in unit and unit['weapon_state'] not in ('equipped','unequipped'):
   raise ValueError(side+':weapon_state requires equipped or unequipped')
  fields(unit['stats'],set(STATS),side+'.stats')
  for key in STATS:integer(unit['stats'].get(key),side+'.stats.'+key,1 if key=='hp' else 0)
  integer(unit['remaining_uses'],side+'.remaining_uses')
  if type(unit['weapon_rank']) is not str or unit['weapon_rank'] not in ('E','D','C','B','A'):
   raise ValueError(side+':weapon_rank requires E/D/C/B/A')
  for key,allowed in (('terrain',{'def','res','avoid'}),('combat_bonuses',{'hit','avoid','crit','crit_avoid','attack'})):
   fields(unit[key],allowed,side+'.'+key)
   if any(type(v) is not int for v in unit[key].values()):
    raise ValueError(side+'.'+key+': values must be integers (not boolean or float)')
  if unit['weapon'] is None and unit['remaining_uses']!=0:
   raise ValueError(side+':weapon: remaining_uses must be zero for an unequipped unit')

def weapon_shape(weapon,side):
 for key in ('id','name'):
  if key in weapon:label(weapon[key],side+'.weapon.'+key)
 for key in ('might','hit','crit'):integer(weapon.get(key),side+'.weapon.'+key)
 if type(weapon.get('rank')) is not str or weapon['rank'] not in ('E','D','C','B','A'):
  raise ValueError(side+':weapon.rank requires E/D/C/B/A')
 if weapon.get('weapon_type') not in ('sword','lance','axe','bow','tome','stone','claw','breath'):
  raise ValueError(side+':weapon.weapon_type unsupported')
 if weapon.get('damage_type') not in ('physical','magical'):
  raise ValueError(side+':weapon.damage_type requires physical or magical')
 distance=weapon.get('range')
 if type(distance) is int and distance>=1:return
 if type(distance) is not str or not re.fullmatch(r'[1-9][0-9]*(?:[-~][1-9][0-9]*)?',distance):
  raise ValueError(side+':weapon.range requires positive integer or range string')
 ends=re.split('[-~]',distance)
 if len(ends)==2 and int(ends[0])>int(ends[1]):
  raise ValueError(side+':weapon.range endpoints reversed')

def require_observation_shape(unit, side):
 """Validate observations without coercing collections or dropping real effects."""
 for field in ('skills','weaknesses'):
  values=unit[field]
  if not isinstance(values,list):
   raise ValueError(side+':'+field+' requires an explicit list of strings; [] means confirmed none')
  for index,value in enumerate(values):
   if type(value) is not str:
    raise ValueError(side+':'+field+'['+str(index)+'] must be a string ID/category')
 if len(unit['skills'])>5:raise ValueError(side+':skills: at most five equipped skills')
 unknown=set(unit['skills'])-SAFE_SKILLS-EVENT_SKILLS
 if unknown:raise ValueError(side+':skills: Unsupported combat skills: '+', '.join(sorted(unknown)))
 if set(unit['weaknesses'])-{'beast','dragon','armour','flying'}:
  raise ValueError(side+':weaknesses: Unknown weakness category; use canonical beast/dragon/armour/flying')
 hp=unit['current_hp']
 if type(hp) is not int:
  raise ValueError(side+':current_hp requires an integer (not boolean or float)')
 stats=unit['stats']
 maximum=stats.get('hp') if isinstance(stats,dict) else None
 if hp<1 or (type(maximum) is int and hp>maximum):
  raise ValueError(side+':current_hp must be within 1..observed max HP')

def require_skill_context(unit, side, context):
 """Reject unknown skill conditions before the calculator can coerce/default them."""
 skills = unit['skills']
 fighters = [s for s in ('indoor_fighter','outdoor_fighter') if s in skills]
 if fighters and type(context.get('outdoors')) is not bool:
  raise ValueError(side+':context.outdoors requires an explicit boolean for '+', '.join(fighters))
 turn_skills = [s for s in ('lucky_seven','even_rhythm','odd_rhythm') if s in skills]
 if turn_skills and (type(context.get('turn')) is not int or context['turn']<1):
  raise ValueError(side+':context.turn requires an explicit positive integer (not boolean) for '+', '.join(turn_skills))

def known_weapon(unit, side):
 """Resolve IDs, then enforce the live input contract without changing mechanics."""
 weapon = unit['weapon']
 if 'forge' in unit:raise ValueError(side+':forge markers unsupported; supply complete weapon values')
 state = unit.get('weapon_state')
 if 'weapon_state' in unit and state is None:raise ValueError(side+':weapon_state cannot be null')
 if state not in (None, 'equipped', 'unequipped'):
  raise ValueError(side+':weapon_state must be equipped or unequipped')
 if weapon is None:
  if side == 'defender' and state == 'unequipped':return None
  raise ValueError(side+':weapon is unknown; only an explicitly unequipped defender may use null')
 if state == 'unequipped':raise ValueError(side+':weapon contradicts weapon_state unequipped')
 if type(weapon) is dict:fields(weapon,WEAPON_FIELDS,side+'.weapon')
 if isinstance(weapon, str):
  try:weapon = lookup('weapons', weapon)
  except ValueError as e:raise ValueError(side+':weapon: '+str(e)) from e
 if not isinstance(weapon, dict) or not weapon:
  raise ValueError(side+':weapon must be a known canonical ID or complete object')
 weapon_shape(weapon,side)
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
 try:
  for side in ('attacker','defender'):require_observation_shape(payload[side],side)
  for side in ('attacker','defender'):require_skill_context(payload[side],side,payload['context'])
  boundary(payload)
 except (ValueError,KeyError,TypeError) as e:return {'status':'UNKNOWN','reason':str(e),'safe_to_claim_survival':False,'outcome':None}
 if payload['support_state']!='none':return {'status':'UNKNOWN','reason':'Full paired/adjacent Dual Strike and Dual Guard outcome is unsupported; use pair_up/paired_forecast for supported bonuses and rates.','safe_to_claim_survival':False,'outcome':None}
 try:
  prepared=copy.deepcopy(payload)
  for side in ('attacker','defender'):prepared[side]['weapon']=known_weapon(prepared[side],side)
  r=calculate(prepared)
 except (ValueError,KeyError,TypeError) as e:return {'status':'UNKNOWN','reason':str(e),'safe_to_claim_survival':False,'outcome':None}
 if r.get('outcome') is None:return {'status':'UNKNOWN','reason':r['limitation'],'safe_to_claim_survival':False,'outcome':None}
 o=r['outcome']
 probabilities={side:o[side+'_death_probability'] for side in ('attacker','defender')}
 at_risk=[side for side,p in probabilities.items() if p>0]
 certain=[side for side,p in probabilities.items() if p==1]
 return {'status':'LETHAL' if certain else 'POTENTIALLY_LETHAL' if at_risk else 'NO_MODELED_DEATH_IN_THIS_DUEL','at_risk_sides':at_risk,'certain_death_sides':certain,'attacker_death_probability':probabilities['attacker'],'defender_death_probability':probabilities['defender'],'conditional_on_observed_inputs':True,'safe_to_claim_map_survival':False,'attacker_can_die':o['attacker_death_probability']>0,'defender_can_die':o['defender_death_probability']>0,'worst_attacker_hp':o['minimum_possible_attacker_hp'],'worst_defender_hp':o['minimum_possible_defender_hp'],'forecast':r,'outcome':o,'warning':'Supported duel only. Side names describe attack roles, not player/enemy allegiance. No prediction of AI order, unseen enemies, reinforcements or future movement. Expected HP is not a guarantee.'}
def object_pairs(pairs):
 result={}
 for key,value in pairs:
  if key in result:raise ValueError('Duplicate JSON object key: '+key)
  result[key]=value
 return result

def invalid_constant(value):
 raise ValueError('Invalid JSON constant: '+value)

def load_battle(path):
 selected=Path(path)
 if selected.name=='current_run.json':raise ValueError('Player run files are refused')
 resolved=selected.resolve(strict=True)
 if resolved.name=='current_run.json':raise ValueError('Player run files are refused')
 run=ROOT/'state'/'current_run.json'
 if run.exists() and os.path.samefile(resolved,run):raise ValueError('Player run aliases are refused')
 return json.loads(resolved.read_text(encoding='utf-8'),object_pairs_hook=object_pairs,
                   parse_constant=invalid_constant)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
 try:payload=load_battle(a.input)
 except (OSError,ValueError,RuntimeError) as e:p.exit(2,'Cannot read battle reliably: '+str(e)+'\n')
 dump(assess(payload))
if __name__=='__main__':main()

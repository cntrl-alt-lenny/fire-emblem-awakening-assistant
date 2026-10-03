#!/usr/bin/env python3
"""Auditable combat forecasts and finite exact probability distributions for supported duels.
Input stats are EFFECTIVE displayed stats: include all active stat bonuses already.
Combat-stat bonuses (hit/avoid/crit) are calculated separately. Unknown effects raise.
"""
import argparse,copy,json
from collections import defaultdict
from functools import lru_cache
from common import lookup,dump,read_json,STATS
from combat_events import EVENT_SKILLS,distribution
RANKS='EDCBA'
SAFE_SKILLS={'veteran','discipline','aptitude','armsthrift','locktouch','pass','movement_plus_1','deliverer','galeforce','despoil','healtouch','special_dance','bond','relief','renewal','paragon','shadowgift','limit_breaker','dual_strike_plus','dual_guard_plus','dual_support_plus','defender','all_stats_plus_2','resistance_plus_10','hp_plus_5','strength_plus_2','magic_plus_2','skill_plus_2','speed_plus_2','luck_plus_4','defence_plus_2','resistance_plus_2','swordfaire','lancefaire','axefaire','bowfaire','tomefaire','avoid_plus_10','hit_rate_plus_10','hit_rate_plus_20','zeal','gamble','prescience','patience','outdoor_fighter','indoor_fighter','lucky_seven','even_rhythm','odd_rhythm','aggressor','swordbreaker','lancebreaker','axebreaker','bowbreaker','tomebreaker','conquest','iotes_shield'}
SAFE_WEAPON_EFFECTS={'Taguel only, Str +3, Skl +5, Spd +5, Lck +4, Def +1','Taguel only, Str +5, Skl +8, Spd +8, Lck +6, Def +4, Res +2','Manaketes only, Str +8, Mag +5, Skl +3, Spd +2, Def +10, Res +7','Manaketes only, Str +11, Mag +6, Skl +5, Spd +4, Def +13, Res +9','–','2 consecutive attacks','Str +5','Spd +5','Luck +10','Mag +5','Skl +5','Skill +5','Def +5','Res +5','Lords, Great Lords and Lodestars only','Chrom and Marth only','Lucina and Marth only','Archers and Snipers only','Recover 10 HP each Turn','Can be used to recover 20 HP','Chrom and Marth only, can be used to recover 20 HP','Lucina and Marth only, can be used to recover 20 HP','Def and Res +5','Def and Res +2','Use to increase Resistance by 5 (effect decreases by 1 each Turn)'}
def clamp(x):return max(0,min(100,x))
@lru_cache(None)
def true_hit(hit):
 if not isinstance(hit,int) or not 0<=hit<=100:raise ValueError('Displayed hit must be integer 0..100')
 return sum((a+b)//2<hit for a in range(100) for b in range(100))/10000

def rank_bonus(typ,rank):
 if rank not in RANKS:raise ValueError('Weapon rank must be E/D/C/B/A')
 if rank in 'ED':return 0,0
 idx='CBA'.index(rank)
 if typ=='sword':return (1,2,3)[idx],0
 if typ in ('lance','bow','tome'):return (1,1,2)[idx],(0,5,5)[idx]
 if typ=='axe':return (0,0,1)[idx],(5,10,10)[idx]
 return 0,0

def triangle(a,b):
 """Both sides use the ADVANTAGEOUS unit's rank; disadvantage removes rank bonus."""
 if not a or not b:return (0,0),(0,0)
 wins={'sword':'axe','axe':'lance','lance':'sword'}
 ta,tb=a['weapon_type'],b['weapon_type']
 sign=1 if wins.get(ta)==tb else -1 if wins.get(tb)==ta else 0
 if not sign:return (0,0),(0,0)
 rank=a['rank'] if sign==1 else b['rank']
 hit={'E':5,'D':5,'C':10,'B':10,'A':15}[rank];mt=1 if rank in 'BA' else 0
 return (sign*mt,sign*hit),(-sign*mt,-sign*hit)

def prepare(u):
 v=copy.deepcopy(u)
 if v.get('alive') is False:raise ValueError('Cannot calculate combat using a dead unit')
 for k in STATS:
  if k not in v.get('stats',{}) or type(v['stats'][k]) is not int or v['stats'][k]<0:raise ValueError(f'Missing/invalid effective stat: {k}')
 if not 0<v.get('current_hp',v['stats']['hp'])<=v['stats']['hp']:raise ValueError('Current HP must be within 1..max HP')
 if len(v.get('skills',[]))>5:raise ValueError('At most five equipped skills')
 unknown=set(v.get('skills',[]))-SAFE_SKILLS-EVENT_SKILLS
 if unknown:raise ValueError('Unsupported combat skills: '+', '.join(sorted(unknown)))
 for field,allowed in [('terrain',{'def','res','avoid'}),('combat_bonuses',{'hit','avoid','crit','crit_avoid','attack'})]:
  values=v.get(field,{})
  if not isinstance(values,dict) or set(values)-allowed:raise ValueError('Unknown '+field+' field; effect cannot be silently omitted')
  if any(type(x) is not int for x in values.values()):raise ValueError(field+' values must be integers')
 if set(v.get('weaknesses',[]))-{'beast','dragon','armour','flying'}:raise ValueError('Unknown weakness category; use canonical beast/dragon/armour/flying')
 if v.get('remaining_uses') is not None and (type(v['remaining_uses']) is not int or v['remaining_uses']<0):raise ValueError('remaining_uses must be nonnegative integer')
 w=v.get('weapon')
 if isinstance(w,str):w=lookup('weapons',w)
 if w:
  w=copy.deepcopy(w)
  if v.get('forge'):raise ValueError('Supply forged might/hit/crit as a full weapon object; forge offsets are ambiguous')
  if w.get('effect','–') not in SAFE_WEAPON_EFFECTS:raise ValueError('Unsupported weapon effect: '+str(w.get('effect')))
  if w.get('damage_type') not in ('physical','magical'):raise ValueError('Explicit physical/magical damage_type required')
  if type(w.get('brave',False)) is not bool:raise ValueError('brave must be boolean')
  if set(w.get('effectiveness',[]))-{'beast','dragon','armour','flying'}:raise ValueError('Unknown weapon effectiveness category')
  for k in ('might','hit','crit'):
   if type(w.get(k)) is not int or w[k]<0:raise ValueError('Weapon requires nonnegative integer '+k)
  if w['weapon_type'] not in ('sword','lance','axe','bow','tome','stone','claw','breath'):raise ValueError('Invalid damaging weapon type')
  if v.get('weapon_rank','E') not in RANKS:raise ValueError('Invalid weapon rank')
  if w.get('rank') and RANKS.index(v['weapon_rank'])<RANKS.index(w['rank']):raise ValueError('Unit cannot use weapon at this rank')
  w['rank']=v.get('weapon_rank','E')
 v['weapon']=w;v['current_hp']=v.get('current_hp',v['stats']['hp']);return v

def in_range(w,distance):
 if not w:return False
 text=str(w['range']).replace('~','-')
 if '-' in text:lo,hi=map(int,text.split('-'));return lo<=distance<=hi
 return int(text)==distance

def modifiers(u,enemy,initiates,context):
 s=set(u.get('skills',[]));hit=avoid=crit=attack=0
 for skill,amount in [('hit_rate_plus_10',10),('hit_rate_plus_20',20)]:
  if skill in s:hit+=amount
 if 'avoid_plus_10' in s:avoid+=10
 if 'zeal' in s:crit+=5
 if 'gamble' in s:hit-=5;crit+=10
 for skill,condition,amount in [('prescience',initiates,15),('patience',not initiates,10),('outdoor_fighter',context.get('outdoors'),10),('indoor_fighter',context.get('outdoors') is False,10),('lucky_seven',context.get('turn',999)<=7,20),('even_rhythm',context.get('turn',1)%2==0,10),('odd_rhythm',context.get('turn',0)%2==1,10)]:
  if skill in s:
   if skill in ('outdoor_fighter','indoor_fighter') and 'outdoors' not in context:raise ValueError('Specify outdoors for fighter skill')
   if skill in ('lucky_seven','even_rhythm','odd_rhythm') and 'turn' not in context:raise ValueError('Specify turn for turn-dependent skills')
   if condition:hit+=amount;avoid+=amount
 typ=enemy['weapon']['weapon_type'] if enemy.get('weapon') else None
 if typ and typ+'breaker' in s:hit+=50;avoid+=50
 if 'aggressor' in s and initiates:attack+=10
 extra=u.get('combat_bonuses',{})
 return {'hit':hit+extra.get('hit',0),'avoid':avoid+extra.get('avoid',0),'crit':crit+extra.get('crit',0),'crit_avoid':extra.get('crit_avoid',0),'attack':attack+extra.get('attack',0)}

def forecast(a,b,initiates,context):
 w=a['weapon'];distance=context.get('distance',1)
 if not in_range(w,distance):return {'can_attack':False,'scheduled_hits':0}
 aw=copy.deepcopy(w);bw=copy.deepcopy(b.get('weapon'))
 if bw:bw['rank']=b.get('weapon_rank','E')
 tri,_=triangle(aw,bw)
 rank_attack,rank_hit=rank_bonus(w['weapon_type'],a.get('weapon_rank','E'))
 if tri[1]<0:rank_attack=rank_hit=0
 am=modifiers(a,b,initiates,context);bm=modifiers(b,a,not initiates,context)
 stat=a['stats']['mag' if w['damage_type']=='magical' else 'str']
 defense=b['stats']['res' if w['damage_type']=='magical' else 'def']
 terrain=b.get('terrain',{})
 defense+=terrain.get('res' if w['damage_type']=='magical' else 'def',0)
 effectiveness=set(w.get('effectiveness',[]))
 if 'conquest' in b.get('skills',[]):effectiveness-={'beast','armour'}
 if 'iotes_shield' in b.get('skills',[]):effectiveness-={'flying'}
 effective=bool(effectiveness&set(b.get('weaknesses',[])))
 attack=stat+w['might']*(3 if effective else 1)+rank_attack+am['attack']
 damage=max(0,attack+tri[0]-defense)
 hit=clamp(w['hit']+(3*a['stats']['skl']+a['stats']['lck'])//2+rank_hit+tri[1]+am['hit']-(3*b['stats']['spd']+b['stats']['lck'])//2-bm['avoid']-terrain.get('avoid',0))
 crit_raw=w['crit']+a['stats']['skl']//2+am['crit']-b['stats']['lck']-bm['crit_avoid']
 crit=clamp(crit_raw+(20 if 'wrath' in a.get('skills',[]) and a['current_hp']*2<=a['stats']['hp'] else 0))
 double=a['stats']['spd']-b['stats']['spd']>=5;hits=(2 if w.get('brave') else 1)*(2 if double else 1)
 if a.get('remaining_uses') is not None and a['remaining_uses']<hits:raise ValueError('Weapon may break during combat; unsupported, supply observed forecast')
 if 'hawkeye' in a.get('skills',[]):hit=100
 return {'can_attack':True,'attack_with_triangle':attack+tri[0],'defense_used':defense,'displayed_attack':attack,'damage':damage,'damage_scope':'Nominal hit without offensive/defensive procs; full results are in outcome','critical_damage':damage*3,'displayed_hit':hit,'true_hit_probability':true_hit(hit),'crit_raw_base':crit_raw,'crit_percent':crit,'doubles':double,'scheduled_hits':hits,'effective':effective,'expected_damage_per_scheduled_hit':true_hit(hit)*damage*(1+2*crit/100)}

def calculate(payload):
 if type(payload.get('context',{}).get('distance',1)) is not int or payload.get('context',{}).get('distance',1)<1:raise ValueError('Distance must be a positive integer')
 a,b=prepare(payload['attacker']),prepare(payload['defender']);context=payload.get('context',{})
 fa,fb=forecast(a,b,True,context),forecast(b,a,False,context)
 if not fa['can_attack']:raise ValueError('Attacker cannot initiate at the supplied range')
 result={'scope':'Supported single duel; effective stats supplied; independent uniform RNG model','source_ids':['calculations','true_hit','p2_skills_game_descriptions_0'],'attacker':fa,'defender':fb}
 if payload.get('partners'):
  result['outcome']=None;result['limitation']='Dual Strike/Guard battle outcome is not implemented; use pair_up.py for bonuses/rates. Do not infer survival from this forecast.'
 else:
  result['outcome']=distribution(a,b,fa,fb)
  result['lethal_risk']=result['outcome']['attacker_death_probability']>0
  result['certainty']='deterministic' if result['outcome']['deterministic'] else 'probability_distribution'
  result['assumptions']=['Effective displayed stats and weapon stats supplied; independent uniform random draws.','Possible outcomes include criticals and supported procs; expected HP is not a survival guarantee.']
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',help='Battle JSON file');args=p.parse_args()
 try:dump(calculate(read_json(args.input)))
 except (ValueError,KeyError) as e:p.exit(2,f'Cannot calculate reliably: {e}\n')
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Awakening EXP for explicitly known internal levels and enemy categories.
Repeated Lunatic engagements refuse by default because the published signed formula conflicts with its explanation.
"""
import argparse,math
from common import DIFFICULTIES,dump,read_json,lookup
CLASS_BONUS={'thief':20,'assassin':20,'trickster':20,'conqueror':20,'revenant':80,'entombed':80,'troubadour':-10,'cleric':-10,'priest':-10}
def multiplier(p):return (1.5 if p.get('veteran_active') else 1)*(2 if p.get('paragon') else 1)
def check(p):
 if p.get('difficulty') not in DIFFICULTIES:raise ValueError('Explicit difficulty required')
 if type(p.get('internal_level')) is not int or p['internal_level']<1:raise ValueError('Supply known positive internal_level; do not guess seal history')
def battle(p):
 check(p)
 for k in ('enemy_level','engagement_count'):
  if type(p.get(k)) is not int or p[k]<1:raise ValueError('Positive '+k+' required')
 if p.get('role','lead') not in ('lead','support'):raise ValueError('Role must be lead/support')
 if type(p.get('enemy_promoted')) is not bool:raise ValueError('Explicit enemy_promoted required; special classes count unpromoted')
 lookup('classes',p['enemy_class'])
 if 'unit_bonus' not in p or type(p.get('boss')) is not bool:raise ValueError('Explicit unit_bonus category and boss flag required')
 t=p['engagement_count'];luna=p['difficulty'] in ('Lunatic','Lunatic+')
 if luna and t>=4 and not p.get('allow_interpreted_lunatic_penalty'):raise ValueError('Repeated Lunatic EXP penalty sign unresolved in printed formula; use observed EXP or explicitly opt into documented interpretation')
 ld=p['enemy_level']+(20 if p['enemy_promoted'] else 0)-p['internal_level']
 hit=(31+ld)//3 if ld>=0 else 10 if ld==-1 else max((33+ld)//3,1)
 hit=max(0,hit-(max(t-3,0) if luna else 0))
 cb=CLASS_BONUS.get(p.get('enemy_class'),0);ub=p.get('unit_bonus')
 if ub not in (None,0,20):raise ValueError('unit_bonus must be null (ordinary), 0 (Harvest Scramble), or 20 (Deadlord/Einherjar)')
 bonus=(cb if ub is None else min(ub+cb,ub))+(20 if p.get('boss') else 0)
 kill=20+ld*3+bonus if ld>=0 else 20+bonus if ld==-1 else max(26+ld*3+bonus,7)
 if not p.get('damaged',False):base=0
 elif p.get('role','lead')=='support':base=hit*(1 if p.get('support_final_blow') else .5)
 else:base=hit+(kill if p.get('killed') else 0)
 # Separate flooring of half-support and combined multipliers has not been independently established.
 mult=multiplier(p)
 if base and (base!=int(base) or mult!=1) and not p.get('allow_unverified_rounding'):raise ValueError('Fractional support/Veteran/Paragon rounding order lacks worked confirmation; supply observed EXP or opt in')
 result=max(1,min(100,math.floor(base*mult))) if base else 0
 return {'exp':result,'level_difference':ld,'damage_component':hit,'kill_component':kill,'character_bonus':bonus,'base_before_modifiers':base,'multiplier':mult,'verification':'interpreted' if (luna and t>=4) or (base and (base!=int(base) or mult!=1)) else 'source_formula_with_empirical_examples','source_ids':['calculations','p2_exp_empirical'],'limitations':['No automatic category inference from map name. Do not use level-template data for unknown enemy level.','EXP award for chip followed by support kill versus lead kill must be supplied explicitly.']}
def staff(p):
 check(p)
 if p.get('kind') not in ('staff','dance'):raise ValueError('kind staff/dance required')
 if type(p.get('base_exp',17 if p['kind']=='dance' else None)) is not int:raise ValueError('Known staff base_exp required')
 if type(p.get('ordinary_unpromoted')) is not bool:raise ValueError('ordinary_unpromoted required; Dancer/special classes false')
 if p['kind']=='dance' and p['ordinary_unpromoted']:raise ValueError('Dancer never gets ordinary-unpromoted bonus')
 il=p['internal_level'];base=17 if p['kind']=='dance' else p['base_exp']
 bonus={'Normal':8,'Hard':3,'Lunatic':0,'Lunatic+':0}[p['difficulty']] if p['ordinary_unpromoted'] else 0
 adjust=-1 if il in (8,11) else 1 if il==30 else 0
 penalty=math.ceil(max(il-5,0)/3)
 raw=base-penalty+bonus+adjust
 if multiplier(p)!=1 and not p.get('allow_unverified_rounding'):raise ValueError('EXP multiplier rounding not independently confirmed')
 return {'exp':max(1,min(100,math.floor(raw*multiplier(p)))),'base_exp':base,'unpromoted_bonus':bonus,'level_penalty':penalty,'exception':adjust,'source_ids':['calculations','p2_exp_staff_empirical'],'verification':'empirical_rounding_interpretation' if multiplier(p)==1 else 'rounding_interpretation'}
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input');p=read_json(parser.parse_args().input)
 try:dump(staff(p) if p.get('kind') in ('staff','dance') else battle(p))
 except (ValueError,KeyError) as e:parser.exit(2,str(e)+'\n')
if __name__=='__main__':main()

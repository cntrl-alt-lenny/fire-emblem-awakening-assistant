#!/usr/bin/env python3
"""Pair bonuses from RAW support stats; dual rates from EFFECTIVE lead/partner stats."""
import argparse
from common import STATS,lookup,read_json,dump
STRIKE={'none':20,'C':30,'B':40,'A':50,'S':60}
GUARD={'none':0,'C':2,'B':5,'A':7,'S':10}
DUAL={'hit':[10,10,10,10,15,15,15,15,20,20,20,20],'avoid':[0,10,10,10,10,15,15,15,15,20,20,20],'crit':[0,0,0,10,10,10,10,15,15,15,15,20],'crit_avoid':[0,0,10,10,10,10,15,15,15,15,20,20]}
def pair_bonus(class_id,raw_stats,rank='none'):
 if rank not in STRIKE:raise ValueError('Invalid support rank')
 c=lookup('classes',class_id)
 if 'pair_up_bonus' not in c:raise ValueError('Class Pair Up bonus not researched')
 result={};support=0 if rank=='none' else 1 if rank in ('C','B') else 2
 for stat in STATS[1:]+('mov',):
  base=c['pair_up_bonus'][stat]
  if stat!='mov' and (stat not in raw_stats or type(raw_stats[stat]) is not int or raw_stats[stat]<0):raise ValueError('Missing/invalid RAW stat '+stat)
  personal=0 if stat=='mov' else min(raw_stats[stat]//10,3)
  result[stat]=personal+base+(support if base and stat!='mov' else 0)
 return result

def dual_bonus(ranks,dual_support_plus=False):
 vals={'none':1,'C':2,'B':3,'A':4,'S':5}
 n=min(12,sum(vals[r] for r in ranks)+(4 if dual_support_plus else 0))
 return {k:(v[n-1] if n else 0) for k,v in DUAL.items()}

def dual_rates(lead,partner,rank='none',dual_strike_plus=False,dual_guard_plus=False):
 if rank not in STRIKE:raise ValueError('Invalid support rank')
 for stats in (lead,partner):
  if any(type(stats.get(k)) is not int or stats[k]<0 for k in ('skl','def','res')):raise ValueError('Effective Skill/Defense/Resistance must be nonnegative integers')
 return {'strike':min(100,(lead['skl']+partner['skl'])//4+STRIKE[rank]+10*dual_strike_plus),'physical_guard':min(100,(lead['def']+partner['def'])//4+GUARD[rank]+10*dual_guard_plus),'magical_guard':min(100,(lead['res']+partner['res'])//4+GUARD[rank]+10*dual_guard_plus)}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args();d=read_json(a.input)
 try:dump({'stat_bonuses':pair_bonus(d['partner_class'],d['partner_raw_stats'],d.get('rank','none')),'dual_support_combat_bonuses':dual_bonus(d.get('adjacent_support_ranks',[d.get('rank','none')]),d.get('dual_support_plus',False)),'dual_rates_percent':dual_rates(d['lead_effective_stats'],d['partner_effective_stats'],d.get('rank','none'),d.get('dual_strike_plus',False),d.get('dual_guard_plus',False)),'source_ids':['pair_support','pair_support_1','calculations'],'note':'Rates are probabilities; the support unit does not receive the lead unit Pair Up stat bonuses.'})
 except (KeyError,ValueError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

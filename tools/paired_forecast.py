#!/usr/bin/env python3
"""Apply Pair Up/Dual Support once, then return nominal forecast and dual rates.
Full paired HP outcome remains UNKNOWN. Leader input stats must be effective BEFORE this Pair Up.
"""
import argparse,copy
from common import dump,read_json,STATS
from pair_up import pair_bonus,dual_bonus,dual_rates
from combat_calculator import calculate

def preview(p):
 if p.get('leader_stats_include_pair_up') is not False:raise ValueError('Explicit leader_stats_include_pair_up=false required to prevent double counting')
 leader=copy.deepcopy(p['leader']);partner=p['partner'];enemy=p['enemy'];rank=p['support_rank']
 if partner.get('alive') is False:raise ValueError('Dead partner cannot Pair Up')
 bonus=pair_bonus(partner['class_id'],p['partner_raw_stats'],rank)
 for stat in STATS[1:]:leader['stats'][stat]+=bonus[stat]
 if 'defender' in leader.get('skills',[]):
  for stat in STATS[1:]:leader['stats'][stat]+=1
 ranks=[rank]+p.get('other_adjacent_support_ranks',[])
 # Dual Support+ holder applicability must be supplied from actual adjacent/paired units.
 combat=dual_bonus(ranks,p.get('dual_support_plus_active',False));existing=leader.get('combat_bonuses',{})
 leader['combat_bonuses']={k:existing.get(k,0)+v for k,v in combat.items()}
 skills=set(leader.get('skills',[]))|set(partner.get('skills',[]))
 rates=dual_rates(leader['stats'],partner['stats'],rank,'dual_strike_plus' in skills,'dual_guard_plus' in skills)
 payload={'attacker':leader if p.get('leader_initiates',True) else enemy,'defender':enemy if p.get('leader_initiates',True) else leader,'context':p.get('context',{}),'partners':['explicit_pair']}
 return {'pair_up_stat_bonus':bonus,'leader_effective_stats_after_pair_up':leader['stats'],'dual_support_combat_bonus':combat,'dual_rates_percent':rates,'forecast':calculate(payload),'full_paired_outcome':'UNKNOWN','warning':'Do not infer paired survival/kill certainty. Support weapon, dual attack ordering, healing and enemy procs need a full paired model. Enemy combat bonuses must be supplied separately.','source_ids':['pair_support','pair_support_1','calculations']}
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input');a=parser.parse_args()
 try:dump(preview(read_json(a.input)))
 except (ValueError,KeyError) as e:parser.exit(2,str(e)+'\n')
if __name__=='__main__':main()

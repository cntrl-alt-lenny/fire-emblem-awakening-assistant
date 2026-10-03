#!/usr/bin/env python3
"""Forge quote from absolute interval allocations, full-use Worth and previous allocation."""
import argparse
from common import lookup,dump
MULTIPLIER=(0,.5,1.5,3,5,7.5)
def quote(weapon,intervals,previous=(0,0,0)):
 w=lookup('weapons',weapon)
 for allocation in [intervals,previous]:
  if len(allocation)!=3 or any(type(i) is not int or not 0<=i<=5 for i in allocation) or sum(allocation)>8:raise ValueError('0..5 intervals per stat; eight total')
 if any(x<y for x,y in zip(intervals,previous)):raise ValueError('Forge intervals cannot be removed')
 if not w['worth'] or w['id']=='mire':raise ValueError('Weapon cannot be forged')
 if w['crit']+3*intervals[2]>50:raise ValueError('Forged critical maximum is 50')
 cost=w['worth']*sum(MULTIPLIER[x]-MULTIPLIER[y] for x,y in zip(intervals,previous))
 if cost!=int(cost):raise ValueError('Fractional-gold rounding unverified for this Worth')
 w=dict(w);w.update(might=w['might']+intervals[0],hit=w['hit']+5*intervals[1],crit=w['crit']+3*intervals[2])
 return {'cost':int(cost),'allocation':intervals,'weapon':w,'source_ids':['items_2'],'limitation':'Enemy forges can exceed player limits. No inventory or gold is changed.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('weapon');p.add_argument('might',type=int);p.add_argument('hit',type=int);p.add_argument('crit',type=int);p.add_argument('--previous',nargs=3,type=int,default=[0,0,0]);a=p.parse_args()
 try:dump(quote(a.weapon,[a.might,a.hit,a.crit],a.previous))
 except ValueError as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

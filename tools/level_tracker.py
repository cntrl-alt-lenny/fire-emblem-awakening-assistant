#!/usr/bin/env python3
"""Record reported gains atomically, with explicit growth assumptions."""
import argparse,copy
from common import STATS,lookup,read_json,dump
from roster_tracker import DEFAULT,mutate,now
from average_stats import growths

def level_up(run,unit,gains,base_growths=None):
 key=lookup('characters',unit)['id'];u=run['units'][key]
 if not u['alive']:raise ValueError('Cannot level up a dead unit')
 if u['stats_basis']!='raw':raise ValueError('Normalize displayed stats to raw before growth analysis')
 c=lookup('classes',u['class_id'])
 if u['level']>=c['level_cap']:raise ValueError('Already at class level cap')
 if any(s not in STATS or type(v) is not int or v<0 for s,v in gains.items()):raise ValueError('Gains must be nonnegative integers on valid stats')
 before=copy.deepcopy(u['stats']);g=growths(key,u['class_id'],u.get('gender'),base_growths,'aptitude' in u.get('skills',[]))
 for stat,v in gains.items():
  if v>(g[stat]+99)//100:raise ValueError('Reported gain exceeds growth-model maximum; use state correction for boosters or uncertain data')
  u['stats'][stat]+=v
 u['level']+=1;u['exp']=0
 event={'kind':'level_up','time':now(),'class_id':u['class_id'],'level':u['level'],'before_stats':before,'after_stats':copy.deepcopy(u['stats']),'gains':{s:gains.get(s,0) for s in STATS},'growths':g,'expected_uncapped_gains':{s:g[s]/100 for s in STATS},'note':'Growth means are expectations, never guaranteed gains. Capped stats require cap-aware comparison.'}
 u['history'].append(event);return run

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--state',default=str(DEFAULT));p.add_argument('unit');p.add_argument('gains',nargs='*',help='hp=1 str=1 skl=1; omitted stats gained zero');p.add_argument('--base-growths',help='JSON object for resolved Robin/child personal growths');a=p.parse_args()
 try:
  gains=dict((s,int(v)) for s,v in (x.split('=') for x in a.gains));override=read_json(a.base_growths) if a.base_growths else None
  r=mutate(a.state,'level_up','Player-reported level-up',lambda r:level_up(r,a.unit,gains,override));dump(r['units'][lookup('characters',a.unit)['id']]['history'][-1])
 except (ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

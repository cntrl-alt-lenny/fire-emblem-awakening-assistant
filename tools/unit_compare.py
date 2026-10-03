#!/usr/bin/env python3
"""Compare an actual unit to a supplied cap-aware average projection."""
import argparse,math
from common import lookup,read_json,dump,STATS
from roster_tracker import DEFAULT,state_path
from average_stats import project

def compare(unit,projection):
 if unit['stats_basis']!='raw':raise ValueError('Raw stats required')
 if not projection['path']:raise ValueError('Projection needs at least one class segment, including zero level-ups if applicable')
 if projection.get('final_displayed_level') is None:raise ValueError('Supply starting_level to ensure comparison at the actual level')
 if projection['final_displayed_level']!=unit['level']:raise ValueError('Projection ends at a different displayed level')
 if projection['path'][-1]['class_id']!=unit['class_id']:raise ValueError('Projection ends in a different class')
 out={}
 for s in STATS:
  a=unit['stats'][s];e=projection['stats'][s];sd=e['standard_deviation'];delta=a-e['mean']
  out[s]={'actual':a,'mean':e['mean'],'difference':delta,'standard_deviations':delta/sd if sd else None,'interpretation':'No random variance in this model' if not sd else 'unusual (over two standard deviations)' if abs(delta)>2*sd else 'within two standard deviations'}
 return out

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--state',default=str(DEFAULT));p.add_argument('unit');p.add_argument('projection_input');a=p.parse_args()
 try:
  u=read_json(state_path(a.state))['units'][lookup('characters',a.unit)['id']];d=read_json(a.projection_input)
  if lookup('characters',d['character'])['id']!=u['id']:raise ValueError('Projection character mismatch')
  dump({'alive':u['alive'],'comparison':compare(u,project(d)),'note':'Compare equivalent permanent stats and the actual class path; equipment, skills and boosters can explain apparent deviations.'})
 except (ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

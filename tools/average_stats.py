#!/usr/bin/env python3
"""Exact per-stat capped growth distributions along an explicitly supplied class path.
Averages do not predict any specific level-up. Internal level controls EXP, not stat growth.
"""
import argparse,math
from collections import defaultdict
from common import STATS,DIFFICULTIES,lookup,read_json,dump
ASSET_STATS={'HP':'hp','Strength':'str','Magic':'mag','Skill':'skl','Speed':'spd','Luck':'lck','Defence':'def','Resistance':'res'}
def growths(character,class_id,gender=None,base_override=None,aptitude=False):
 char=lookup('characters',character);cl=lookup('classes',class_id)
 base=base_override if base_override is not None else char['base_growths']
 if character in ('robin','Avatar','Robin') and base_override is None:raise ValueError('Robin requires resolved asset/flaw base_growths')
 if base is None:raise ValueError('Resolve child parent-dependent base growths first')
 mod=cl.get('growth_modifiers')
 if cl['id']=='taguel':
  if gender not in ('M','F'):raise ValueError('Taguel growths require gender')
  mod=cl['growth_modifiers_by_gender'][gender]
 if mod is None:raise ValueError('Class growths unknown')
 return {s:base[s]+mod[s]+(20 if aptitude else 0) for s in STATS}
def internal_level(level,promoted,cumulative):return level+(20 if promoted else 0)+cumulative

def second_seal_cumulative(level,promoted,cumulative,difficulty):
 if difficulty not in DIFFICULTIES:raise ValueError('Invalid difficulty')
 cap={'Normal':20,'Hard':30,'Lunatic':50,'Lunatic+':50}[difficulty]
 return min(cap,cumulative+(level+(20 if promoted else 0)-1)//2)

def distribution_step(dist,growth,cap,base):
 """dist keys are retained personal offsets; class display can hide surplus at cap."""
 guaranteed,rem=divmod(growth,100);p=rem/100;out=defaultdict(float)
 for offset,q in dist.items():
  if offset+base>=cap:out[offset]+=q;continue
  for gain,prob in ((guaranteed,1-p),(guaranteed+1,p)):
   out[min(offset+gain,cap-base)]+=q*prob
 return dict(out)

def project(d):
 ch=lookup('characters',d['character']);current=lookup('classes',d['starting_class']);stats=d['starting_raw_stats']
 if set(stats)!=set(STATS):raise ValueError('Supply all eight starting raw stats')
 capmods=d.get('cap_modifiers',ch['cap_modifiers'])
 if capmods is None:raise ValueError('Resolved cap modifiers required for Robin/children')
 offsets={s:{stats[s]-current['base_stats'][s]:1.0} for s in STATS}
 total=0;path=[];display_level=d.get('starting_level')
 if display_level is not None and (type(display_level) is not int or not 1<=display_level<=current['level_cap']):raise ValueError('Invalid starting level')
 for segment in d['segments']:
  new=lookup('classes',segment['class_id']);levels=segment['level_ups']
  if type(levels) is not int or levels<0 or levels>=new['level_cap']:raise ValueError('Invalid number of level-ups in a class segment')
  if new['id']!=current['id']:
   if segment.get('change') not in ('promotion','reclass'):raise ValueError('Class transition needs change=promotion/reclass')
   if segment['change']=='promotion' and new['id'] not in current['promotes_to']:raise ValueError('Invalid promotion link')
   if segment['change']=='reclass' and ch['class_set_condition'] is None and new['id'] not in ch['class_set'] and not any(new['id'] in lookup('classes',c)['promotes_to'] for c in ch['class_set']):raise ValueError('Class not in researched character class set')
  if display_level is not None:
   if segment.get('change') in ('promotion','reclass'):display_level=1
   display_level+=levels
   if display_level>new['level_cap']:raise ValueError('Path exceeds displayed level cap')
  if new['caps'] is None:raise ValueError('Caps unknown')
  g=growths(ch['id'],new['id'],d.get('gender'),d.get('base_growths'),segment.get('aptitude',False))
  for s in STATS:
   cap=new['caps'][s]+capmods.get(s,0)
   for _ in range(levels):offsets[s]=distribution_step(offsets[s],g[s],cap,new['base_stats'][s])
  total+=levels;current=new;path.append({'class_id':new['id'],'level_ups':levels,'growths':g})
 result={}
 for s in STATS:
  cap=current['caps'][s]+capmods.get(s,0);base=current['base_stats'][s]
  display=defaultdict(float)
  for n,p in offsets[s].items():display[min(cap,max(0,n+base))]+=p
  mean=sum(n*p for n,p in display.items());variance=sum((n-mean)**2*p for n,p in display.items())
  result[s]={'mean':mean,'standard_deviation':math.sqrt(variance),'cap':cap,'distribution':dict(sorted(display.items()))}
 return {'stats':result,'path':path,'total_level_ups':total,'final_displayed_level':display_level,'basis':'raw permanent stats','source_ids':['character_growths','class_details_1','class_details','inheritance_1','class_details_2'],'limitations':['Specified class path does not infer seal eligibility, levels already gained, or available seal inventory.','Per-stat marginals; empty-level rerolls and correlations are not modeled.','Caps are retained across class changes as hidden personal offsets; no skills/equipment/temp boosts in displayed estimates.','Internal level and EXP scaling affect how many levels are attainable; they do not replace level-up counts.']}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
 try:dump(project(read_json(a.input)))
 except (ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

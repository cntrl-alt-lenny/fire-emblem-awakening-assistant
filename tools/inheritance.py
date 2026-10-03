#!/usr/bin/env python3
"""Resolve Avatar modifiers and child personal growth/cap formulas; no inferred parentage."""
import argparse,json
from common import ROOT,STATS,lookup,read_json,dump

def avatar(asset,flaw):
 if asset==flaw:raise ValueError('Asset and flaw must differ')
 a=json.loads((ROOT/'data/characters/avatar.json').read_text())['records'][0]
 if asset not in a['modifiers'] or flaw not in a['modifiers']:raise ValueError('Unknown asset/flaw')
 result={}
 for field,start in [('growth_modifiers',a['unmodified_growths']),('cap_modifiers',{s:0 for s in STATS[1:]})]:
  result['base_growths' if field=='growth_modifiers' else field]={s:start[s]+a['modifiers'][asset][field]['asset'][s]+a['modifiers'][flaw][field]['flaw'][s] for s in start}
 bases=a['unmodified_bases'].copy()
 for stat,side in [(asset,0),(flaw,1)]:bases[stat]+=a['base_asset_flaw_changes'][stat if stat in ['hp','lck'] else 'other'][side]
 result.update(starting_raw_stats=bases,asset=asset,flaw=flaw,source_ids=a['source_ids']);return result

def child(d):
 ch=lookup('characters',d['child'])
 if ch['category']!='child':raise ValueError('Not a child unit')
 parents=d['parents']
 if len(parents)!=2:raise ValueError('Supply two resolved parents')
 for p in parents:
  for field,keys in [('base_growths',STATS),('cap_modifiers',STATS[1:])]:
   if set(p[field])!=set(keys) or any(type(v) is not int for v in p[field].values()):raise ValueError('Parent '+field+' must be resolved numerical values')
 g={s:(parents[0]['base_growths'][s]+parents[1]['base_growths'][s]+ch['absolute_child_growths'][s])//3 for s in STATS}
 caps={s:parents[0]['cap_modifiers'][s]+parents[1]['cap_modifiers'][s]+(0 if d.get('robin_child_marriage') else 1) for s in STATS[1:]}
 return {'base_growths':g,'cap_modifiers':caps,'source_ids':['inheritance','inheritance_1','character_growths'],'limitations':['Parent compatibility, fixed parent, gender/class substitutions and inherited skills must be checked separately.','No recruitment-base estimate: actual parent raw stats and child auto-level treatment require further verification.','robin_child_marriage is true only when Robin marries a child-generation unit.']}
def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
 a=sub.add_parser('avatar');a.add_argument('asset');a.add_argument('flaw')
 c=sub.add_parser('child');c.add_argument('input');d=p.parse_args()
 try:dump(avatar(d.asset,d.flaw) if d.cmd=='avatar' else child(read_json(d.input)))
 except (ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

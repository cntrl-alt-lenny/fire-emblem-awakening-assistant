#!/usr/bin/env python3
"""Sequential supported duels with player HP carried across an explicit enemy attack order."""
import argparse,copy
from collections import defaultdict
from common import read_json,dump
from combat_calculator import calculate

def evaluate(payload):
 if payload.get('partners'):raise ValueError('Dual combat outcomes unsupported')
 player=payload['player']
 if player.get('remaining_uses') is not None:
  needed=sum(calculate({'attacker':entry['unit'],'defender':player,'context':entry.get('context',{})})['defender']['scheduled_hits'] for entry in payload['enemies'])
  if player['remaining_uses']<needed:raise ValueError('Player weapon may break across enemy-phase sequence; provide enough uses or calculate shorter sequence')
 states={player.get('current_hp',player['stats']['hp']):1.0};steps=[]
 for entry in payload['enemies']:
  new=defaultdict(float)
  for hp,prob in states.items():
   if hp==0:new[0]+=prob;continue
   p=copy.deepcopy(player);p['current_hp']=hp
   result=calculate({'attacker':entry['unit'],'defender':p,'context':entry.get('context',{})})
   for state in result['outcome']['states']:new[state['defender_hp']]+=prob*state['probability']
  states=dict(new);steps.append({'enemy':entry.get('label','enemy'),'death_probability':states.get(0,0),'expected_hp':sum(h*p for h,p in states.items())})
 return {'steps':steps,'final_hp_distribution':states,'death_probability':states.get(0,0),'minimum_possible_hp':min(h for h,p in states.items() if p>0),'limitations':['Enemy attack order, ranges, targets and effective stats must be supplied; this does not predict AI decisions.','No Dual Strikes/Guards, weapon breakage, EXP-triggered level-ups, terrain healing or unsupported skills.','Provided player durability must cover maximum scheduled retaliation across the whole phase; missing durability assumes enough uses.']}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
 try:dump(evaluate(read_json(a.input)))
 except (ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Verified Mend/Physic/Recover healing only; refuses unsupported staves and contexts."""
import argparse
from common import lookup,read_json,dump
RANKS='EDCBA'
def heal(p):
 staff=lookup('items',p['staff']);key=staff['id'];rank=p['weapon_rank']
 if rank not in RANKS or RANKS.index(rank)<RANKS.index(staff['rank']):raise ValueError('Staff rank requirement not met')
 if key not in ('mend','physic','recover'):raise ValueError('Healing coefficient not verified for this staff')
 for k in ('magic','current_hp','max_hp','distance','remaining_uses'):
  if type(p.get(k)) is not int or p[k]<0:raise ValueError('Nonnegative integer '+k+' required')
 if p['remaining_uses']<1:raise ValueError('Staff exhausted')
 if not 0<=p['current_hp']<=p['max_hp'] or p['max_hp']<1:raise ValueError('Invalid HP')
 if p['current_hp']==0:raise ValueError('Healing cannot revive a defeated unit')
 maximum=p['magic']//2 if key=='physic' else 1
 if not 1<=p['distance']<=maximum:raise ValueError('Target outside verified staff range')
 unknown=set(p.get('skills',[]))-{'healtouch'}
 if unknown:raise ValueError('Supply effective Magic; unsupported healing skills: '+', '.join(unknown))
 bonus={'E':0,'D':0,'C':1,'B':2,'A':3}[rank]+(5 if 'healtouch' in p.get('skills',[]) else 0)
 nominal=p['max_hp'] if key=='recover' else (15 if key=='mend' else 8)+p['magic']//2+bonus
 amount=min(p['max_hp']-p['current_hp'],nominal)
 return {'nominal_healing':nominal,'hp_restored':amount,'final_hp':p['current_hp']+amount,'range_max':maximum,'source_ids':['calculations','p2_mend' if key=='mend' else 'p2_physic' if key=='physic' else 'weapons_b_2','skills_extra'],'verification':'reference_formula','certainty':'deterministic'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
 try:dump(heal(read_json(a.input)))
 except (ValueError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

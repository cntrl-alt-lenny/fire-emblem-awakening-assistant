import sys,json,copy,types,subprocess
from pathlib import Path
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'tools'))
from tactical_combat import assess
original=types.ModuleType('original_gate');original.__file__=str(root/'tools/tactical_combat.py');exec(subprocess.check_output(['git','show','e78fa7bcc245071556a408f725105ac63ce7a8e9:tools/tactical_combat.py'],cwd=root,text=True),original.__dict__)
base=json.loads((root/'examples/battle.json').read_text());cases=leaks=controls=0
for side in ('attacker','defender'):
 for field,values in [('skills',[{},'',(),0,True,1.5,None,['vantage',3]]),('weaknesses',[{},'',(),0,True,1.5,None,['flying',3]]),('current_hp',[True,False,1.5,'1',None,[],{},0,-1,base[side]['stats']['hp']+1])]:
  for value in values:
   p=copy.deepcopy(base);p[side][field]=value;before=copy.deepcopy(p);r=assess(p);assert p==before;assert r['status']=='UNKNOWN' and r['outcome'] is None and r['safe_to_claim_survival'] is False,(side,field,value,r)
   assert side in str(r) and field in str(r),(side,field,r)
   leaks+=original.assess(p)['outcome'] is not None;cases+=1
 for hp in (1,base[side]['stats']['hp']):
  for skills in ([],['vantage'],['outdoor_fighter'],['odd_rhythm']):
   p=copy.deepcopy(base);p[side]['current_hp']=hp;p[side]['skills']=skills;p['context'].update(outdoors=False,turn=7);before=copy.deepcopy(p);assert assess(p)==original.assess(p);assert p==before;controls+=1
 p=copy.deepcopy(base);p[side]['weapon']='iron_sword' if side=='attacker' else 'iron_axe';assert assess(p)==original.assess(p);controls+=1
p=copy.deepcopy(base);p['defender'].update(weapon=None,weapon_state='unequipped',weapon_rank='E',remaining_uses=0);assert assess(p)==original.assess(p);controls+=1
print('Brain independent malformed cases:',cases,'; numerical leaks in baseline:',leaks,'; full supported controls unchanged:',controls)

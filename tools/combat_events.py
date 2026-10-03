"""Finite HP branches for verified isolated proc/passive interactions.
No paired battles or multi-hit proc chains. Unsupported combinations fail closed.
"""
from collections import defaultdict
PRIORITY=('sol','luna','ignis','vengeance')
DEFENSIVE={'pavise','aegis','miracle','pavise_plus','aegis_plus'}
EVENT_SKILLS=set(PRIORITY)|DEFENSIVE|{'vantage','vantage_plus','wrath','hawkeye','luna_plus','rightful_king','rightful_god'}
def validate(a,b):
 for u in (a,b):
  s=set(u.get('skills',[]))
  if len(s&DEFENSIVE)>1:raise ValueError('Multiple defensive procs/always-active guards: ordering not verified')
  active=[skill for skill in PRIORITY if skill in s]
  if len(active)>1 and activation(u,active[0])<1:raise ValueError('Multiple probabilistic offensive procs: shared versus separate RNG checks not independently verified')
  if 'luna_plus' in s and s&set(PRIORITY):raise ValueError('Luna+ with offensive proc ordering not verified')
 if (set(a.get('skills',[]))|set(b.get('skills',[])))&{'luna','luna_plus'} and any(any(u.get('terrain',{}).get(k,0) for k in ('def','res')) for u in (a,b)):raise ValueError('Luna interaction with terrain defense not verified')
def activation(u,skill):
 boost=(10 if 'rightful_king' in u.get('skills',[]) else 0)+(30 if 'rightful_god' in u.get('skills',[]) else 0)
 if skill=='miracle':rate=u['stats']['lck']
 elif skill=='vengeance':rate=2*u['stats']['skl']
 else:rate=u['stats']['skl']
 return min(100,rate+boost)/100

def branches(u,v,f,uh,vh):
 skills=set(u.get('skills',[]));defskills=set(v.get('skills',[]));off=[];remaining=1.0
 for skill in PRIORITY:
  if skill in skills:
   p=activation(u,skill);off.append((skill,remaining*p));remaining*=1-p
 off.append((None,remaining));damage=[]
 p=f['true_hit_probability'];crit=max(0,min(100,f['crit_raw_base']+(20 if 'wrath' in skills and uh*2<=u['stats']['hp'] else 0)))/100
 damage.append((0,0,1-p))
 for proc,q in off:
  if not q:continue
  d=f['damage']
  if proc=='luna' or 'luna_plus' in skills:d=max(0,f['attack_with_triangle']-f['defense_used']//2)
  elif proc=='ignis':d=max(0,f['attack_with_triangle']+u['stats']['str' if u['weapon']['damage_type']=='magical' else 'mag']//2-f['defense_used'])
  elif proc=='vengeance':d=max(0,f['attack_with_triangle']+(u['stats']['hp']-uh)//2-f['defense_used'])
  typ=u['weapon']['weapon_type'];guard='pavise' if typ in ('sword','lance','axe','stone','claw') and u['weapon']['damage_type']!='magical' else 'aegis' if typ in ('bow','tome','breath') else None
  # Levin/other magical melee weapons are still sword/lance/axe for Pavise.
  if typ in ('sword','lance','axe'):guard='pavise'
  if typ=='stone':
   wid=u['weapon'].get('id','')
   if 'beaststone' in wid:guard='pavise'
   elif 'dragonstone' in wid:guard='aegis'
   elif defskills&{'pavise','aegis','pavise_plus','aegis_plus'}:raise ValueError('Stone type needed to choose Pavise versus Aegis')
  for iscrit,cq in ((False,1-crit),(True,crit)):
   dealt=d*(3 if iscrit else 1)
   guardp=1 if guard and guard+'_plus' in defskills else activation(v,guard) if guard in defskills else 0
   for guarded,gq in ((False,1-guardp),(True,guardp)):
    if not gq:continue
    actual=dealt//2 if guarded else dealt
    mp=activation(v,'miracle') if 'miracle' in defskills and vh>1 and actual>=vh else 0
    for miracle,mq in ((False,1-mp),(True,mp)):
     inflicted=min(actual,vh-1 if miracle else vh)
     if proc=='sol' and actual>vh:raise ValueError('Sol overkill healing cap is unverified; supply observed result')
     heal=inflicted//2 if proc=='sol' else 0
     damage.append((inflicted,heal,p*q*cq*gq*mq))
 return damage

def distribution(a,b,fa,fb):
 validate(a,b);states={(a['current_hp'],b['current_hp']):1.0}
 order=[];sa=set(b.get('skills',[]))
 vantage=fb['can_attack'] and ('vantage_plus' in sa or ('vantage' in sa and b['current_hp']*2<=b['stats']['hp']))
 first=['b','a'] if vantage else ['a','b']
 for side in first:
  u,f=(a,fa) if side=='a' else (b,fb)
  if f['can_attack']:order.extend([side]*(2 if u['weapon'].get('brave') else 1))
 for side,u,f in [('a',a,fa),('b',b,fb)]:
  if f.get('doubles'):order.extend([side]*(2 if u['weapon'].get('brave') else 1))
 for side in order:
  nxt=defaultdict(float);u,v,f=(a,b,fa) if side=='a' else (b,a,fb)
  for (ah,bh),prob in states.items():
   if not ah or not bh:nxt[ah,bh]+=prob;continue
   uh,vh=(ah,bh) if side=='a' else (bh,ah)
   for d,heal,q in branches(u,v,f,uh,vh):
    if not q:continue
    unew=min(u['stats']['hp'],uh+heal);vnew=vh-d
    state=(unew,vnew) if side=='a' else (vnew,unew);nxt[state]+=prob*q
  states=dict(nxt)
 active=[(a,b,p) for (a,b),p in sorted(states.items()) if p>0]
 return {'order':order,'vantage_active':vantage,'attacker_death_probability':sum(p for a,b,p in active if a==0),'defender_death_probability':sum(p for a,b,p in active if b==0),'expected_attacker_hp':sum(a*p for a,b,p in active),'expected_defender_hp':sum(b*p for a,b,p in active),'minimum_possible_attacker_hp':min(a for a,b,p in active),'minimum_possible_defender_hp':min(b for a,b,p in active),'maximum_possible_attacker_hp':max(a for a,b,p in active),'maximum_possible_defender_hp':max(b for a,b,p in active),'deterministic':len(active)==1,'states':[{'attacker_hp':a,'defender_hp':b,'probability':p} for a,b,p in active]}

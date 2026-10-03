#!/usr/bin/env python3
"""Atomic JSON run-state tracker with immutable event history and process locking."""
import argparse,copy,fcntl,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
from common import ROOT,STATS,DIFFICULTIES,MODES,SPOILERS,lookup,slug,read_json,dump
DEFAULT=ROOT/'state/current_run.json'
def now():return datetime.now(timezone.utc).isoformat()
def state_path(path):
 p=Path(path).resolve()
 if ROOT not in p.parents:raise ValueError('Run files must be inside this project')
 return p

def validate_unit(u):
 lookup('characters',u['id']);lookup('classes',u['class_id'])
 if type(u.get('level')) is not int or not 1<=u['level']<=lookup('classes',u['class_id'])['level_cap']:raise ValueError('Invalid displayed level')
 if u.get('stats_basis') not in ('raw','displayed'):raise ValueError('stats_basis must be raw or displayed')
 if set(u.get('stats',{}))!=set(STATS) or any(type(x) is not int or x<0 for x in u['stats'].values()):raise ValueError('Supply all eight integer stats')
 if u.get('cumulative_level') is not None and (type(u['cumulative_level']) is not int or u['cumulative_level']<0):raise ValueError('Invalid cumulative level')
 if type(u.get('alive')) is not bool:raise ValueError('alive must be boolean')
 if len(u.get('skills',[]))>5:raise ValueError('At most five equipped skills')
 for s in u.get('skills',[]):lookup('skills',s)
 for typ,rank in u.get('weapon_ranks',{}).items():
  if typ not in ('sword','lance','axe','bow','tome','staff','stone'):raise ValueError('Unknown weapon type')
  if rank not in ('E','D','C','B','A',None):raise ValueError('Invalid weapon rank')
 instances=set()
 for item in u.get('inventory',[]):
  if item['instance_id'] in instances:raise ValueError('Duplicate inventory instance')
  instances.add(item['instance_id'])
  try:lookup('weapons',item['item_id'])
  except ValueError:lookup('items',item['item_id'])
  if item.get('remaining_uses') is not None and (type(item['remaining_uses']) is not int or item['remaining_uses']<0):raise ValueError('Invalid remaining uses')
 for k,r in u.get('supports',{}).items():
  lookup('characters',k)
  if r not in ('none','C','B','A','S'):raise ValueError('Invalid support rank')

def mutate(path,kind,note,fn):
 path=state_path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with open(str(path)+'.lock','a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  old=read_json(path) if path.exists() else None
  new=copy.deepcopy(old);new=fn(new)
  if new['difficulty'] not in DIFFICULTIES or new['mode'] not in MODES or new['spoiler_mode'] not in SPOILERS:raise ValueError('Invalid run settings')
  for u in new['units'].values():validate_unit(u)
  before={k:v for k,v in (old or {}).items() if k!='events'}
  after={k:v for k,v in new.items() if k!='events'}
  new.setdefault('events',[]).append({'sequence':len(new.get('events',[]))+1,'time':now(),'kind':kind,'note':note,'before':before,'after':copy.deepcopy(after)})
  new['updated_at']=now()
  fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.run-',suffix='.json')
  try:
   with os.fdopen(fd,'w') as f:json.dump(new,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
   os.replace(tmp,path)
  finally:
   if os.path.exists(tmp):os.unlink(tmp)
  return new

def initial(difficulty,mode,spoiler='Tactical spoilers'):
 return {'schema_version':1,'difficulty':difficulty,'mode':mode,'spoiler_mode':spoiler,'chapter':None,'turn':None,'gold':None,'convoy':[],'units':{},'events':[],'updated_at':None}

def upsert(run,unit,correction=False,note=''):
 unit=copy.deepcopy(unit);unit['id']=lookup('characters',unit['id'])['id'];unit['class_id']=lookup('classes',unit['class_id'])['id']
 k=unit['id'];existing=run['units'].get(k)
 if existing and existing['alive'] is False and unit.get('alive',False) is True and not(correction and note):raise ValueError('Dead unit cannot reappear; explicit --correct-alive with note required')
 merged=copy.deepcopy(existing) if existing else {'alive':True,'history':[],'weapon_ranks':{},'inventory':[],'skills':[],'supports':{},'exp':None,'stats_basis':'raw','gender':None,'cumulative_level':None}
 if existing and 'history' in unit and unit['history'][:len(existing['history'])]!=existing['history']:raise ValueError('History cannot be erased or rewritten by upsert')
 merged.update(unit);validate_unit(merged);run['units'][k]=merged;return run

def death(run,key):
 k=lookup('characters',key)['id'];u=run['units'][k]
 if run['mode']=='Casual':u['available_this_map']=False
 else:u['alive']=False
 u['history'].append({'kind':'defeated','time':now(),'mode':run['mode']});return run

def consume(run,key,instance,uses):
 u=run['units'][lookup('characters',key)['id']]
 if type(uses) is not int or uses<1:raise ValueError('Uses must be positive')
 item=next((x for x in u['inventory'] if x['instance_id']==instance),None)
 if item is None:raise ValueError('Inventory instance not found')
 if item.get('remaining_uses') is None:raise ValueError('Remaining uses unknown; report actual value first')
 if item['remaining_uses']<uses:raise ValueError('Cannot consume more uses than remain')
 item['remaining_uses']-=uses
 if item['remaining_uses']==0:u['inventory'].remove(item)
 return run

def class_change(run,key,new_class,actual_stats,kind):
 if kind not in ('promotion','reclass'):raise ValueError('Specify promotion or reclass')
 k=lookup('characters',key)['id'];u=run['units'][k]
 if not u['alive']:raise ValueError('Cannot change class of dead unit')
 target=lookup('classes',new_class);old=lookup('classes',u['class_id'])
 if kind=='promotion' and u['level']<10:raise ValueError('Master Seal promotion requires level 10')
 if kind=='reclass':
  if old['tier']!='promoted' and u['level']<10:raise ValueError('Second Seal requires level 10 in nonpromoted classes')
  if target['tier']=='promoted' and (old['tier']=='promoted' and u['level']<10 or old['tier']=='special' and u['level']<30 or old['tier']=='base'):raise ValueError('Promoted reclass target requires promoted level 10 or special level 30')
 if kind=='promotion' and target['id'] not in old['promotes_to']:raise ValueError('Invalid promotion')
 entry={'kind':kind,'time':now(),'from_class':u['class_id'],'from_level':u['level'],'before_stats':copy.deepcopy(u['stats']),'to_class':target['id'],'after_stats':copy.deepcopy(actual_stats),'seal_consumption':'Not inferred: record consumed seal separately'}
 if kind=='reclass' and u.get('cumulative_level') is not None:
  from average_stats import second_seal_cumulative
  u['cumulative_level']=second_seal_cumulative(u['level'],old['tier']=='promoted',u['cumulative_level'],run['difficulty'])
 entry['cumulative_level_after']=u.get('cumulative_level')
 u.update(class_id=target['id'],level=1,exp=0,stats=actual_stats);validate_unit(u);u['history'].append(entry);return run

def set_support(run,left,right,rank):
 a=lookup('characters',left)['id'];b=lookup('characters',right)['id']
 if a==b or rank not in ('none','C','B','A','S'):raise ValueError('Invalid support')
 for k,other in [(a,b),(b,a)]:
  u=run['units'][k]
  if rank=='S' and any(r=='S' and x!=other for x,r in u['supports'].items()):raise ValueError('A unit cannot have two S supports')
  u['supports'][other]=rank
 return run

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--state',default=str(DEFAULT));sub=p.add_subparsers(dest='cmd',required=True)
 init=sub.add_parser('init');init.add_argument('--difficulty',choices=DIFFICULTIES,required=True);init.add_argument('--mode',choices=MODES,required=True);init.add_argument('--spoiler-mode',choices=SPOILERS,default='Tactical spoilers')
 sub.add_parser('show')
 change=sub.add_parser('class-change');change.add_argument('unit');change.add_argument('class_id');change.add_argument('stats_json');change.add_argument('--kind',choices=['promotion','reclass'],required=True)
 support=sub.add_parser('support');support.add_argument('left');support.add_argument('right');support.add_argument('rank',choices=['none','C','B','A','S'])
 sub.add_parser('complete-map')
 add=sub.add_parser('upsert');add.add_argument('unit_json');add.add_argument('--correct-alive',action='store_true');add.add_argument('--note',default='Player-reported state')
 dead=sub.add_parser('death');dead.add_argument('unit');dead.add_argument('--note',default='Player reported defeat')
 use=sub.add_parser('consume');use.add_argument('unit');use.add_argument('instance');use.add_argument('--uses',type=int,default=1)
 setp=sub.add_parser('set');setp.add_argument('field',choices=['chapter','turn','gold','spoiler_mode']);setp.add_argument('value')
 a=p.parse_args()
 try:
  if a.cmd=='show':dump(read_json(state_path(a.state)));return
  def operation(run):
   if a.cmd=='init':
    if run is not None:raise ValueError('Run already exists. Use a new --state file to preserve it.')
    return initial(a.difficulty,a.mode,a.spoiler_mode)
   if run is None:raise ValueError('Initialize a run first')
   if a.cmd=='upsert':return upsert(run,read_json(a.unit_json),a.correct_alive,a.note)
   if a.cmd=='death':return death(run,a.unit)
   if a.cmd=='consume':return consume(run,a.unit,a.instance,a.uses)
   if a.cmd=='class-change':return class_change(run,a.unit,a.class_id,read_json(a.stats_json),a.kind)
   if a.cmd=='support':return set_support(run,a.left,a.right,a.rank)
   if a.cmd=='complete-map':
    for u in run['units'].values():
     if run['mode']=='Casual' and u['alive']:u['available_this_map']=True
    run['turn']=None;return run
   if a.cmd=='set':
    value=int(a.value) if a.field in ('turn','gold') else a.value
    if a.field=='chapter':lookup('chapters',value)
    if a.field=='turn' and value<1:raise ValueError('Turn starts at 1')
    if a.field=='gold' and value<0:raise ValueError('Gold cannot be negative')
    run[a.field]=value;return run
  r=mutate(a.state,a.cmd,getattr(a,'note','Player-reported update'),operation)
  dump({'state':str(state_path(a.state)),'event':len(r['events']),'units':len(r['units'])})
 except (ValueError,KeyError,FileNotFoundError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()

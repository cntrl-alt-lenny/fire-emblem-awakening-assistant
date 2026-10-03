#!/usr/bin/env python3
"""Deterministic offline normalization of retained factual tables. No web fetching."""
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATS=['hp','str','mag','skl','spd','lck','def','res']
def clean(s):
 return re.sub(r'\s*\*?_\{\d+\}', '',s).strip().replace('’',"'")
def ident(s):
 s=clean(s).replace('+',' plus ').replace("'",'')
 return re.sub(r'[^a-z0-9]+','_',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('_')
def cid(s):
 k=ident(s)
 return {'avatar':'robin','lonqu':'lon_qu','sayri':'say_ri','yenfay':'yen_fay'}.get(k,k)
def load(key,i=0):return json.loads((ROOT/'research'/f'{key}.json').read_text())[i]
def rows(page):
 for t in page['tables']:
  for row in t['rows']:yield t['section'],[clean(x) for x in row]
def write(path,records):
 (ROOT/'data'/path).write_text(json.dumps({'schema_version':1,'records':records},indent=2,ensure_ascii=False)+'\n')
def sourced(name,source):return {'id':ident(name),'name':clean(name),'source_ids':[source],'verification':'single_source_transcribed'}
def addsource(r,source,field):
 if source not in r['source_ids']:r['source_ids'].append(source)
 r.setdefault('field_sources',{})[field]=[source]
def classnames(s):
 if s=='Priest, Cleric':return ['Priest','Cleric']
 if s in ('War Monk/Cleric','War Monk, War Cleric'):return ['War Monk','War Cleric']
 if s=='Wyvern Rider/Lord':return ['Wyvern Rider','Wyvern Lord']
 if s=='Lord':return ['Lord (M)','Lord (F)']
 if s=='Great Lord':return ['Great Lord (M)','Great Lord (F)']
 result=[]
 for x in s.split(','):
  x=x.strip()
  result.extend(classnames(x) if x in ('Lord','Great Lord') else [x])
 return result
def classid(s,character=None):
 if s=='Lord':s='Lord (F)' if character=='lucina' else 'Lord (M)'
 return ident(s)
def number(s):
 if not re.fullmatch(r'[+-]?\d+',s):raise ValueError(s)
 return int(s)
def statcells(cells,keys=STATS):
 result={};boosts={}
 for k,x in zip(keys,cells):
  m=re.fullmatch(r'([+-]?\d+)(?:_\{([+-]?\d+)\})?',x)
  if not m:raise ValueError((k,x))
  result[k]=int(m[1])
  if m[2]:boosts[k]=int(m[2])
 return result,boosts

def main():
 classes={}
 p=load('foundation')
 for section,r in rows(p):
  if len(r)!=10 or not r[1].isdigit():continue
  name=r[0].replace(' *','')
  if '(shifted)' in name:continue
  for n in classnames(name):
   o=sourced(n,p['source_id']); o.update(base_stats=dict(zip(['hp','str','mag','skl','spd','def','res'],map(int,r[1:8]))),movement=int(r[8]),weapons=[ident(x) for x in r[9].split(', ')],starting_weapon_rank='E',caps=None,growth_modifiers=None,skills=[],promotes_to=[],promotes_from=[],gender_restriction=None)
   o['base_stats']['lck']=0;classes[o['id']]=o
 for section,r in rows(load('class_details')):
  if len(r)!=9 or not r[1].isdigit():continue
  for n in classnames(r[0]):
   if ident(n) not in classes:continue
   o=classes[ident(n)];o['caps']=dict(zip(STATS,map(int,r[1:])))
   o['tier']={'Non-promoted Classes':'base','Promoted Classes':'promoted','Special Classes':'special'}[section]
   addsource(o,'class_details','caps')
 for section,r in rows(load('class_details',1)):
  if len(r)!=8 or not r[1].isdigit():continue
  for n in classnames(r[0]):
   if ident(n) not in classes and n.startswith('Taguel ('):continue
   targets=[n]
   if n=='Taguel':targets=['Taguel']
   for target in targets:
    if ident(target) in classes:
     o=classes[ident(target)];o['growth_modifiers']=dict(zip(['hp','str','mag','skl','spd','def','res'],map(int,r[1:])));o['growth_modifiers']['lck']=0;addsource(o,'class_details_1','growth_modifiers')
 # Gender-specific Taguel growths must not collapse.
 classes['taguel']['growth_modifiers_by_gender']={}
 for section,r in rows(load('class_details',1)):
  if r[0] in ('Taguel (M)','Taguel (F)'):
   g=dict(zip(['hp','str','mag','skl','spd','def','res'],map(int,r[1:])));g['lck']=0
   classes['taguel']['growth_modifiers_by_gender'][r[0][-2]]=g
 for section,r in rows(load('pair_support')):
  if section!="Support Unit's Class Bonus" and section!='Support Unit’s Class Bonus':continue
  if len(r)!=9 or r[0]=='Class':continue
  for n in classnames(r[0]):
   if ident(n) in classes:
    o=classes[ident(n)];o['pair_up_bonus']=dict(zip(STATS[1:]+['mov'],[int(x or 0) for x in r[1:]]));addsource(o,'pair_support','pair_up_bonus')
 promotions={'Lord (M)':['Great Lord (M)'],'Lord (F)':['Great Lord (F)'],'Tactician':['Grandmaster'],'Cavalier':['Paladin','Great Knight'],'Knight':['General','Great Knight'],'Myrmidon':['Swordmaster','Assassin'],'Mercenary':['Hero','Bow Knight'],'Fighter':['Warrior','Hero'],'Barbarian':['Berserker','Warrior'],'Archer':['Sniper','Bow Knight'],'Thief':['Assassin','Trickster'],'Pegasus Knight':['Falcon Knight','Dark Flier'],'Wyvern Rider':['Wyvern Lord','Griffon Rider'],'Mage':['Sage','Dark Knight'],'Dark Mage':['Sorcerer','Dark Knight'],'Priest':['Sage','War Monk'],'Cleric':['Sage','War Cleric'],'Troubadour':['Valkyrie','War Cleric']}
 for n,ps in promotions.items():
  classes[ident(n)]['promotes_to']=list(map(ident,ps));addsource(classes[ident(n)],'class_sets_1','promotes_to')
  for target in ps:classes[ident(target)]['promotes_from'].append(ident(n))
 for k,o in classes.items():
  o.setdefault('tier','enemy_or_npc')
  o['level_cap']=30 if o['tier']=='special' else 20
  if k in ['fighter','barbarian','berserker','warrior','priest','war_monk','dread_fighter','lord_m','great_lord_m']:o['gender_restriction']='M'
  if k in ['pegasus_knight','falcon_knight','dark_flier','troubadour','valkyrie','cleric','war_cleric','bride','dancer','lord_f','great_lord_f']:o['gender_restriction']='F'
  o['availability']='DLC' if k in ['bride','dread_fighter'] else 'legacy_only' if k=='lodestar' else 'SpotPass' if k=='conqueror' else 'ordinary' if o['tier']!='enemy_or_npc' else 'enemy_or_npc'
 skills={}
 for section,r in rows(load('skills_extra')):
  if section!='Obtainable Skills' or len(r)!=6 or r[1]=='Skill':continue
  o=sourced(r[1],'skills_extra');o.update(effect=r[2],activation=r[3],learned_in=[],calculator_supported=False)
  for n in classnames(r[4]):
   if ident(n) in classes and r[5].isdigit():
    o['learned_in'].append({'class_id':ident(n),'level':int(r[5])});classes[ident(n)]['skills'].append({'skill_id':o['id'],'level':int(r[5])})
  skills[o['id']]=o
 chars={};last=None
 for section,r in rows(load('characters')):
  if not r or r[0]=='Name':continue
  if re.search(r'\([HL]\)$',r[0]):
   name=re.sub(r'_[{]([^}]+)[}]',r'\1',r[0]);k=cid(re.sub(r' \([HL]\)$','',name));o=chars[k]
   cells=[x for x in r[1:] if x!=''];st,boost=statcells(cells)
   d='Hard' if '(H)' in name else 'Lunatic';o['starting_stats_by_difficulty'][d]={'raw':st,'equipment_skill_bonuses':boost}
   if d=='Lunatic':o['starting_stats_by_difficulty']['Lunatic+']={'raw':st.copy(),'equipment_skill_bonuses':boost.copy()}
   continue
  if r[0]=='Morgan' and len(r)==14:r.insert(12,'Varies')
  if len(r)!=15:raise ValueError(('Character row width',r))
  k=cid(r[0]);st,boost=statcells(r[3:11]);o=sourced('Robin' if k=='robin' else r[0],'characters');o['id']=k
  o.update(starting_class_id=None if r[1]=='Varies' else classid(r[1],k),starting_level=int(r[2]),starting_stats_by_difficulty={},absolute_child_bases=st if section=='Children Characters' else None,base_growths=None,absolute_child_growths=None,cap_modifiers=None,recruitment=None,class_set=None,starting_inventory=[ident(x) for x in r[13].split(', ') if x not in ['–','Varies'] and not x.startswith('Varies')],starting_skills=[ident(x) for x in r[14].split(', ') if x!='Varies'],starting_weapon_ranks={},category='child' if section=='Children Characters' else 'SpotPass_story' if section=='SpotPass-exclusive Characters' else 'first_generation')
  if section!='Children Characters':
   for d in ['Normal','Hard','Lunatic','Lunatic+']:o['starting_stats_by_difficulty'][d]={'raw':st.copy(),'equipment_skill_bonuses':boost.copy()}
  for typ,rank,extra in re.findall(r'Image: Weapon Rank (\w+) ([EDCBA–])(?: \(\+(\d+)\))?',r[12]):o['starting_weapon_ranks'][typ.lower()]={'rank':None if rank=='–' else rank,'extra_wexp':int(extra or 0)}
  chars[k]=o
 for section,r in rows(load('character_growths')):
  if len(r)==9 and all(x.isdigit() for x in r[1:]) and section in ['Initial Characters','Children characters'] and cid(r[0]) in chars:
   k=cid(r[0]);o=chars[k];field='absolute_child_growths' if section=='Children characters' else 'base_growths';o[field]=dict(zip(STATS,map(int,r[1:])));addsource(o,'character_growths',field)
 for section,r in rows(load('inheritance',1)):
  if section=='Initial Characters' and len(r)==8 and cid(r[0]) in chars:
   o=chars[cid(r[0])];o['cap_modifiers']=dict(zip(STATS[1:],[int(x or 0) for x in r[1:]]));addsource(o,'inheritance_1','cap_modifiers')
 for section,r in rows(load('recruitment')):
  if len(r)==4 and cid(r[0]) in chars:
   o=chars[cid(r[0])];o['recruitment']={'chapter':r[2],'condition':r[3]};addsource(o,'recruitment','recruitment')
 for section,r in rows(load('class_sets')):
  if section in ['Class Sets','Children Characters'] and cid(r[0]) in chars:
   o=chars[cid(r[0])];o['class_set']=[classid(x,cid(r[0])) for x in r[1:] if ident(x) in classes or x=='Lord'];o['class_set_condition']= 'gender-compatible regular classes' if cid(r[0])=='robin' else 'includes additional inherited classes' if o['category']=='child' else None;addsource(o,'class_sets','class_set')
 # Known source typos are documented, never propagated as game facts.
 chars['yarne']['starting_weapon_ranks']={'stone':{'rank':None,'extra_wexp':0}}
 chars['nah']['starting_weapon_ranks']={'stone':{'rank':None,'extra_wexp':0}}
 weapons=[];items=[]
 for key,i,typ in [('weapons_a',0,'sword'),('weapons_a',1,'lance'),('weapons_a',2,'axe'),('weapons_b',0,'bow'),('weapons_b',1,'tome'),('items',0,'stone')]:
  p=load(key,i)
  for section,r in rows(p):
   if len(r)!=11 or not r[3].isdigit():continue
   o=sourced(r[1],p['source_id']);o.update(weapon_type=typ,rank=None if r[2]=='–' else r[2],might=int(r[3]),hit=int(r[4]),crit=int(r[5]),range=r[6],effectiveness=[ident(x.strip()) for x in re.findall(r'Image: ([A-Za-z ]+?)(?= Image:|$)',r[7])],uses=int(r[8]) if r[8].isdigit() else None,worth=int(r[9]) if r[9].isdigit() else None,effect=r[10],damage_type='magical' if typ=='tome' or r[1] in ['Levin Sword','Shockstick','Bolt Axe'] else 'physical',weight=None,weight_note='No weapon-weight attack-speed penalty in Awakening; doubling uses Speed.',special_effect_review='required' if r[10]!='–' else 'ordinary')
   if typ=='stone' and r[1] not in ['Beaststone','Beaststone+','Dragonstone','Dragonstone+']:o['weapon_type']='claw' if 'Claw' in r[1] else 'breath'
   o['brave']='Brave' in r[1] or ('twice' in r[10].lower() or '2 consecutive attacks' in r[10].lower())
   o['stat_bonuses']={}
   combined=re.search(r'Def and Res \+(\d+)',r[10])
   if combined:o['stat_bonuses'].update({'def':int(combined[1]),'res':int(combined[1])})
   for stat,v in re.findall(r'\b(Str|Mag|Skl|Skill|Spd|Lck|Luck|Def|Res) \+(\d+)',r[10]):o['stat_bonuses'][{'skill':'skl','luck':'lck'}.get(stat.lower(),stat.lower())]=int(v)
   weapons.append(o)
 p=load('weapons_b',2)
 for section,r in rows(p):
  if len(r)==8 and r[4].isdigit():
   o=sourced(r[1],p['source_id']);o.update(item_type='staff',weapon_type='staff',rank=r[2],range=r[3],uses=int(r[4]),worth=int(r[5]) if r[5].isdigit() else None,base_exp=int(r[6]),effect=r[7]);items.append(o)
 for section,r in rows(load('items',1)):
  if len(r)==5 and (r[2].isdigit() or r[2]=='–'):
   o=sourced(r[1],'items_1');o.update(item_type='valuable' if r[1].startswith('Bullion') else 'consumable_or_key',uses=int(r[2]) if r[2].isdigit() else None,worth=int(r[3]) if r[3].isdigit() else None,effect=r[4],sell_price=int(re.search(r'[0-9,]+',r[4])[0].replace(',','')) if r[4].startswith('Sells for') else None);items.append(o)
 chapters=[]
 for section,r in rows(load('chapter_catalog')):
  if section in ['Main story','Paralogues'] and len(r)==6 and r[0]:
   label=r[0];k='chapter_'+re.search(r'\d+',label)[0] if label.startswith('Chapter') else 'paralogue_'+re.search(r'\d+',label)[0] if label.startswith('Paralogue') else ident(label)
   o=sourced(r[1],'chapter_catalog');o['id']=k;o.update(kind='paralogue' if section=='Paralogues' else 'main',number=int(re.search(r'\d+',label)[0]) if re.search(r'\d+',label) else None,label=label,objective=r[2],defeat_condition=r[3],recruitable_units=[cid(x.strip()) for x in r[4].split(',') if x.strip()!='None'],bosses=[x.strip() for x in r[5].split(',')],deployment_limit=None,map_dimensions=None,terrain=None,chests=None,villages=None,doors=None,events=None,difficulty_data={d:{'status':'not_researched','enemies':None,'reinforcements':None} for d in ['Normal','Hard','Lunatic','Lunatic+']});chapters.append(o)
  elif section.startswith('Series ') and len(r)==5 and r[0]!='Title':
   o=sourced(r[0],'chapter_catalog');o['id']='dlc_'+o['id'];o.update(kind='DLC',number=None,label=r[0],objective=r[1].replace('emeny','enemy'),defeat_condition=r[2],recruitable_units=[],legacy_rewards=[x.strip() for x in r[3].split(',') if x.strip()!='None'],bosses=[r[4]],deployment_limit=None,difficulty_data={d:{'status':'not_researched','enemies':None,'reinforcements':None} for d in ['Normal','Hard','Lunatic','Lunatic+']});chapters.append(o)
 write('classes/classes.json',list(classes.values()));write('characters/characters.json',list(chars.values()));write('skills/skills.json',list(skills.values()));write('weapons/weapons.json',weapons);write('items/items.json',items);write('chapters/chapters.json',chapters)
 # Canonical grouped systems tables preserve rowspan gaps until semantic normalization.
 for key,indices,out in [('economy',[0,1,2],'items/economy.json'),('support_growth',[0,1],'supports/support_growth.json'),('locations',[1,2],'mechanics/availability_and_barracks.json'),('other_systems',[1,2],'mechanics/world_and_boosts.json')]:
  records=[]
  for i in indices:
   p=load(key,i)
   for j,t in enumerate(p['tables']):records.append({'id':f'{p["source_id"]}_{j}','name':t['section'],'source_ids':[p['source_id']],'verification':'extracted_unreviewed','rows':t['rows']})
  write(out,records)
 sources=[];seen=set()
 for path in sorted((ROOT/'research').glob('*.json')):
  if path.name in ['audit.json']:continue
  content=json.loads(path.read_text())
  if not isinstance(content,list):continue
  for p in content:
   if 'source_id' not in p:continue
   if p['source_id'] in seen:continue
   seen.add(p['source_id']);sources.append({'id':p['source_id'],'name':p['name'],'url':p['url'],'accessed':p['accessed'],'scope':[t['section'] for t in p['tables']],'limitations':'Public web reader factual-table extraction. Single-source unless explicitly cross-checked. Row spans and conditional variants require review.','method':'public_web_reader','tables_retained':len(p['tables'])})
 (ROOT/'data/sources.json').write_text(json.dumps(sources,indent=2)+'\n')
 print(json.dumps({k:len(v) for k,v in [('classes',classes),('characters',chars),('skills',skills),('weapons',weapons),('items',items),('chapters',chapters)]},indent=2))
if __name__=='__main__':main()

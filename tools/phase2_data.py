#!/usr/bin/env python3
"""Offline, conservative normalization of phase-two factual extracts.
Never infer an absent wave, coordinates, random skill, forge or mode.
"""
import json,re
from pathlib import Path
from urllib.parse import unquote
from common import ROOT,STATS,DIFFICULTIES,slug,records
R=ROOT/'research/phase2'
def write(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def map_id(text):
 text=unquote(text).replace('_',' ').replace('\xa0',' ')
 m=re.search(r'(Chapter|Paralogue|Sidequest)\s*(\d+)\b',text,re.I)
 if m:return ('chapter_' if m[1].lower()=='chapter' else 'paralogue_')+m[2]
 for k in ('premonition','prologue','endgame'):
  if re.search(r'\b'+k+r'\b',text,re.I):return k
 return None
def numeric_rows(p):
 return sum(len(row)>=15 and re.fullmatch(r'\d+',row[2]) is not None for t in p['tables'] for row in t['rows'])
def main():
 sources=json.loads((ROOT/'data/sources.json').read_text());source_map={s['id']:s for s in sources}
 chapters=records('chapters');cm={c['id']:c for c in chapters}
 inventory=json.loads((R/'map_inventory.json').read_text());mids=[m['id'] for m in inventory]
 classes={c['id'] for c in records('classes')};weapons={c['id'] for c in records('weapons')};skills={c['id'] for c in records('skills')}
 best={};guides={};attempts=[]
 def register(p,scope):
  sid='p2_'+p['id']
  source_map[sid]={'id':sid,'name':p['name'],'url':p['url'],'accessed':p['accessed'],'scope':scope,'verification':'public_reference_partial','limitations':'Single-source extracted factual data; reader/search output may be incomplete. Same publisher is not independent confirmation. '+('Guide defaults to Hard; other modes require explicit evidence.' if 'gamerguides.com' in p['url'] else 'Lunatic tables do not establish Lunatic+ skills, positions or random rolls.')}
  return sid
 for f in sorted(R.glob('*.json')):
  d=json.loads(f.read_text())
  if not isinstance(d,list):continue
  for p in d:
   if not isinstance(p,dict) or 'tables' not in p:continue
   mid=map_id(p['name'])
   if mid in mids:attempts.append({'map_id':mid,'url':p.get('url'),'access_status':p.get('access_status'),'method':p.get('method')})
   if mid not in mids or not p.get('url'):continue
   if 'gamerguides.com' in p['url'] and 'fire-emblem-awakening' in p['url']:register(p,['Hard map reference; explicitly identified other-mode notes when present'])
   if 'Awakening LM Enemy Data:' in p['name'] and numeric_rows(p)>numeric_rows(best.get(mid,{'tables':[]})):best[mid]=p
   if 'gamerguides.com' in p['url'] and 'fire-emblem-awakening' in p['url']:
    # Aggregate search pages have unrelated map headings; select only matching subsection.
    valid=[t for t in p['tables'] if map_id(t.get('map_heading') or p['name'])==mid and ('Boss' in t['section'] or 'New Units' in t['section'])]
    limits=[x for x in p.get('factual_candidates',[]) if map_id(x.get('map_heading') or p['name'])==mid and re.match(r'Character Limit:',x['text'])]
    score=sum(len(t['rows']) for t in valid)+5*len(limits)
    if score>guides.get(mid,(0,None,None,None))[0]:guides[mid]=(score,p,valid,limits)
 enemies=[];waves=[];coverage=[];anomalies=[]
 for mid in mids:
  c=cm[mid]
  for mode in DIFFICULTIES:
   slot=c['difficulty_data'][mode]
   for key in ('map_reference','reported_absence','hazard_claims','conflicts','initial_enemy_ids'):slot.pop(key,None)
   slot.update({'status':'unresolved','enemies':None,'reinforcements':None,'coverage':{'starting_positions':'UNKNOWN','terrain':'UNKNOWN','interactables':'UNKNOWN','ai':'UNKNOWN','reinforcement_schedule':'unresolved'},'safe_for_tactical_certainty':False})
  # Hard reference metadata stays inside Hard slot; catalog objective is not overwritten.
  if mid in guides:
   _,p,ts,limits=guides[mid];sid=register(p,['Hard deployment/boss/recruitment reference'])
   meta={'source_ids':[sid],'verification':'single_source_partial','bosses':[],'recruitment_mentions':[],'deployment_limit':None}
   for x in limits:
    n=re.search(r'Character Limit:\s*(\d+)',x['text'])
    if n:meta['deployment_limit']=int(n[1]);meta['deployment_limit_includes_chrom']='Including Chrom' in x['text']
   for t in ts:
    for row in t['rows']:
     if len(row)==4 and row[2].isdigit():
      if 'Boss' in t['section']:meta['bosses'].append({'name':row[0],'class_name':row[1],'level':int(row[2]),'equipment_text':row[3],'equipment_stats':'UNKNOWN'})
      else:meta['recruitment_mentions'].append({'name':row[0],'class_name':row[1],'level':int(row[2]),'condition_text':row[3],'note':'May describe an earlier chapter; not proof of recruitment on this map.'})
   c['difficulty_data']['Hard'].update(status='partially_verified',map_reference=meta)
  if mid in best:
   p=best[mid];sid=register(p,['Lunatic representative enemy stats/classes/equipment/known skills; partial reinforcement timing'])
   initial=[];all_ids=[];rw=[]
   for ti,t in enumerate(p['tables']):
    section=t['section'];is_wave='Reinforcement' in section
    if section not in ('','Starting','Enemy','Reinforcements'):continue
    ids=[]
    for ri,row in enumerate(t['rows']):
     if len(row)!=15 or not row[2].isdigit():continue
     cid=slug(row[1]);cid={'valkrie':'valkyrie','lord':'lord_f','war_monk':'war_monk','war_cleric':'war_cleric'}.get(cid,cid)
     if cid not in classes:anomalies.append({'map_id':mid,'type':'unresolved_class','value':row[1],'source_ids':[sid]});continue
     if not all(re.fullmatch(r'\d+(?:\+\d+)?',v) for v in row[3:11]):anomalies.append({'map_id':mid,'type':'unparsed_stats','row':row,'source_ids':[sid]});continue
     raw={k:int(v.split('+')[0]) for k,v in zip(STATS,row[3:11])};bonus={k:int(v.split('+')[1]) for k,v in zip(STATS,row[3:11]) if '+' in v}
     equipment=[];inv=[]
     for value in row[13].split(','):
      value=value.strip();key=slug(value.rstrip('+'));equipment.append({'source_text':value,'item_id':key if key in weapons else None,'enemy_forge_marker':len(value)-len(value.rstrip('+')),'effective_weapon_stats':'UNKNOWN' if '+' in value else 'base_reference'})
      if key in weapons:inv.append(key)
     known=[];unknown=[]
     for value in row[14].split(','):
      value=value.strip();key=slug(value);key={'defense_plus_2':'defence_plus_2'}.get(key,key)
      if key in skills:known.append(key)
      elif value not in ('-','–',''):unknown.append(value)
     eid=f'{mid}_lunatic_t{ti}_r{ri}'
     e={'id':eid,'name':row[0],'chapter_id':mid,'difficulty':'Lunatic','class_id':cid,'source_class_name':row[1],'level':int(row[2]),'stats':raw,'source_stat_bonuses':bonus,'effective_stats':{k:raw[k]+bonus.get(k,0) for k in STATS},'stats_interpretation':'Representative source values; + annotations retained separately. Confirm displayed stats in game.','movement':int(row[11]) if row[11].isdigit() else None,'weapon_rank_text':row[12],'inventory':inv,'equipment':equipment,'skills_known':known,'skills_unresolved':unknown,'random_skills_unresolved':bool(unknown),'position':None,'phase':'reinforcement' if is_wave else 'UNKNOWN' if not section else 'initial_or_scripted' if t.get('timing_label') else 'initial','timing_text':t.get('timing_label'),'source_ids':[sid],'verification':'single_source_partial','limitations':'Not an exact spawned unit. Positions/random skills/forge stats unverified. Do not auto-build a battle from this template.'}
     enemies.append(e);ids.append(eid);all_ids.append(eid)
     if not is_wave and section in ('Starting','Enemy') and not t.get('timing_label'):initial.append(eid)
    if is_wave:
     for ri,row in enumerate(t['rows']):
      turn=re.fullmatch(r'Turn (\d+)',row[0]) if row else None
      if not turn or not all(slug(v) in classes or v=='-' for v in row[1:]):continue
      w={'id':f'{mid}_lunatic_progression_{ti}_{ri}','chapter_id':mid,'difficulty':'Lunatic','enemy_ids':[],'turns':[int(turn[1])],'timing_type':'reported_turn','trigger':'UNKNOWN','spawn_location':'UNKNOWN','coordinates':None,'can_act_on_spawn':'UNKNOWN','units':[{'class_id':slug(v),'source_slot_index':index,'equipment':'UNKNOWN','note':'Source refers to same-class starting data; equipment variant/coordinates not established.'} for index,v in enumerate(row[1:],1) if v!='-'],'source_ids':[sid],'crosscheck_status':'single_source_progression','safe_for_tactical_certainty':False,'verification':'partially_verified','schedule_completeness':'UNKNOWN'}
      waves.append(w);rw.append(w)
    if is_wave and ids:
     timing=t.get('timing_label');match=re.fullmatch(r'Turns? (\d+)(?:[-–](\d+))?',timing or '')
     turns=list(range(int(match[1]),int(match[2] or match[1])+1)) if match else None
     w={'id':f'{mid}_lunatic_wave_{ti}','chapter_id':mid,'difficulty':'Lunatic','enemy_ids':ids,'turns':turns,'timing_text':timing,'timing_type':'reported_turn' if turns else 'UNKNOWN','trigger':'UNKNOWN','spawn_location':'UNKNOWN','coordinates':None,'can_act_on_spawn':'UNKNOWN','source_ids':[sid],'crosscheck_status':'not_independently_confirmed','safe_for_tactical_certainty':False,'verification':'partially_verified','schedule_completeness':'UNKNOWN'}
     waves.append(w);rw.append(w)
   slot=c['difficulty_data']['Lunatic'];slot.update(status='partially_verified',enemies=all_ids or None,initial_enemy_ids=initial or None,reinforcements=rw or None)
   slot['coverage']['enemy_templates']='partially_verified'
   # Non-stat tables such as endgame progression remain factual staging, not invented templates.
 review=json.loads((R/'reviewed_additions.json').read_text())
 for source in review['sources']:source_map[source['id']]=source
 for i,claim in enumerate(review['wave_claims']):
  w={'id':'p2_reviewed_wave_'+str(i),'enemy_ids':[],'coordinates':None,'can_act_on_spawn':'UNKNOWN','safe_for_tactical_certainty':False,'verification':'partially_verified','schedule_completeness':'UNKNOWN',**claim}
  if w.get('spawn_phase')=='beginning_enemy_phase':
   w['can_act_on_spawn']=True;w['can_act_on_spawn_verification']='single_source_mode_rule';w['source_ids']=list(dict.fromkeys(w['source_ids']+['gamerguides_modes']))
  slot=cm[w['chapter_id']]['difficulty_data'][w['difficulty']]
  slot['status']='partially_verified';slot['reinforcements']=(slot['reinforcements'] or [])+[w];waves.append(w)
 for claim in review['absence_claims']:
  slot=cm[claim['chapter_id']]['difficulty_data'][claim['difficulty']];slot['reported_absence']=claim;slot['status']='partially_verified'
 for claim in review['hazards']:
  slot=cm[claim['chapter_id']]['difficulty_data'][claim['difficulty']];slot.setdefault('hazard_claims',[]).append({**claim,'verification':'single_source_partial'});slot['status']='partially_verified'
 for conflict in review['conflicts']:
  for mode in conflict['difficulties']:cm[conflict['map_id']]['difficulty_data'][mode].setdefault('conflicts',[]).append(conflict)
 for mid in mids:
  c=cm[mid]
  for mode in DIFFICULTIES:
   slot=c['difficulty_data'][mode]
   ss=c['source_ids']+slot.get('map_reference',{}).get('source_ids',[])
   if mode=='Lunatic' and mid in best:ss+=[register(best[mid],['Lunatic representative enemy table'])]
   ss+=[sid for w in slot['reinforcements'] or [] for sid in w['source_ids']]
   ss+=slot.get('reported_absence',{}).get('source_ids',[])
   coverage.append({'id':mid+'_'+slug(mode),'map_id':mid,'name':c['name'],'difficulty':mode,'source_ids':list(dict.fromkeys(ss)),'verification':'derived_coverage_audit','map_status':slot['status'],'reinforcement_status':'partially_verified' if slot['reinforcements'] or slot.get('reported_absence') else 'unresolved','enemy_count':len(slot['enemies'] or []),'wave_count':len(slot['reinforcements'] or []),'positions':'UNKNOWN','fully_checked':False,'safe_for_tactical_certainty':False})
 # Replace old partial Ch7 templates with source-preserving richer versions.
 write(ROOT/'data/chapters/chapters.json',{'schema_version':1,'records':chapters})
 write(ROOT/'data/enemies/enemies.json',{'schema_version':1,'records':enemies})
 write(ROOT/'data/chapters/reinforcements.json',{'schema_version':1,'records':waves})
 write(ROOT/'data/chapters/coverage.json',{'schema_version':1,'records':sorted(coverage,key=lambda x:(list(cm).index(x['map_id']),DIFFICULTIES.index(x['difficulty'])))})
 write(ROOT/'research/phase2/normalization_audit.json',{'anomalies':anomalies,'map_attempts':attempts,'policy':'No difficulty copying; no absence inference; no coordinate/forge/random-skill guesses.'})
 for category in ('weapons','items'):
  rs=records(category)
  if category=='weapons':
   for record in rs:
    if record['weapon_type']=='tome':record['dark_magic_classification']=None;record['class_restriction_note']='Original table color encodes dark-only restrictions; plain-text extraction loses it. Verify individual eligibility; do not assume all tome classes can use this weapon.'
  for cross in review['numeric_crosschecks']:
   if cross['category']!=category:continue
   for record in rs:
    if record['id']==cross['id']:
     record['source_ids']=list(dict.fromkeys(record['source_ids']+cross['source_ids']));record['independent_numeric_crosscheck']=cross['expected']
  write(ROOT/'data'/category/(category+'.json'),{'schema_version':1,'records':rs})
 # Game-derived wording cross-check changes only the verified HP boundary.
 sr=records('skills');p=json.loads((R/'skills_game_descriptions.json').read_text())[0];sid=register(p,['Game-localization skill descriptions; Vantage/Wrath inclusive half-HP boundary'])
 for skill in sr:
  if skill['id'] in ('vantage','wrath'):
   skill['effect']=('Defender attacks first when current HP is at most half maximum HP.' if skill['id']=='vantage' else 'Adds 20 critical when current HP is at most half maximum HP.')
   skill['source_ids']=list(dict.fromkeys(skill['source_ids']+[sid]));skill['boundary_crosscheck']='game_localization'
 from combat_events import EVENT_SKILLS
 for skill in sr:
  if skill['id'] in EVENT_SKILLS:
   skill['calculator_supported']=True;skill['calculator_support_note']='Supported with isolated-interaction restrictions; see combat_events.validate and docs/combat-formulas.md. Never omit unsupported combinations.'
  if skill['id']=='pavise':
   skill['effect']='Halves sword/lance/axe/beaststone/blighted-claw/talon damage; Skill% activation; excludes Dual Strikes.';skill['source_ids']=list(dict.fromkeys(skill['source_ids']+['p2_pavise']))
 write(ROOT/'data/skills/skills.json',{'schema_version':1,'records':sr});write(ROOT/'data/sources.json',list(source_map.values()))
 print(json.dumps({'enemy_templates':len(enemies),'partial_waves':len(waves),'Lunatic_maps':len(best),'Hard_metadata_maps':len(guides),'anomalies':len(anomalies)}))
if __name__=='__main__':main()

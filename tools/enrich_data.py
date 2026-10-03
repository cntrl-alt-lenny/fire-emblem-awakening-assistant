#!/usr/bin/env python3
"""Reviewed additions and corrections, with provenance. Run after build_data.py."""
import json,re
from common import ROOT,STATS,lookup
from build_data import ident,clean

def read(path):return json.loads((ROOT/path).read_text())
def save(path,value):(ROOT/path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def dataset(path,records):save('data/'+path,{'schema_version':1,'records':records})
def main():
 sources=read('data/sources.json')
 # Remove irrelevant search-result pollution; only inspected relevant pages are sources.
 sources=[s for s in sources if not s['id'].startswith('enemy_ch7_lunatic_')]
 manual=[
 ('true_hit','Fire Emblem Wiki: True hit','https://fireemblemwiki.org/wiki/True_hit','Awakening 2RN probability and table checks','Fan reference; its numeric table credits Serenes Forest, so not fully independent.'),
 ('fe_wiki_pair','Fire Emblem Wiki: Pair Up','https://fireemblemwiki.org/wiki/Pair_Up','Independent explanatory cross-check: Awakening vs Fates, adjacent support, summed dual support levels','Initial public read succeeded; subsequent reader requests failed. Do not mix Fates rules.'),
 ('pegasus_calculations','Pegasus Knight Awakening calculations','https://www.pegasusknight.com/wiki/fe13/%E8%A8%88%E7%AE%97%E5%BC%8F','Damage, doubling, rank, healing; numerical discrepancy investigation','Several sections explicitly marked uncorrected; early copied New Mystery values. Triangle/rank/terrain conflicts excluded from calculator.'),
 ('nintendo_manual','Nintendo Awakening EU electronic manual','https://www.nintendo.com/eu/media/downloads/games_8/emanuals/nintendo_3ds_2/fire_emblem__awakening_1/ElectronicManual_Nintendo3DS_FireEmblemAwakening_EN.pdf','Classic/Newcomer, game over, seals, EXP threshold, Pair Up commands','EU Newcomer terminology equals Casual. Historical network instructions do not imply present availability.'),
 ('gamerguides_modes','Gamer Guides: Starting a New Game','https://www.gamerguides.com/fire-emblem-awakening/guide/intro-and-gameplay/gameplay','Hard and above reinforcement action timing','Public search excerpt; corroborates timing, not specific schedules.'),
 ('fandom_lunatic_plus','Fandom Fire Emblem Wiki: Lunatic+ Mode','https://fireemblem.fandom.com/wiki/Lunatic%2B_Mode','Lunatic+ skill pools and unlock conditions','Public search excerpt; article marked stub. Validate observed enemy skills.'),
 ('support_basics_review','Serenes Forest: Support Basics (full reviewed section)','https://serenesforest.net/awakening/characters/supports/support-basics/','Map support limits, fractional points, rounding, marriage and Chrom edge cases','Tie/rounding rules from one numerical source.'),
 ]
 for sid,name,url,scope,limits in manual:
  sources.append({'id':sid,'name':name,'url':url,'accessed':'2026-10-02','scope':[scope],'limitations':limits,'method':'public_web_reader_or_search_excerpt'})
 skills=read('data/skills/skills.json')['records'];by={s['id']:s for s in skills}
 additions={'Shadowgift':('Allows dark tomes when the class can use tomes.','passive'),'Paragon':('Doubles EXP.','passive'),"Iote's Shield":('Removes flying effectiveness vulnerability.','passive'),'Limit Breaker':('Raises the seven non-HP stat caps by 10.','passive'),'Dragonskin':('Halves damage; blocks Lethality and Counter.','passive'),'Hit Rate +10':('Adds 10 hit.','passive'),'Rightful God':('Adds 30 percentage points to activation rates.','passive'),'Vantage+':('Defender attacks first.','passive'),'Luna+':('Always applies Luna.','passive'),'Hawkeye':('Always hits.','passive'),'Pavise+':('Always halves sword/lance/axe/beaststone damage; does not halve Dual Strikes.','passive'),'Aegis+':('Always halves bow/tome/dragonstone damage; does not halve Dual Strikes.','passive')}
 for name,(effect,activation) in additions.items():
  k=ident(name)
  if k not in by:
   o={'id':k,'name':name,'effect':effect,'activation':activation,'learned_in':[],'source_ids':['skills_extra'],'verification':'single_source_transcribed','calculator_supported':False};skills.append(o);by[k]=o
 from combat_calculator import SAFE_SKILLS
 for skill in skills:
  skill['calculator_supported']=skill['id'] in SAFE_SKILLS
  if skill['calculator_supported']:skill['calculator_support_note']='Supported duel whitelist: active stat bonuses must already be in effective stats; non-duel effects are not simulated. Dual skills require separately supplied partner/rate context.'
 classes=read('data/classes/classes.json')['records']
 for c in classes:
  for entry in c['skills']:
   if entry['skill_id'] in by:by[entry['skill_id']]['source_ids']=sorted(set(by[entry['skill_id']]['source_ids']))
 # Character recruitment source has an actual typo: Chrom Mov 6 (Lord Mov 5).
 chars=read('data/characters/characters.json')['records']
 for c in chars:
  c['starting_skills']=[s for s in c['starting_skills'] if s not in ('varies',)]
  if c['category']!='child':c['starting_stats_by_difficulty']['Lunatic+']={'raw':None,'equipment_skill_bonuses':None,'status':'not_independently_verified','note':'Lunatic equivalence was not independently established; actual reported stats override templates.'}
  c['special_properties']=[]
  if c['id'] in ['panne','yarne']:c['special_properties']=['beast weakness persists when reclassed']
  if c['id'] in ['nowi','nah','tiki']:c['special_properties']=['dragon weakness persists when reclassed']
  if c['id']=='robin':c['special_properties']=['asset/flaw modifies bases, growths and cap modifiers','gender determines regular class availability','Veteran increases EXP when paired up']
  if c['id']=='morgan':c['starting_inventory']=[]
  if c['id']=='robin':
   c['base_growths_unmodified']=c['base_growths'];c['base_growths']=None
 # Attach named obtainability tables only when caption resolves.
 weapons=read('data/weapons/weapons.json')['records'];items=read('data/items/items.json')['records'];inventory={x['id']:x for x in weapons+items}
 for key in ['obtain_swords','obtain_magic']:
  for page in read('research/'+key+'.json'):
   for t in page['tables']:
    k=ident(t['section'])
    if k in inventory:
     inventory[k].setdefault('obtainability',[]).extend({'method':clean(row[0]),'locations':clean(row[1]),'source_ids':[page['source_id']],'verification':'single_source_transcribed','difficulty':None} for row in t['rows'] if len(row)==2)
     inventory[k]['source_ids']=sorted(set(inventory[k]['source_ids']+[page['source_id']]))
 # Normalize support thresholds into explicit edges. Keep gender-specific Robin/Morgan variants.
 supports=[];pairs={};conflicts=[]
 for p in read('research/support_growth.json')[:1]:
  for t in p['tables']:
   if t['section']=='Support Growth':continue
   people=t['section'].split('/')
   for row in t['rows']:
    if len(row)!=5 or row[0]=='Character(s)':continue
    for left in people:
     for right in row[0].split(', '):
      if right.startswith('Any '):continue
      a=ident(left);b=ident(right)
      if a==b:continue
      pair=tuple(sorted([a,b]));thresholds={rank:int(v) if v.isdigit() else None for rank,v in zip(['C','B','A','S'],row[1:])}
      if pair in pairs and pairs[pair]['thresholds']!=thresholds:conflicts.append({'pair':pair,'values':[pairs[pair]['thresholds'],thresholds]})
      else:pairs[pair]={'id':pair[0]+'__'+pair[1],'name':left+' / '+right,'units':list(pair),'thresholds':thresholds,'threshold_basis':'total_accumulated_points','source_ids':['support_growth'],'verification':'single_source_transcribed','limitations':'Fixed-parent/sibling edges are conditional on actual parentage; not included by this threshold table.'}
 # Explicitly disallow impossible Morgan(M)/Morgan(F) pair despite a source-table error.
 invalid=tuple(sorted(['morgan_m','morgan_f']))
 if invalid in pairs:del pairs[invalid]
 supports=list(pairs.values());dataset('supports/compatibility.json',supports)
 save('research/support_conflicts.json',{'conflicts':conflicts,'excluded':['morgan_m__morgan_f'],'reason':'Supports page explicitly excludes male/female Morgan marriage; growth table accidentally includes it.'})
 # Avatar modifier facts; blank source cells denote zero modifiers.
 growth_rows=read('research/character_growths.json')[0]['tables'];cap_rows=read('research/inheritance.json')[1]['tables']
 avatar={}
 statkeys={'HP':'hp','Strength':'str','Magic':'mag','Skill':'skl','Speed':'spd','Luck':'lck','Defence':'def','Resistance':'res'}
 for t in growth_rows:
  if t['section']!='Avatar':continue
  for r in t['rows']:
   if r[0] not in statkeys or len(r)!=9:continue
   mod={'asset':{},'flaw':{}}
   for s,x in zip(STATS,r[1:]):
    if not x:a=b=0
    elif '+/-' in x:a=int(x[3:]);b=-a
    else:a,b=map(int,x.split('/'))
    mod['asset'][s]=a;mod['flaw'][s]=b
   avatar[statkeys[r[0]]]={'growth_modifiers':mod}
 for t in cap_rows:
  if t['section']!='Avatar':continue
  for r in t['rows']:
   if r[0] not in statkeys or len(r)!=8:continue
   mod={'asset':{},'flaw':{}}
   for s,x in zip(STATS[1:],r[1:]):
    a,b=map(int,x.split('/')) if x else (0,0);mod['asset'][s]=a;mod['flaw'][s]=b
   avatar[statkeys[r[0]]]['cap_modifiers']=mod
 dataset('characters/avatar.json',[{'id':'avatar_configuration','name':'Avatar configuration','unmodified_bases':{'hp':19,'str':6,'mag':5,'skl':5,'spd':6,'lck':4,'def':6,'res':4},'unmodified_growths':{'hp':40,'str':40,'mag':35,'skl':35,'spd':35,'lck':55,'def':30,'res':20},'base_asset_flaw_changes':{'hp':[5,-3],'lck':[4,-2],'other':[2,-1]},'modifiers':avatar,'source_ids':['characters','character_growths','inheritance_1'],'verification':'single_source_transcribed'}])
 # Normalize one inspected enemy dataset, without assigning its values to Hard/Normal.
 enemies=[]
 p=read('research/enemy_ch7_lunatic.json')[0]
 for t in p['tables']:
  for r in t['rows']:
   if len(r)!=15 or not r[2].isdigit():continue
   enemies.append({'id':f'chapter_7_lunatic_{len(enemies)+1}','name':r[0],'chapter_id':'chapter_7','difficulty':'Lunatic','class_id':ident(r[1]),'level':int(r[2]),'stats':dict(zip(STATS,map(int,r[3:11]))),'movement':int(r[11]),'weapon_rank':r[12],'inventory':[ident(x) for x in r[13].split(', ')],'skills_known':[ident(x) for x in r[14].split(', ') if x!='Random'],'random_skills_unresolved':'Random' in r[14],'phase':'reinforcement' if t['section']=='Reinforcements' else 'initial','source_ids':['enemy_ch7_lunatic'],'verification':'single_source_transcribed','limitations':'Indexed table is a representative numerical reference. Actual spawned stats, skills and forged weapon stats must be inspected in-game.'})
 dataset('enemies/enemies.json',enemies)
 chapters=read('data/chapters/chapters.json')['records']
 for ch in chapters:
  if ch['id']=='chapter_7':
   ch['difficulty_data']['Lunatic']={'status':'partial','enemies':[e['id'] for e in enemies if e['phase']=='initial'],'reinforcements':[{'turn':5,'phase':'enemy','location':'western edge; exact squares unknown','enemy_ids':[e['id'] for e in enemies if e['phase']=='reinforcement'],'conditions':None,'source_ids':['enemy_ch7_lunatic','reinforcements_early_1'],'verification':'timing_cross_referenced_stats_conflict','safe_for_tactical_certainty':False,'uncertainty':'EmblemWiki lists level 9; Fandom groups Hard/Lunatic as level 7. Do not use Hard statistics for Lunatic; exact coordinates and trigger/block rules unverified.'}]}
   ch['source_ids']+=['enemy_ch7_lunatic','reinforcements_early_1']
 # Deliberately retain other search schedules as candidates, never safe schedules.
 candidates=[]
 for path in sorted((ROOT/'research').glob('reinforcements_*.json')):
  for p in read(path.relative_to(ROOT)):
   candidates.append({'id':p['source_id'],'name':p['name'],'candidate_lines':p['reinforcement_candidates'],'source_ids':[p['source_id']],'verification':'unreviewed_search_excerpt','safe_for_tactical_certainty':False})
 dataset('chapters/reinforcement_candidates.json',candidates)
 for path,records in [('skills/skills.json',skills),('characters/characters.json',chars),('classes/classes.json',classes),('weapons/weapons.json',weapons),('items/items.json',items),('chapters/chapters.json',chapters)]:dataset(path,records)
 # Shop rows and merchant continuation rows are explicit source table groups.
 shops=[];merchant=[];rare=[];rewards=[]
 for page in read('research/economy.json'):
  current=None
  for t in page['tables']:
   for row in t['rows']:
    if page['source_id']=='economy_2':
     if len(row)==2 and row[1].isdigit():rewards.append({'id':ident(row[0]),'name':clean(row[0]),'renown':int(row[1]),'reward_id':'tikis_tear' if ident(row[0])=='tikis_tears' else ident(row[0]),'source_ids':['economy_2'],'verification':'single_source_transcribed'})
    elif len(row)==7 and row[1].startswith(('Ch.','Par.','Pro.')):
     label=row[1];chapter='prologue' if label=='Pro.' else ('paralogue_' if label.startswith('Par.') else 'chapter_')+re.search(r'\d+',label)[0]
     current={'id':chapter,'name':clean(row[0]),'chapter_id':chapter,'item_ids':[ident(x) for x in row[2:] if x!='–'],'source_ids':[page['source_id']],'verification':'single_source_transcribed','limitations':'World-map location catalog; merchant spawn probability/stock selection not inferred.' if page['source_id']=='economy_1' else 'Buy/sell pricing, discounts and difficulty changes require separate verification.'}
     (shops if page['source_id']=='economy' else merchant).append(current)
    elif page['source_id']=='economy_1' and len(row)==5 and current is not None:current['item_ids'] +=[ident(x) for x in row if x!='–']
    elif page['source_id']=='economy_1' and t['section']=='Rare Items':
     if len(row)==7 and row[0]=='Rare item':rare +=[ident(x) for x in row[2:]]
     elif len(row)==5:rare +=[ident(x) for x in row]
 dataset('items/shops.json',shops);dataset('items/merchants.json',merchant);dataset('items/renown.json',rewards)
 dataset('items/merchant_rare_pool.json',[{'id':'rare_item_pool','name':'Travelling merchant rare pool','item_ids':rare,'source_ids':['economy_1'],'verification':'single_source_transcribed','limitations':'Selection probability unknown.'}])
 save('data/sources.json',sources)
 print({'supports':len(supports),'support_conflicts':len(conflicts),'enemies':len(enemies),'skills':len(skills),'obtainability_weapons':sum('obtainability' in w for w in weapons)})
if __name__=='__main__':main()

"""Author reviewed factual extracts, NOT a scraper. Run to regenerate reviewed.json."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parents[2]
sources=json.loads((P/'data/sources.json').read_text())
chapters=json.loads((P/'data/chapters/chapters.json').read_text())['records']
extra=json.loads((P/'research/hard_verification/additional_sources.json').read_text())
def source(sid,name,url,scope,limitations,method='public_web_reader',family=None):
 extra.append(dict(id=sid,name=name,url=url,scope=[scope],limitations=limitations,method=method,accessed='2026-10-02',evidence_family=family or sid))
source('hr_gg_spawn','Gamer Guides — Starting a New Game','https://www.gamerguides.com/fire-emblem-awakening/guide/intro-and-gameplay/gameplay/starting-a-new-game','Hard and above: reinforcements act as enemy phase begins','General ordinary reinforcement rule; does not certify every scripted exception.',family='gamerguides_vincent_lau')
source('hr_hard_spawn_observation','GBAtemp — Awakening Hard reinforcement discussion','https://gbatemp.net/threads/fire-emblem-awakening-reinforcements.435653/','Explicit Hard player report: enemies spawn at beginning of enemy phase, can attack immediately','Public search-index excerpt only; direct page returned 403. Independent community report, not a controlled game-script audit.','public_search_excerpt','gbatemp_original_player')
source('hr_fandom16','Fire Emblem Fandom — Nagas Voice, Hard reinforcement subsection','https://fireemblem.fandom.com/wiki/Naga%27s_Voice','Explicit Hard turn 4/5/6 classes, counts and equipment; contrasted with separately headed Lunatic subsection','Public indexed subsection, not full page retrieval. Independent corroboration of each precise count was not available.','public_search_excerpt','fandom_editors')
source('hr_fandom17','Fire Emblem Fandom — Inexorable Death, Hard reinforcement subsection','https://fireemblem.fandom.com/wiki/Inexorable_Death','Reported Hard turn 8 eastern / turn 9 west-central / turn 10 central staircase waves','Public indexed Hard subsection revisited 2026-10-03: first/second inventories each four units; central entry reports one War Monk with Silver Axe and one Hero with Silver Sword. Inherited six-unit central inventory has no recoverable external basis; neither alternative is adopted as observed gameplay. Classic/Casual and region/version unspecified. Subsequent mode boundary lost in original excerpt; later listed turns NOT imported as Hard. First side conflicts with explicitly Hard Japanese observation.','public_search_excerpt','fandom_editors')
next(s for s in extra if s['id']=='hr_fandom17')['accessed']='2026-10-03'
source('hr_jp_recruit','Pegasus Knight — Awakening recruitment','https://www.pegasusknight.com/wiki/fe13/%E3%83%A6%E3%83%8B%E3%83%83%E3%83%88/%E4%BB%B2%E9%96%93%E3%81%AB%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95','Recruitment conditions; killing Holland makes Severa hostile','General recruitment system, not Hard enemy stats. Possible underlying overlap with other references; not counted as independent corroboration.',family='pegasus_recruitment')
guides={}
for s in sources:
 if s['id'].startswith('p2_guide') and 'gamerguides' in s['url']:
  leaf=s['url'].rstrip('/').split('/')[-1]
  m=re.search(r'^(chapter|sidequest)-(\d+)-',leaf)
  mid=('chapter_' if m[1]=='chapter' else 'paralogue_')+m[2] if m else next((x for x in ('prologue','premonition','endgame') if leaf.startswith(x+'-')),None)
  if mid:guides.setdefault(mid,s['id'])
for mid,leaf in [('chapter_9','chapter-9-emmeryn'),('chapter_10','chapter-10-renewal'),('paralogue_5','sidequest-5-scion-of-legend')]:
 sid='hr_gg_'+mid;section='story-walkthrough/beginning-to-chapter/' if mid.startswith('chapter') else 'sidequests-paralogues/sidequests-1-to-13/'
 source(sid,'Gamer Guides — '+leaf,'https://www.gamerguides.com/fire-emblem-awakening/guide/'+section+leaf,'Hard map tactical reference','Guide defaults to Hard according to reading-this-guide. Exclude explicitly labelled Lunatic paragraphs. Contains occasional objective errors; do not certify completeness.',family='gamerguides_vincent_lau');guides[mid]=sid

def claim(value,sids,confidence='SUPPORTED',notes=None):
 return dict(value=value,confidence=confidence,source_ids=sids,notes=notes)
def C(mid,value,confidence='SUPPORTED',notes=None,sids=None):return claim(value,sids or [guides[mid],'p2_guide_scope'],confidence,notes)
M={}
ids=['prologue']+['chapter_'+str(n) for n in range(1,26)]+['endgame']+['paralogue_'+str(n) for n in range(1,18)]
limits=[4,6,7,8,6,9,10,11,10,12,13,13,12,12,13,12,14,14,13,15,15,14,13,15,15,15,16]+[8,10,10,12,13,13,13,13,13,13,13,13,13,13,13,13,13]
for mid,limit in zip(ids,limits):
 M[mid]=dict(id=mid,guide_id=guides[mid],deployment=C(mid,limit,notes='Pre-battle limit including Chrom; automatic NPC/allied arrivals are additional. Early chapters without preparation use initial army size.'),hazards=[],interactables=[],activation=[],waves=[],conflicts=[],reinforcement_absence=None)
def h(mid,text,confidence='SUPPORTED',sids=None,notes=None):M[mid]['hazards'].append(C(mid,text,confidence,notes,sids))
def i(mid,text,confidence='SUPPORTED'):M[mid]['interactables'].append(C(mid,text,confidence))
def a(mid,text,confidence='SUPPORTED',sids=None):M[mid]['activation'].append(C(mid,text,confidence,sids=sids))
def w(mid,key,location=None,turns=None,trigger=None,units=None,sids=None,confidence='PARTIAL',kind=None,notes=None,repeat=None):
 ss=sids or [guides[mid],'p2_guide_scope']; c='SUPPORTED'
 row=dict(id='hard_'+mid+'_'+key,chapter_id=mid,difficulty='Hard',mode='Classic',confidence=confidence,source_ids=ss,
 timing=claim(dict(kind=kind or ('fixed' if turns else 'event' if trigger else 'unknown'),turns=turns,event=trigger,repeat=repeat),ss,c if turns or trigger or repeat else 'UNKNOWN',notes),
 location=claim(location,ss,c if location else 'UNKNOWN'),units=claim(units,ss,c if units else 'UNKNOWN'),
 spawn_phase=claim('beginning_enemy_phase',ss+['hr_gg_spawn'],'SUPPORTED','Ordinary Hard rule applied; map-specific scripted exceptions have not all been excluded.'),
 immediate_action=claim(dict(can_move=True,can_attack=True,can_kill_on_spawn=True),['hr_gg_spawn','hr_hard_spawn_observation'],'VERIFIED','General Hard ordinary reinforcement rule, not an independent observation of this wave.'),
 coordinates=claim(None,[],'UNKNOWN'),skills=claim(None,[],'UNKNOWN'),suppression=claim(None,[],'UNKNOWN'),schedule_completeness='UNKNOWN')
 M[mid]['waves'].append(row);return row

def u(count,class_id,*equipment,level=None,location=None):return dict(count=count,class_id=class_id,equipment=list(equipment) or None,level=level,location=location)
# Only short normalized factual claims. Explicit other-mode paragraphs excluded.
h('prologue','Bridge chokepoint; Garrick carries a Hand Axe (range 1–2).')
h('chapter_1','Sully and Virion arrive on turn 2. Woods/forts affect movement and combat. The guide Hammer paragraph is explicitly Lunatic and is excluded.')
h('chapter_2','Vaike starts without his axe; Miriel arrives from the south on turn 2 carrying it. Northern bridge constrains movement.')
h('chapter_3','A Hammer-bearing Fighter threatens armoured units; enemy bows threaten flying units. Inspect exact enemy inventories before moving Frederick or Sumia.')
i('chapter_3','Doors on the left/right routes; obtain Door Keys from enemies. Kellam is an NPC: recruit with Chrom.')
h('chapter_4','Small deployment; boss carries Parallel Falchion. Lon’qu joins at map completion, not at the start of Chapter 5.')
h('chapter_5','Ricken and Maribelle start isolated in the north. Wyverns cross cliffs and can threaten units beyond ground chokepoints.')
w('chapter_5','disputed_schedule','Forts; northwestern flying approach',sids=['reinforcements_early_0','hr_jp_5',guides['chapter_5']],confidence='CONFLICTED',notes='Western indexed Hard table reports turns 3/4/5; explicitly Hard JP 2012-04-19 comment reports a different turn-3 mixture and tentative turn-5 group. Full schedule cannot be selected safely.')
M['chapter_5']['conflicts'].append(claim({'western_report':'T3 foot units; T4 two Wyverns northwest; T5 mixed group','japanese_hard_observation':'T3 two Wyverns plus Barbarian and Myrmidon, central-left; tentative T5 foot units','resolution':None},['reinforcements_early_0','hr_jp_5'],'CONFLICTED','Possible region, phase convention or guide error not established. Within western page table/prose also differ on a Dark Mage versus second Barbarian.'))
a('chapter_5','Hard-labelled JP report: two initial Wyverns advance on turn 1; remaining Wyverns/boss respond to attack range. Exact activation tiles unknown.',sids=['hr_jp_5'])
h('chapter_6','Emmeryn must survive. Gaius is initially hostile: talk with Chrom rather than killing him. Panne arrives on turn 2.')
a('chapter_6','Validar eventually advances; exact activation turn/condition unresolved. Three approaches threaten Emmeryn.','PARTIAL')
h('chapter_7','Flying enemies cross mountain/cliff barriers. Cordelia arrives from the west on turn 3.')
w('chapter_7','t5','Western map edge',[5],units=[u(3,'wyvern_rider','steel_axe',level=7)],sids=['reinforcements_early_1',guides['chapter_7']],confidence='SUPPORTED',notes='Exact turn/count/equipment single indexed Hard subsection; western arrival corroborated by guide. Not a certified complete schedule.')
h('chapter_8','Gregor and Nowi start isolated south; desert movement can prevent timely rescue.')
i('chapter_8','Three villages: west Master Seal, southeast Second Seal, northeast Rescue. Full tile coordinates unknown.')
h('chapter_8','Guide tentatively suggests villages are not attacked on Hard; do not rely on that tentative claim.','PARTIAL')
h('chapter_9','Recruit NPC Libra and enemy Tharja using Chrom. Desert movement and arriving enemies behind the starting area threaten slow units.')
w('chapter_9','rear_arrival','Behind player starting area')
h('chapter_10','Thieves carrying valuable loot escape northwest; reaching them can expose a unit to fort-spawned Wyverns.')
w('chapter_10','t6','Western forts',[6],units=[u(1,'wyvern_rider','steel_axe',level=13),u(1,'wyvern_rider','hand_axe',level=13)],sids=['reinforcements_mid_0',guides['chapter_10']],confidence='SUPPORTED')
i('chapter_11','Chests contain Bullion and Goddess Icon; thieves threaten chest loot.')
a('chapter_11','Gangrel may advance on turn 4 or when approached; trigger boundary unknown.','PARTIAL')
row=w('chapter_11','t3_forts','Forts, including southern forts',kind='conditional_report')
row['timing']=claim({'kind':'conditional_report','turns':None,'reported_start_turn':3,'event':'Fort arrivals: turn-3 warning; subsequent timing unresolved','repeat':None},row['source_ids'],'PARTIAL','Source warns about positioning on Turn 3 and occupying southern forts by Turn 3; it does not specify recurrence or a final turn. Reported start is an interpretation of that warning. Retain as a possible family from that turn, not a prediction of arrivals on every later turn.')
w('chapter_11','t4_nw','Northwest (top-left) map area',[4],units=[u(3,None)],notes='Three arrivals reported; exact classes, equipment and tiles unknown.')
M['chapter_11']['waves'][0]['suppression']=C('chapter_11','An occupied fort can prevent its spawn; applicability to every fort/wave not certified.')
h('chapter_12','Cherche joins automatically. Numerous mounted and armoured enemies; inspect effective weapons and counter ranges.')
h('chapter_13','Longbow enemies on raised terrain can attack at range 3; flying units remain vulnerable. Lucina joins after completion.')
w('chapter_13','forts','Forts')
h('chapter_14','Four main chokepoints connect ships; incoming Pegasus enemies bypass ground chokepoints.')
i('chapter_14','Ship chests; exact contents/coordinates not certified in this Hard pass.')
w('chapter_14','fliers','Approaches to the ships',units=[u(None,'pegasus_knight')])
h('chapter_15','Say’ri is an unarmed NPC under immediate pressure; talk with Chrom and provide a weapon/healing. Beach movement slows non-fliers.')
a('chapter_15','Enemies on the beach move toward player forces; the old post-reinforcement group activation claim is quarantined.')
M['chapter_15']['reinforcement_absence']=claim(True,['hr_jp_15'],'SUPPORTED','Explicit Hard-labelled original comment, 2012-04-30, reports no reinforcements. Japanese-release observation; not game-script proof. False old waves belong to Chapter 16 Lunatic, not contradictory Hard evidence.')
h('chapter_16','Hard-labelled JP 2012-04-26 observation reports a Warrior with Counter; inspect actual skills. Counter is not guaranteed on every Warrior.',sids=['hr_jp_16'])
h('chapter_16','Some arriving Warriors carry bows; Falcon arrivals threaten units on both sides. Do not concentrate safety checks only at the southern edge.')
w('chapter_16','t4','Southern/bottom map edge',[4],units=[u(2,'fighter','steel_axe',level=20),u(1,'fighter','short_axe',level=20),u(1,'fighter','short_axe','concoction',level=20),u(1,'hero','silver_sword',level=3),u(1,'hero','silver_axe',level=3),u(2,'warrior','silver_axe','silver_bow',level=3)],sids=['hr_fandom16',guides['chapter_16']],confidence='SUPPORTED',notes='Eight Hard units; ten-unit Lunatic mixture expressly excluded.')
w('chapter_16','t5','East/west edges (Silver Lance); southeast/southwest edges (Spear)',[5],units=[u(2,'falcon_knight','silver_lance',level=3),u(2,'falcon_knight','spear',level=3)],sids=['hr_fandom16'],confidence='SUPPORTED')
w('chapter_16','t6','Southern/bottom map edge',[6],units=[u(4,'bow_knight','silver_sword','silver_bow',level=3)],sids=['hr_fandom16'],confidence='SUPPORTED')
h('chapter_17','Army begins in three southern groups. Multiple staircases spawn enemies; first wave side and exact warning/turn relationship are conflicted.')
i('chapter_17','Northwest chests include Boots and Seraph Robe; thief threatens loot.')
a('chapter_17','Explicit Hard JP 2014-09-06 report: entering attack range of enemies in upper six rows activates that group. Exact geometric boundary not certified.',sids=['hr_jp_17'])
for key,location,reported,units in [('first','Eastern stairs OR western stairs',[8],[u(2,'hero','silver_sword'),u(1,'war_monk','silver_axe'),u(1,'sniper','silver_bow')]),('second','West-central stairs',[9],[u(2,'hero','silver_sword'),u(1,'sniper','silver_bow'),u(1,'war_monk','silver_axe')]),('central','Central stairs',[10],[u(3,'hero','silver_sword'),u(2,'war_monk','silver_axe'),u(1,'sniper','silver_bow')])]:
 row=w('chapter_17',key,location,units=units,sids=['hr_fandom17',guides['chapter_17'],'hr_jp_17'],confidence='CONFLICTED' if key=='first' else 'PARTIAL',notes='Indexed Hard table reports turn '+str(reported[0])+'. Warning/conditional timing not independently established; not treated as an unconditional fixed turn.')
 row['timing']=claim({'kind':'conditional_report','turns':None,'reported_turns':reported,'event':'After Say’ri warning; exact interval/trigger unresolved','repeat':None},row['source_ids'],'PARTIAL')
 if key=='first':row['location']['confidence']='CONFLICTED'
M['chapter_17']['conflicts'].append(claim({'guide_and_index':'Eastern stairs first','hard_jp_2012_04_27':'Left stairs first, approximately three turns after warning','resolution':None},[guides['chapter_17'],'hr_fandom17','hr_jp_17'],'CONFLICTED','Do not convert warning to a certified fixed turn or choose only one side to guard.'))
h('chapter_18','Lava progressively consumes floor tiles; affected movement/damage and exact phase must be checked in game.')
i('chapter_18','Guide chest disappearance deadlines: Bullion M turn 7; Energy Drop and Rescue turn 10; Second Seal turn 11. Exact phase unknown: retrieve earlier rather than treating deadline as a safe final action.')
h('chapter_19','Walhart can move when approached. Conquest negates armour/beast effective damage; equipped Sol is a sword, not proof of a Sol proc skill.')
w('chapter_19','forts','Multiple forts',notes='Guide turn-8 note explicitly refers to Lunatic and is NOT used for Hard.')
M['chapter_19']['waves'][0]['suppression']=C('chapter_19','Occupied forts prevent their arrivals; complete applicability unknown.')
i('chapter_20','Chests require keys/Locktouch; exact Hard chest positions unresolved.')
legacy=json.loads((P/'data/chapters/reinforcements.json').read_text())['records']
l20=next(x for x in legacy if x['chapter_id']=='chapter_20' and x['difficulty']=='Hard')
row=w('chapter_20','southern_warning','Southwest, south and southeast edges',trigger='One turn after soldier warning',units=l20['units'],sids=['reinforcements_20_22_0',guides['chapter_20']],notes='Indexed Hard table reports turn 6; guide establishes warning-relative timing. Whether the warning itself is conditional is unknown.',kind='relative')
row['timing']['value'].update(reported_turns=[6],offset_turns=1)
h('chapter_20','Objective wording conflicts: chapter catalog says defeat Walhart; guide says defeat every boss. Verify the displayed objective before attempting a boss rush.','CONFLICTED',sids=['chapter_catalog',guides['chapter_20']])
M['chapter_20']['conflicts'].append(claim({'catalog':'Defeat Walhart','hard_guide':'Defeat every boss','resolution':None},['chapter_catalog',guides['chapter_20']],'CONFLICTED'))
h('chapter_21','Long-range magic from outer halls can threaten units across walls. Algol has a magical Bolt Axe.')
w('chapter_21','outer_stairs','Stairs in left/right outer halls')
w('chapter_21','main_area','Main interior area')
M['chapter_22']['reinforcement_absence']=C('chapter_22',True,notes='Guide explicitly says no reinforcements; not inferred from an empty table. Single strong specific source; no game-script certification.')
h('chapter_22','Thirteen initial enemies including Aversa; Deadlords carry powerful equipment. Exact Hard stats/skills must be observed.')
h('chapter_23','Initially Chrom/Robin isolated above a barrier. First Validar defeat removes barrier and adds Basilio/Flavia; second Validar moves to the eastern area.')
w('chapter_23','stairs','Southern/bottom stairs',trigger='Script warning during the Validar sequence; exact stage/turn unknown',notes='Do not assume warning is available early enough to reposition safely.')
M['chapter_23']['waves'][0]['suppression']=C('chapter_23','Occupied stairs can prevent spawns; not all staircase cases independently established.')
w('chapter_24','fort_sequence','Forts',repeat={'interval_turns':1,'first_turn':None,'last_turn':None,'termination':None},kind='repeating',notes='Consecutive-turn arrivals described; beginning/end and complete wave counts unknown.')
h('chapter_24','Woods slow mounted units; flying enemies bypass that ground restriction.')
w('chapter_25','multiple_angles','Several map approaches',notes='Hard guide describes early attacks from multiple directions; exact reinforcement locations/turns unresolved.')
h('chapter_25','Do not treat all enemy arrivals as fort-bound or assume adjacent peaks prevent flying attacks.')
w('endgame','continuous','Map edges/arrival locations unresolved',repeat={'interval_turns':1,'first_turn':None,'last_turn':None,'termination':'Defeat Grima'},kind='repeating',notes='Guide says every turn until completion; first spawning turn and unit count unknown.')
h('endgame','Grima’s Dragonskin/Expiration interaction is outside supported full combat outcomes; do not present a precise survival probability.')
h('paralogue_1','Donnel must gain a level and survive completion to join. Thieves threaten chests; enemy bows threaten fliers.')
i('paralogue_1','Two chests and enemy Chest Keys; exact tiles not certified.')
h('paralogue_2','Anna here is an NPC, not the later recruitable unit. A Barbarian targets the village; no certified visit deadline.')
a('paralogue_2','Southern group activation is related to approaching its range / visiting village, but logical trigger condition is unresolved.','PARTIAL')
i('paralogue_2','Village is threatened; guide turn-5/6 estimate is strategy interpretation, not a fixed destruction script.')
h('paralogue_3','Villagers flee west/southwest and are threatened by Pegasus Knights. Whether all villagers dying is mission failure rather than lost rewards remains unresolved.','PARTIAL')
i('paralogue_4','Interior doors/chests; thieves flee with loot. Walls constrain fliers too.')
h('paralogue_5','Enemies target NPC Sages; an NPC may die on the first enemy phase. Gecko is described with Vantage and Pass: inspect skill panel before attacking.')
i('paralogue_5','NPC interactions yield items; Owain’s southeast Sage interaction can yield Missiletainn. Exact prerequisite details not fully established.','PARTIAL')
h('paralogue_6','Pass-bearing Assassins can bypass an ordinary body block. Flying threats approach from north/south; the guide does not establish whether all are newly spawned.')
h('paralogue_6','Inigo’s optional five-kill reward is not his recruitment condition.')
h('paralogue_7','Longbows can threaten villagers beyond ordinary bow range; boss eventually advances, exact trigger unknown.')
w('paralogue_8','t5','Stairs',[5])
i('paralogue_8','Doors/chests: guide reports only one Door Key and no Chest Keys; bring appropriate key/Locktouch rather than relying on chest drops.')
h('paralogue_9','Cynthia is initially an enemy. Ruger can turn green units hostile; killing indiscriminately can lose recruitment.')
a('paralogue_9','Approaching north of northern walls affects Ruger’s retreat/conversion behaviour; exact activation geometry unresolved.','PARTIAL')
h('paralogue_10','Severa must reach and talk to Holland; Chrom/Cordelia talking to her alone does not recruit her. Killing Holland can turn her hostile.',sids=['recruitment','hr_jp_recruit'])
h('paralogue_10','Vantage-bearing Assassins and Levin Sword Tricksters threaten escorts. Confirm actual skills/equipment.')
i('paralogue_10','Doors permit shortcuts to Holland; central staircases and chests.')
w('paralogue_10','severa_join','Four central staircases',trigger='Severa talks to Holland and joins; next enemy phase',notes='Event-triggered, NOT a fixed turn. Other staircase arrivals are not ruled out.')
M['paralogue_10']['waves'][0]['suppression']=C('paralogue_10','Occupying a staircase prevents its spawn; single guide claim, precise tiles unknown.')
w('paralogue_11','t5','Forts on northern islands',[5],units=[u(None,'wyvern_lord')])
h('paralogue_11','Five scattered villagers need protection; Wyvern reinforcements bypass ground screening.')
w('paralogue_12','stairs','Stairs',notes='Guide points to a reinforcement image; image-derived exact turns/tiles were not reliably established.')
h('paralogue_12','Morgan starts as NPC; thieves threaten chests immediately. Do not invent a thief capture deadline.')
w('paralogue_13','faction_arrivals',trigger='Depends on selected faction / fighting both sides; exact trigger unknown',notes='Guide reports additional enemies; faction-specific arrival times, locations, classes unknown.')
h('paralogue_13','Faction choice changes hostile units. Yarne can be NPC or enemy: recruit using Chrom or Panne in either case.')
w('paralogue_14','village_visits',trigger='Each village visit',kind='event',repeat={'interval_turns':None,'first_turn':None,'last_turn':None,'termination':'No further village visits'},notes='Aggregate repeated event family; individual village-specific waves cannot yet be enumerated. Not one certified finite wave.')
i('paralogue_14','Recruit Laurent by visiting southwest village with Chrom/Miriel. Hidden village sequence northeast → northwest → southeast; visits can spawn enemies.')
h('paralogue_15','Noire arrives automatically turn 2, isolated in northern enclosure among flying threats. Guide approximate escape window is not a certified reinforcement turn.')
h('paralogue_16','Walls break and reform as turns/area events occur. Opening near Nah can open other routes; exact triggers unknown. Long-range tomes and Counter-bearing Warriors are hazards.')
i('paralogue_16','Opened doors remain open according to guide; changing walls do not establish permanent safe chokepoints.')
w('paralogue_17','flying_waves','West, south and east approaches',notes='Multiple flying waves; count and exact timing unknown. Record is an event family, not a complete list of individual waves.')
h('paralogue_17','Flying reinforcements prioritize Tiki and can fly past the player’s army.',confidence='VERIFIED',sids=[guides['paralogue_17'],'hr_jp_p17'],notes='Hard guide and independent Hard-labelled Japanese player report of losing Tiki agree on target priority. Does not prove exact reach/turns.')
a('paralogue_17','Boss advances after reinforcement enemies are eliminated; exact final-wave enumeration unresolved.','PARTIAL')
# Objective contradictions are retained rather than accepting guide boss-rush shorthand.
for mid in ['prologue','chapter_1','chapter_2','chapter_6','chapter_9']:
 M[mid]['conflicts'].append(claim({'catalog':next(c['objective'] for c in chapters if c['id']==mid),'guide':'Boss/defend shorthand differs from catalog','resolution':None},['chapter_catalog',guides[mid]],'CONFLICTED','Require in-game displayed objective; do not advise that killing boss necessarily ends a rout map.'))
# Conservative phase and action application: the general rule does not prove every script.
for m in M.values():
 for wave in m['waves']:
  if m['id'] not in ('chapter_7','chapter_10','chapter_16','chapter_20','paralogue_10'):
   wave['spawn_phase']=claim(None,[],'UNKNOWN','Ordinary Hard arrivals act at enemy-phase beginning, but exact phase of this map-specific event was not directly established.')
  wave['immediate_action']['confidence']='SUPPORTED'
  wave['immediate_action']['notes']='Conditional application of VERIFIED ordinary Hard rule: if this is an ordinary beginning-enemy-phase arrival it can move/attack and kill immediately. This wave was not independently observed; scripted phase/exception uncertainty remains.'
  if wave['units']['value']:
   wave['units']['notes']='Support applies to the supplied attributes only. Null class/count/equipment/level/location remains UNKNOWN, never absent. Skill rolls and exact enemy forge stats are not established.'
# Chapter 17 field-specific inventory dispositions follow generic note rewriting.
# History alone cannot support the central literal; keep both alternatives visible.
for wave in M['chapter_17']['waves']:
 if wave['id'].endswith('_central'):
  wave['units']=claim(None,['hr_fandom17'],'CONFLICTED',
   'Inherited six-unit alternative: 3 Heroes with Silver Sword, 2 War Monks with Silver Axe, 1 Sniper with Silver Bow; earliest recoverable literal is cf17834fd6a8867d06c25faa772a5d8700f32167 author_review.py, with no recoverable external basis. Accessible indexed two-unit alternative: 1 War Monk with Silver Axe and 1 Hero with Silver Sword (Hard reinforcement turn-10 row, accessed 2026-10-03). Neither alternative is selected as actual gameplay; null inventory is UNKNOWN, not zero. hr_fandom17 supports only the indexed alternative. Gamer Guides supplies no inventory; the Hard-labelled Pegasus comment does not enumerate central classes/counts/equipment. Classic/Casual, region/version and this event phase remain unestablished. No complete schedule or safety guarantee.')
 else:
  wave['units']['source_ids']=['hr_fandom17']
  wave['units']['notes']='Reported class/count/equipment only: single-source indexed Hard reinforcement '+('turn-8' if wave['id'].endswith('_first') else 'turn-9')+' row (hr_fandom17, accessed 2026-10-03); not independently observed gameplay. Gamer Guides lists no inventory. The Hard-labelled Pegasus 2012-04-27 comment reports four arrivals including a Sniper, but supplies neither all class counts nor equipment and does not identify a table wave unambiguously. Classic/Casual, region/version and event phase are unspecified. Null level/location and unlisted skills/forges remain UNKNOWN. Timing/location conflict and incomplete schedule remain unchanged.'
for mid,area in [('chapter_5','Main force south; Ricken/Maribelle isolated north'),('chapter_8','Main force north; Gregor/Nowi isolated south'),('chapter_16','Southern/bottom approach to the Mila Tree'),('chapter_17','Three southern player groups'),('chapter_23','Chrom/Robin separated above barrier from rest of army'),('paralogue_4','Southern entry with three interior approaches'),('paralogue_15','Noire arrives in northern enclosure on turn 2')]:
 M[mid]['starting_area']=C(mid,area,notes='Descriptive area only, not a certified coordinate map.')
for mid,name,cls,lv,eq in [('chapter_9','Campari','General',1,'Short Spear, Dracoshield'),('chapter_10','Mustafa','Berserker',1,'Short Axe, Beaststone'),('paralogue_5','Gecko','Assassin',10,'Silver Sword, Silver Bow, Second Seal')]:
 M[mid]['boss_override']=C(mid,[{'name':name,'class_name':cls,'level':lv,'equipment_text':eq,'equipment_stats':'UNKNOWN'}],notes='Guide Hard-default boss table; displayed stats/skills and enemy forges remain unknown.')
# The first interaction matters for this optional item, not for recruitment.
M['paralogue_5']['interactables'][0]=C('paralogue_5','NPC Sages give items when spoken to. Owain receives Missiletainn from the southeast Sage only if another unit has not already spoken to that Sage.')

review=dict(schema_version=1,reviewed_date='2026-10-02',maps=list(M.values()),additional_sources=extra,
 quarantines=[dict(ids=['p2_reviewed_wave_2','p2_reviewed_wave_3','p2_reviewed_wave_4'],chapter_id='chapter_15',reason='Map and difficulty heading loss: contents match Chapter 16 Lunatic subsection, not Chapter 15 Hard.',source_ids=['reinforcements_14_16_0','hr_fandom16','hr_jp_15'],status='RESOLVED_IMPORT_ERROR')],
 access_limitations=['GameFAQs guides and several wiki pages blocked/restricted; no bypass attempted.','Neoseeker guide and StrategyWiki returned 403; not used for new claims.','No gameplay footage was treated as observational evidence; difficulty and event state not established.','Gamer Guides mirrors and repeated source IDs are one evidence family; possible overlap with MK guide means not independent corroboration.'])
(P/'research/hard_verification/reviewed.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
print('Authored',len(M),'map reviews;',len(extra),'additional source records')

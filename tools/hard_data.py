#!/usr/bin/env python3
"""Offline rebuild of reviewed Hard/Classic claims; never borrows enemy mode data."""
import json
from common import ROOT,records
R=ROOT/'research/hard_verification'
CONFIDENCES={'VERIFIED','SUPPORTED','PARTIAL','CONFLICTED','UNKNOWN'}
CAMPAIGN_IDS=['prologue']+['chapter_'+str(n) for n in range(1,26)]+['endgame']+['paralogue_'+str(n) for n in range(1,18)]
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def unknown(note):return {'value':None,'confidence':'UNKNOWN','source_ids':[],'notes':note}
def main():
 review=json.loads((R/'reviewed.json').read_text());ss=json.loads((ROOT/'data/sources.json').read_text());sm={s['id']:s for s in ss}
 for s in review['additional_sources']:sm[s['id']]=s
 write(ROOT/'data/sources.json',list(sm.values()))
 source_docs(sm,review['additional_sources'])
 cm={c['id']:c for c in records('chapters')};chars=records('characters');maps=[];waves=[]
 for entry in review['maps']:
  mid=entry['id'];c=cm[mid];guide=entry['guide_id'];ws=entry['waves'];waves+=ws
  absence=entry['reinforcement_absence'];conflicts=entry['conflicts']
  objective={'value':c['objective'],'confidence':'SUPPORTED','source_ids':['chapter_catalog',guide], 'notes':'Campaign objective catalog compared against Hard-default guide; verify displayed objective before declaring completion.'}
  if any('catalog' in (x['value'] or {}) for x in conflicts):objective['confidence']='CONFLICTED'
  if mid=='chapter_15':objective['source_ids']=['chapter_catalog','hr_jp_15'];objective['notes']='Rout. Guide boss-only objective rejected against two chapter references; false reinforcement rows quarantined separately.'
  rs=[]
  for k in c['recruitable_units']:
   ch=next(x for x in chars if x['id']==k)
   rs.append({'unit_id':k,'condition':{'value':ch['recruitment']['condition'] if ch['recruitment']['condition']!='–' else 'Automatically at start','confidence':'SUPPORTED','source_ids':['recruitment',guide],'notes':'Recruitment system conditions checked against current Hard reference. Unit must survive to retain recruit in Classic.'}})
  initial=unknown('No complete Hard enemy roster, starting coordinates, numerical stats, enemy forges or random skill rolls certified. Observe actual enemies; Lunatic templates cannot substitute.')
  boss=c['difficulty_data']['Hard'].get('map_reference',{}).get('bosses') or None
  bossclaim={'value':boss,'confidence':'SUPPORTED' if boss else 'UNKNOWN','source_ids':[guide] if boss else [],'notes':'Hard-default guide metadata; exact displayed stats and equipped skill rolls remain unknown. Weapon names do not establish proc skills.'}
  row={'id':mid+'_hard_classic','chapter_id':mid,'name':c['name'],'difficulty':'Hard','mode':'Classic','scope':'ordinary_campaign','survey_checked':True,'confidence':'CONFLICTED' if conflicts else 'PARTIAL','source_ids':list(dict.fromkeys(['chapter_catalog',guide,'p2_guide_scope']+[s for w in ws for s in w['source_ids']]+([s for s in absence['source_ids']] if absence else []))),
   'objective':objective,'deployment':entry['deployment'],'starting_area':entry.get('starting_area',unknown('Exact Hard starting tiles not established; consult observed map.')),'initial_enemies':initial,'bosses':entry.get('boss_override',bossclaim),'recruitments':rs,
   'hazards':entry['hazards'],'activation':entry['activation'],'interactables':entry['interactables'],'interactables_complete':False,'shops':unknown('World-map shops are separate; full in-map shop/event inventory not established.'),
   'reinforcements':{'status':'present' if ws else 'none_supported' if absence else 'unknown','absence':absence,'wave_ids':[w['id'] for w in ws],'schedule_complete':False,'confidence':'CONFLICTED' if any(w['confidence']=='CONFLICTED' for w in ws) else 'PARTIAL' if ws else 'SUPPORTED' if absence else 'UNKNOWN','notes':'Explicit absence is one-source support, not certified game-script proof.' if absence else 'An empty or filtered wave list never establishes absence. Event-family records are not fully enumerated waves.'},
   'conflicts':conflicts,'unknowns':['Complete enemy roster/stats/skills/forges and coordinates','Full interactable geometry and scripted activation boundaries','Every reinforcement wave and exception to ordinary Hard immediate action']}
  # No invented pre-preparation deployment limits: army size differs from selection limit.
  if mid in ('prologue','chapter_1','chapter_2'):row['deployment']=unknown('No pre-battle selectable deployment limit established; automatic arrivals are not a deployment cap.')
  if absence:row['unknowns'].remove('Every reinforcement wave and exception to ordinary Hard immediate action')
  maps.append(row)
 write(ROOT/'data/chapters/hard_tactics.json',{'schema_version':1,'records':maps,'tutorial':{'chapter_id':'premonition','scope':'tutorial_not_counted_in_44','confidence':'PARTIAL','source_ids':['chapter_catalog','p2_guide_00_0'],'notes':'Scripted opening duel; general campaign reinforcement rules not asserted.'}})
 write(ROOT/'data/chapters/hard_reinforcements.json',{'schema_version':1,'records':waves})
 write(ROOT/'data/chapters/hard_quarantine.json',{'quarantines':review['quarantines']})
 # Preserve legacy facts as history, make bad Hard records unusable even by old tools.
 bad={k for q in review['quarantines'] for k in q['ids']}
 for filename in ('reinforcements','chapters'):
  p=ROOT/'data/chapters'/f'{filename}.json';d=json.loads(p.read_text())
  for row in d['records']:
   candidates=[row] if filename=='reinforcements' else (row['difficulty_data']['Hard']['reinforcements'] or [])
   for w in candidates:
    if w['id'] in bad:w.update(quarantined=True,quarantine_reason=review['quarantines'][0]['reason'],safe_for_tactical_certainty=False)
   if filename=='chapters' and row['id']=='chapter_15':
    for claim in row['difficulty_data']['Hard'].get('hazard_claims',[]):
     if 'reinforcements_14_16_0' in claim.get('source_ids',[]):claim.update(quarantined=True,quarantine_reason='Same contaminated source as misassigned waves; activation cannot establish Hard Chapter 15 behavior.')
  write(p,d)
 report(maps,waves)

def source_docs(sm,added):
 p=ROOT/'SOURCES.md';text=p.read_text();mark='\n## Hard / Classic forensic source additions'
 text=text.split(mark)[0]
 lines=[mark,'','Original additions accessed 2026-10-02; Chapter 17 inventory provenance revisited 2026-10-03 (individual dates in registry). '+str(len(added))+' registry IDs added; repeated publishers/URLs are not independent sources. `data/sources.json` is authoritative. Existing Serenes Forest recruitment/mechanics and chapter catalog are reused; no new Lunatic data imported.','','| ID | Source | Extracted scope | Limits |','|---|---|---|---|']
 for row in added:lines.append('| '+row['id']+' | ['+row['name']+']('+row['url']+') | '+', '.join(row['scope']).replace('|','/')+' | '+row['limitations'].replace('|','/')+' |')
 lines+=['','Evidence families: Gamer Guides/mirrors = one; indexed Fandom rows = one secondary editorial family; explicit Pegasus Knight Hard comments = original observational reports with Japanese-release limits; GBAtemp = independent player corroboration. No full copyrighted guide pages retained. Blocked GameFAQs/Neoseeker/StrategyWiki/Fandom pages were not bypassed. No gameplay footage accepted without visible Hard/state evidence. See `research/hard_verification/reviewed.json` for access limits and conflicts.']
 p.write_text(text+'\n'.join(lines)+'\n')

def report(maps,waves):
 counts={c:sum(m['confidence']==c for m in maps) for c in ['VERIFIED','SUPPORTED','PARTIAL','CONFLICTED','UNKNOWN']};wc={c:sum(w['confidence']==c for w in waves) for c in counts}
 r={'campaign_maps_checked':len(maps),'map_confidence':counts,'reinforcement_records':len(waves),'wave_confidence':wc,'event_family_records':[w['id'] for w in waves if w['timing']['value'].get('repeat') or w['timing']['value'].get('reported_start_turn') or w['id'] in ('hard_paralogue_17_flying_waves','hard_chapter_5_disputed_schedule')],'absence_supported':[m['chapter_id'] for m in maps if m['reinforcements']['status']=='none_supported'],'absence_verified':[],
 'ordinary_hard_same_turn_rule':'VERIFIED by Hard-specific guide and independent player report','maps_with_rule_applied':[m['chapter_id'] for m in maps if m['reinforcements']['status']=='present'],'maps_with_supported_spawn_phase':list(dict.fromkeys(w['chapter_id'] for w in waves if w['spawn_phase']['confidence'] in ('VERIFIED','SUPPORTED'))),'maps_with_directly_observed_immediate_action':[],'map_specific_script_exception_audits_complete':[],'complete_schedules':0,'readiness':'Suitable to BEGIN with evidence-aware assisted play, not a guarantee of an Ironman-safe route. Unknown hazards and incomplete schedules are always exposed; observed enemy data required for combat.'}
 write(R/'coverage_counts.json',r)
 lines=['# Hard / Classic tactical coverage — 2026-10-02','','44 ordinary campaign maps reviewed: Prologue, Chapters 1–25, Endgame, Paralogues 1–17. Premonition is a separate scripted tutorial; SpotPass/DLC remain outside this phase. Historical four-mode matrix: `research/hard_verification/previous_map_coverage.md`.','','**Map confidence is overall completeness, not the confidence of every individual fact.** VERIFIED = independent credible corroboration or strong game-derived evidence; SUPPORTED = one strong specific source; PARTIAL = important missing details; CONFLICTED = unresolved credible disagreement; UNKNOWN = no reliable evidence. No complete map/schedule is certified. Useful supported claims remain available on PARTIAL maps.','','Counts: '+json.dumps(counts)+'. Reinforcement records: '+str(len(waves))+' '+json.dumps(wc)+'. Event-family/unknown-group records are included; this is not a count of every actual wave.','','| Map | Tactical coverage | Reinforcement status | Recorded waves/families | Key unresolved risk |','|---|---|---|---:|---|']
 for m in maps:
  risk='Objective/arrival conflict; inspect in game' if m['confidence']=='CONFLICTED' else 'Initial roster, tiles and complete schedule missing' if m['reinforcements']['status']=='present' else 'Absence single-source; enemy observations required' if m['reinforcements']['status']=='none_supported' else 'Reinforcement existence/absence UNKNOWN'
  lines.append(f"| {m['chapter_id']} | {m['confidence']} | {m['reinforcements']['status']} | {len(m['reinforcements']['wave_ids'])} | {risk} |")
 lines+=['','## Immediate action and absence','','Ordinary Hard enemies appearing at the **beginning of enemy phase can move and attack immediately**, potentially killing on spawn. General rule is VERIFIED; application to each documented ordinary arrival is supported, but **no map has a complete scripted-exception audit**. '+str(len(r['maps_with_rule_applied']))+' maps have positive arrival evidence and rule-based immediate-action warnings. Unknown-phase scripted events require conservative treatment.','','Absence reasonably supported by explicit source statements: Chapter 15 (Hard-labelled Japanese original observation) and Chapter 22 (Hard-default guide). Neither absence is game-script VERIFIED. Other maps without recorded waves remain UNKNOWN, never “none.”','','## Highest-risk gaps','','Chapter 5: conflicting schedules/classes. Chapter 17: eastern versus western first staircase and conditional timing. Chapter 20: boss objective disagreement and warning-trigger timing. Chapters 9, 11, 13–14, 19, 21, 23–25, Endgame and Paralogues 8, 10–14, 17: schedules/spawn geometry not complete. Chapter 18 disappearing terrain/chest phase and Paralogue 16 changing-wall triggers are not fully established. Other empty schedules do not establish absence.','','Hard Chapter 16 now has separate supported 8/4/4-unit arrivals at reported turns 4/5/6. Old Chapter 15 records matching Chapter 16 Lunatic are quarantined, including the associated activation claim. Other-mode data remain separate.','','Use `python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase player`. This asks about the **current turn’s next enemy phase**, not turn 6. An enemy-phase query targets turn N+1. Missing/conditional events remain visible. All commands show only the selected map.','','See `docs/hard-reinforcements.md`, `research/hard_verification/reviewed.json`, `data/chapters/hard_tactics.json` and `data/chapters/hard_reinforcements.json` for field-level provenance and caveats.']
 (ROOT/'docs/map-coverage.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()

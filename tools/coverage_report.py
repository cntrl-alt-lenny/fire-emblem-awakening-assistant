#!/usr/bin/env python3
"""Regenerate a per-map/mode human coverage matrix from canonical audit data."""
import json
from common import ROOT,DIFFICULTIES

def main():
 rows=json.loads((ROOT/'data/chapters/coverage.json').read_text())['records'];maps={}
 for r in rows:maps.setdefault(r['map_id'],{})[r['difficulty']]=r
 text=['# Tactical map coverage — 2026-10-02','','51 story/paralogue maps × four separate difficulty modes. Every map received a source survey; no map has received a complete, independently verified tactical check. **P = partially verified; U = unresolved; V = verified. No V entries.** Partial means some sourced facts exist, not that the map is safe.','','## Overall map data','','| Map | Normal | Hard | Lunatic | Lunatic+ |','|---|---|---|---|---|']
 abbrev={'partially_verified':'P','unresolved':'U','verified':'V'}
 for mid,ds in maps.items():text.append('| '+mid+' | '+' | '.join(abbrev[ds[d]['map_status']] for d in DIFFICULTIES)+' |')
 text+=['','## Reinforcement schedules','','Partial includes a reported wave or unconfirmed absence claim. Timing, conditions, exact spawn tiles and immediate-action behavior are not all confirmed. Empty candidates never establish absence.','','| Map | Normal | Hard | Lunatic | Lunatic+ |','|---|---|---|---|---|']
 for mid,ds in maps.items():text.append('| '+mid+' | '+' | '.join(abbrev[ds[d]['reinforcement_status']] for d in DIFFICULTIES)+' |')
 text+=['','## Missing fields and evidence limits','','Enemy starting coordinates and reliable AI activation geometry remain UNKNOWN for all maps. Lunatic numerical templates are available for a subset; they preserve random skill slots and unknown enemy-forge parameters. Hard metadata includes deployment/boss/recruitment mentions; it is not a complete enemy roster. Normal and Lunatic+ enemy/map details remain unresolved. Villages/chests/doors/terrain and events are not comprehensively covered. Existing world-map shop tables do not establish in-map shop inventories.','','See `data/chapters/coverage.json` for counts and source IDs, `data/chapters/reinforcements.json` for individual claims, and `research/phase2/final_audit.json` for mode totals. `research/phase2/reviewed_additions.json` records investigated disagreements. Reader output can omit tables; an empty extract is not evidence of an empty map.','','## Next evidence required','','Obtain mode-specific map images/coordinates and event scripts or reliable independently cross-checked wave tables. Confirm trigger boundaries, spawn-blocking, phase and immediate action for each wave. Resolve Chapter5 turn disagreement before certifying it. Obtain actual observed enemy stats/skills/forge values for any live calculation. Certify absence only with complete checked evidence.']
 (ROOT/'docs/map-coverage.md').write_text('\n'.join(text)+'\n')
if __name__=='__main__':main()

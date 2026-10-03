# Independent manual tactical-danger audit — 2026-10-02

This review asks what could kill a unit even with all structural tests passing. No live run was created or modified. It does not claim playtesting or game-script verification.

| Simulated reliance | Danger found | Action / remaining limitation |
|---|---|---|
| Player phase 5, Chapter 7: ask about next enemy phase | Old query advanced to turn 6 and missed turn-5 arrival | New query requires phase; regression targets EP5 and includes three western Wyverns |
| Chapter 15: plan around old flying/bow arrivals | Indexed rows actually match Chapter 16 Lunatic | Preserve/quarantine three waves and associated AI assertion; old and new queries exclude them |
| Chapter 16: count reinforcements | Lunatic mixture would falsely give ten/six/six instead of Hard eight/four/four | Separate explicitly headed Hard subsection; precise count single-source SUPPORTED, tiles/skills unknown |
| Chapter 19: expect turn-8 reinforcements | Guide's turn-8 paragraph is explicitly Lunatic | Hard keeps fort presence but timing UNKNOWN |
| Chapter 5: park beside forts after apparent last wave | Conflicting counts/turns and flying approaches | No selected complete schedule; conflicts always visible; no end-of-wave safety claim |
| Chapter 17: screen only eastern stairs | Explicit Hard Japanese report says left first | First side CONFLICTED; warning timing conditional; no automatic all-safe route |
| Paralogue 10: kill enemy Villager or talk to Severa once | Holland is required; recruitment triggers stairs | Precise recruitment retained; killing Holland hazard exposed; trigger has no invented turn |
| Paralogue 14: visit village at end of turn | Visit can cause arrivals | Event family retained at all turns; exact phase and wave makeup UNKNOWN |
| Paralogue 17: body-block ground approach to Tiki | Fliers can target Tiki and bypass player | Independently corroborated targeting fact VERIFIED; exact arrivals/reach unknown |
| Chapter 18: collect chest exactly at quoted deadline | Destruction phase not established | Supported reported turn retained with explicit early-retrieval caveat; floor damage/path unknown |
| Paralogue 16: use wall as permanent shield | Walls change by area/turn, opening other routes | Map hazard retained; exact boundary UNKNOWN; enemy Counter must be inspected |
| Chapter 20 / early rout maps: kill boss assuming completion | Conflicting guide objective | Objective conflicts explicit; require displayed objective, not an invented resolution |
| Chapter with no imported waves | Source omission mistaken for absence | Explicit UNKNOWN status and additional-arrivals warning; none inferred from silence |
| “No enemy doubles” with speed difference four/five | Off-by-one doubling threshold | Regression tests four does not double; five does |
| Survive expected damage but fail on a crit / Brave / Vantage | Average hides lethal possible outcome | Worst HP, both death probabilities and attack ordering tested; no probability is certainty |
| Empty skill/partner/weakness defaults in an ordinary calculator input | Counter, effectiveness, Dual Strike/Guard silently missed | Strict live wrapper requires observed completeness and explicit fields; missing/null partner status UNKNOWN |
| Counter / Dragonskin / drain weapon / unsupported proc combination | Unsupported calculation falsely reassuring | Existing refusals preserved; strict wrapper returns UNKNOWN, not a stripped-effects answer |
| Two supplied enemy attacks but an unseen third arrives | Finite sequence is not a complete enemy phase | No map-survival claim; actual complete attackers, ranges, AI order and arrivals must be established separately |

Remaining danger: incomplete enemy positions/stats/forges/random skills and complete spawn enumeration across the campaign. These facts cannot be generated from class level, a tier list or Lunatic templates. Missing records are exposed at every selected-map query. A hypothetical move cannot be declared safe solely from this knowledge base. Observe current enemy panels, occupied spawn tiles, turn/phase, NPC status and warnings; if critical geometry or a trigger is unknown, say so and withhold the guarantee.

Readiness under the requested standard: **sufficient to BEGIN evidence-aware assisted Hard/Classic play**, because known, supported and uncertain claims are distinguished and unsafe omissions are not treated as absence. It is **not** a certified Ironman route database. Future maps with conflicts require current-map evidence before precise reinforcement-dependent positioning advice. No complete schedule has been certified.

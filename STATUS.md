# Build status — 2026-10-02, Hard / Classic forensic pass

**Sufficiently reliable to BEGIN evidence-aware Hard/Classic assisted play under the requested readiness standard.** The assistant can distinguish verified facts, useful supported facts and uncertainty, refuses unsupported combat outcomes and cannot silently treat missing map data as no threat. This is **not** a certified Ironman route reference: complete enemy geometry and complete reinforcement schedules remain unavailable. No playthrough was initialized; `CURRENT_RUN.md` and state files are unchanged.

The focused source survey, normalization, tooling, validation and separate manual danger audit are finished. Tactical data coverage remains partial. Prior status/coverage are preserved in `research/hard_verification/previous_STATUS.md` and `previous_map_coverage.md`; general data and other difficulty slots are preserved. Phase-two readiness assessed the stricter “without any unverified tactical information” standard and remains false in its historical audit. The current readiness judgment permits uncertainty when it is exposed and no unsupported guarantee is made.

## Coverage counters

| Requested measure | Result |
|---|---|
| Ordinary Hard campaign maps checked | **44**: Prologue + Chapters 1–25 + Endgame + Paralogues 1–17 |
| VERIFIED complete tactical maps | **0** |
| SUPPORTED complete tactical maps | **0** |
| PARTIAL tactical maps | **36** |
| CONFLICTED tactical maps | **8**: Prologue; Chapters 1, 2, 5, 6, 9, 17, 20 |
| UNKNOWN overall maps | **0**; every map has useful reviewed facts, but individual fields can be UNKNOWN |
| Reinforcement wave/event-family records | **29**; not the total actual wave count |
| VERIFIED individual complete wave records | **0** |
| SUPPORTED wave records | **5**: Chapter7 turn5; Chapter10 turn6; Chapter16 turns4/5/6 |
| PARTIAL / CONFLICTED / UNKNOWN wave records | **22 / 2 / 0**; many attributes within these are UNKNOWN |
| Reinforcement presence / supported absence / unknown existence | **23 / 2 / 19 maps** |
| Reasonably established absence | **Chapter15 and Chapter22, SUPPORTED**; zero game-script VERIFIED absences |
| Complete verified schedules | **0** |
| Same-turn rule | **VERIFIED general ordinary Hard rule**; applied conditionally to positive-arrival evidence on **23 maps** |
| Supported map-specific spawning phase + general action rule | **5 maps**: Chapters7,10,16,20 and Paralogue10; no independent observation of each individual wave |
| Complete map-specific scripted-exception audits | **0** |
| Tests passing | **115** at round 002, including 13 combat-gate regressions; historical forensic pass had 101 |
| Added source registry IDs | **16**, registry total **217**; IDs and mirrors do not equal independent sources |

Overall map confidence measures completeness and unresolved contradictions, not whether every fact on the map is doubtful. SUPPORTED precise facts remain useful on PARTIAL maps. Event-family records explicitly represent incomplete enumeration (village visits, continuous arrivals, Tiki-targeting waves, disputed Chapter5 schedule); do not present 29 as all actual waves. See `docs/map-coverage.md` and machine-readable `research/hard_verification/coverage_counts.json`.

Premonition is a separately tracked scripted tutorial, outside the 44 count. Procedural skirmishes need actual observed map/enemy state; no fixed schedule imported. SpotPass Paralogues18–23 and DLC remain separate and were not expanded.

## Important corrections and evidence

Three legacy Hard Chapter15 reinforcement rows and the related activation assertion are quarantined: lost headings assigned Chapter16 Lunatic content to Chapter15 Hard. They remain in historical data with explicit flags; both legacy and new queries exclude them. Chapter16's explicitly headed Hard subsection supports eight/four/four arrivals at reported turns4/5/6, not Lunatic ten/six/six. Exact spawn tiles, skill rolls and forges remain unknown.

General Hard ordinary arrivals can move/attack at enemy-phase beginning and kill immediately, supported by the Hard-specific Gamer Guides explanation and independent Hard player report. Do not assume a grace phase for unknown scripted arrivals. An unconfirmed scripted event's phase remains UNKNOWN; applying a general rule does not observe that event.

Chapter5 schedules/classes conflict. Chapter17 first staircase side and warning-relative timing conflict; later indexed rows with a lost mode boundary were excluded. Chapter19's explicitly Lunatic turn8 paragraph was not imported as Hard. Chapter7's Hard/Lunatic level disagreement is scoped separately instead of downgrading a good Hard-specific claim.

Recruitment conditions were rechecked against Serenes Forest, the Hard-default guide and a Japanese recruitment reference. Important current-map dangers include Holland/Severa event recruitment, village-triggered arrivals, Tiki-targeting fliers, changing walls, disappearing terrain/chests, Pass/Vantage/Counter and long-range weapons. Guide boss/rout/defend shorthand conflicts remain explicit on early maps and Chapter20; the game's displayed objective is required before a boss-rush conclusion. Chapter15 rout is preferred against guide shorthand using chapter references. Recruitment conditions do not supply actual child stats/classes.

Sources reused: Serenes Forest mechanics/recruitment and chapter catalog. Sources added: eight Pegasus Knight chapter/comment pages, Pegasus Knight recruitment, three missing Gamer Guides map pages, its Hard spawn rule page, explicit indexed Hard Fandom subsections for Chapters16/17 and an independent GBAtemp Hard report. Repeated guide mirrors and possible MK guide overlap are not independent corroboration. Restricted sources were not bypassed. No footage was accepted without visible difficulty/state. The registry records exact URLs, dates, applicability and limitations; only factual extracts are stored.

## Tools and files changed

New canonical `data/chapters/hard_tactics.json`, `hard_reinforcements.json`, `hard_quarantine.json`; updated `data/sources.json`. Legacy `chapters.json`/`reinforcements.json` only gain Hard quarantine flags. Non-Hard difficulty slots are unchanged.

New tools: `tools/map_info.py` (Hard current-map and phase-aware event query), `tools/tactical_combat.py` (strict observed-input safety gate), `tools/hard_data.py` (offline reviewed-data/source/report rebuild), `tools/audit_hard.py` (scope, confidence, references, timing and contamination audit). Updated `tools/tactical_query.py` (quarantine filtering, legacy timing notice), `Makefile` (new build/audit stages), `AGENTS.md`, `SOURCES.md`, `README.md`, this status and `docs/map-coverage.md`.

New tests: `tests/test_hard.py`. New reference: `docs/hard-reinforcements.md`. New factual research/audit artifacts are in `research/hard_verification/`: plan, reviewed extraction and authoring script, additional source registry, quarantine/conflict rationale, coverage counts, manual audit, validation, logs and rebuild/preservation report. No full webpages/guide prose were archived.

Example next enemy phase:

```sh
python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase player
```

This targets enemy phase5. `--phase enemy` would target phase6. A turn without a phase is rejected. Known supported claims and uncertain/conflicted parts are separate; unknown/event timing remains a candidate. No matching wave is not absence. Explicit single-source absence is useful support but does not set the stronger certainty flag. No-spoiler mode hides tactical details; normal assistant replies must stay concise and scope to current map.

Strict combat inputs require observed completeness, effective displayed stats, explicit support state/partner list, current HP, weapon/forge, ranks, all skills, weaknesses, terrain, combat bonuses, durability and distance. It reports worst HP and both death possibilities for supported duels; expected HP is not a guarantee. Missing data and Counter/Dragonskin/drain/unsupported procs or full dual outcomes return UNKNOWN. Existing calculator subset remains intact; no broad combat rewrite or EXP expansion was performed. Existing EXP ambiguity/refusals remain as previously documented.

Round 002 repairs the live input contract: custom/forged weapons require known
effect, Brave and effectiveness fields; canonical IDs resolve those fields
without changing data. Explicitly observed unequipped defenders remain
supported. Certain modeled death is LETHAL with the affected side named;
possible death remains POTENTIALLY_LETHAL. Supported numerical results and
the general calculator are unchanged. These regressions add no verified
gameplay facts, map coverage or complete schedules.

## Final verification and remaining danger

`make audit`: all original validation, phase-two semantic checks, new Hard audit and **101 tests pass**. Source IDs resolve; exact class/item references and 44-map inventory pass. Two offline rebuilds generated identical hashes for all **28 data JSON files**. All Normal/Lunatic/Lunatic+ chapter slots, `CURRENT_RUN.md` and state files are unchanged. `research/hard_verification/rebuild_and_preservation.json` contains checks; no run initialized. Tests verify invariants and regressions, not every source fact.

The separate manual audit in `research/hard_verification/manual_audit.md` tested Ironman-style failure scenarios and caused additional conservative fixes: unknown event phases remain unknown; adjacent support state is explicit; empty wave queries cannot reassure; single-source absence is not script certainty.

Remaining tactical-danger gaps: full initial enemy positions/stats/equipment/skill rolls/forges; complete spawn enumeration and tiles; activation boundaries and scripted exceptions. High-priority unresolved maps: Chapter5 and17 conflicts; Chapter20 warning trigger/objective; Chapters9,11,13–14,19,21,23–25/Endgame and Paralogues8,10–14,17 incomplete arrival schedules; Chapter18 disappearance phase and Paralogue16 wall triggers. The 19 maps lacking positive/absence evidence retain UNKNOWN reinforcement status. These do **not** prevent beginning under an uncertainty-aware standard, but they prevent unconditional reinforcement-dependent route guarantees.

Next work: obtain clearly Hard-labelled full wave tables or game-derived event evidence for Chapter5/17, then Chapter11/20/21/23–25 and child-map event families; verify coordinates and trigger boundaries through accessible map images or genuinely observable Hard footage. Do not spend effort on encyclopaedic expansion before these risks.

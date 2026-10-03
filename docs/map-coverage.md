# Hard / Classic tactical coverage — 2026-10-02

44 ordinary campaign maps reviewed: Prologue, Chapters 1–25, Endgame, Paralogues 1–17. Premonition is a separate scripted tutorial; SpotPass/DLC remain outside this phase. Historical four-mode matrix: `research/hard_verification/previous_map_coverage.md`.

**Map confidence is overall completeness, not the confidence of every individual fact.** VERIFIED = independent credible corroboration or strong game-derived evidence; SUPPORTED = one strong specific source; PARTIAL = important missing details; CONFLICTED = unresolved credible disagreement; UNKNOWN = no reliable evidence. No complete map/schedule is certified. Useful supported claims remain available on PARTIAL maps.

Counts: {"VERIFIED": 0, "SUPPORTED": 0, "PARTIAL": 36, "CONFLICTED": 8, "UNKNOWN": 0}. Reinforcement records: 29 {"VERIFIED": 0, "SUPPORTED": 5, "PARTIAL": 22, "CONFLICTED": 2, "UNKNOWN": 0}. Event-family/unknown-group records are included; this is not a count of every actual wave.

| Map | Tactical coverage | Reinforcement status | Recorded waves/families | Key unresolved risk |
|---|---|---|---:|---|
| prologue | CONFLICTED | unknown | 0 | Objective/arrival conflict; inspect in game |
| chapter_1 | CONFLICTED | unknown | 0 | Objective/arrival conflict; inspect in game |
| chapter_2 | CONFLICTED | unknown | 0 | Objective/arrival conflict; inspect in game |
| chapter_3 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| chapter_4 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| chapter_5 | CONFLICTED | present | 1 | Objective/arrival conflict; inspect in game |
| chapter_6 | CONFLICTED | unknown | 0 | Objective/arrival conflict; inspect in game |
| chapter_7 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| chapter_8 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| chapter_9 | CONFLICTED | present | 1 | Objective/arrival conflict; inspect in game |
| chapter_10 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| chapter_11 | PARTIAL | present | 2 | Initial roster, tiles and complete schedule missing |
| chapter_12 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| chapter_13 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| chapter_14 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| chapter_15 | PARTIAL | none_supported | 0 | Absence single-source; enemy observations required |
| chapter_16 | PARTIAL | present | 3 | Initial roster, tiles and complete schedule missing |
| chapter_17 | CONFLICTED | present | 3 | Objective/arrival conflict; inspect in game |
| chapter_18 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| chapter_19 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| chapter_20 | CONFLICTED | present | 1 | Objective/arrival conflict; inspect in game |
| chapter_21 | PARTIAL | present | 2 | Initial roster, tiles and complete schedule missing |
| chapter_22 | PARTIAL | none_supported | 0 | Absence single-source; enemy observations required |
| chapter_23 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| chapter_24 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| chapter_25 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| endgame | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| paralogue_1 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_2 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_3 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_4 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_5 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_6 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_7 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_8 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| paralogue_9 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_10 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| paralogue_11 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| paralogue_12 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| paralogue_13 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| paralogue_14 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |
| paralogue_15 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_16 | PARTIAL | unknown | 0 | Reinforcement existence/absence UNKNOWN |
| paralogue_17 | PARTIAL | present | 1 | Initial roster, tiles and complete schedule missing |

## Immediate action and absence

Ordinary Hard enemies appearing at the **beginning of enemy phase can move and attack immediately**, potentially killing on spawn. General rule is VERIFIED; application to each documented ordinary arrival is supported, but **no map has a complete scripted-exception audit**. 23 maps have positive arrival evidence and rule-based immediate-action warnings. Unknown-phase scripted events require conservative treatment.

Absence reasonably supported by explicit source statements: Chapter 15 (Hard-labelled Japanese original observation) and Chapter 22 (Hard-default guide). Neither absence is game-script VERIFIED. Other maps without recorded waves remain UNKNOWN, never “none.”

## Highest-risk gaps

Chapter 5: conflicting schedules/classes. Chapter 17: eastern versus western first staircase and conditional timing. Chapter 20: boss objective disagreement and warning-trigger timing. Chapters 9, 11, 13–14, 19, 21, 23–25, Endgame and Paralogues 8, 10–14, 17: schedules/spawn geometry not complete. Chapter 18 disappearing terrain/chest phase and Paralogue 16 changing-wall triggers are not fully established. Other empty schedules do not establish absence.

Hard Chapter 16 now has separate supported 8/4/4-unit arrivals at reported turns 4/5/6. Old Chapter 15 records matching Chapter 16 Lunatic are quarantined, including the associated activation claim. Other-mode data remain separate.

Use `python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase player`. This asks about the **current turn’s next enemy phase**, not turn 6. An enemy-phase query targets turn N+1. Missing/conditional events remain visible. All commands show only the selected map.

See `docs/hard-reinforcements.md`, `research/hard_verification/reviewed.json`, `data/chapters/hard_tactics.json` and `data/chapters/hard_reinforcements.json` for field-level provenance and caveats.

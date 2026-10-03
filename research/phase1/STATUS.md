# Build status — 2026-10-02

**Substantial initial reference and tested tools delivered; comprehensive research remains in progress.** Ready to begin recording a real run and answer supported calculations from observed inputs. Not ready to certify arbitrary map/reinforcement safety. No run is initialized, and no player difficulty/army has been assumed.

## Collected and normalized

| Dataset | Extent | Verification / remaining work |
|---|---|---|
| Characters | 49 story/children/SpotPass-story identities; recruitment, levels/classes, raw bases/bonus annotations, growths, cap modifiers, ranks, inventories and class sets | Single-source numerical tables; Robin configurable, children conditional; legacy bonus teams incomplete; Lunatic+ recruitment templates explicitly unknown |
| Classes | 55 sex variants/ordinary/special/DLC/enemy-NPC entries; bases, caps, movement, weapons, growths, skills/levels, reciprocal promotion graph, Pair Up bonuses | NPC growth/Pair Up gaps; exhaustive legality/availability audit incomplete |
| Weapons | 138 damaging entries across swords/lances/axes/bows/tomes/stones/claws/breath | Rank/stats/range/durability/Worth/effectiveness/effects retained; 107 have obtainability; axes/stones locations incomplete; restrictions must be checked |
| Items/staves | 59 entries, including 12 staves and three bullions | Uses/Worth/effects; bullion sell values sourced; other sell/discount pricing not inferred |
| Skills | 103 entries including obtainable, DLC/placeholders and enemy-only skills | Descriptions/activation, available class learning links; only selected combat effects implemented |
| Shops/economy | 48 shop locations, 49 travelling-merchant stock pools, 10-item rare pool, 33 renown rewards | Row-span stock groups normalized and item/chapter references checked; spawn probabilities and exact prices unfinished |
| Supports | 316 deduplicated fixed threshold edges; cumulative thresholds, Pair Up/Dual Support and fractional point rules | Generic Avatar and parent/sibling conditional edges not fully expanded; legality/point tracker incomplete |
| Maps | 28 main entries (premonition, prologue,1–25,endgame),23 paralogues,25 DLC map entries; names/objectives/boss/recruit catalog | Catalog complete for these lists; **303/304 difficulty slots unresearched**, one partial Chapter7 Lunatic table with22 enemies; most deployment/terrain/villages/chests/events unknown |
| Reinforcements | Chapter7 Lunatic partial record plus unreviewed search candidates | **Zero fully verified safe schedules**; mode/stat discrepancy and exact coordinates/triggers unresolved |
| Core mechanics | Reviewed formulas for damage/hit/crit/doubling/triangle/ranks/effectiveness, 2RN, Pair Up/dual rates, growths, caps, seals, internal levels, forging | Most single-source; full EXP/healing/rescue/terrain/status calculations incomplete |
| Other systems | Retained factual tables for birthdays/barracks, temporary boosts, world encounters, child availability | Partly staged/unreviewed; full movement/economy/legacy/DLC systems need further work |

The registry has66 source/extract IDs covering Serenes Forest/EmblemWiki, Fire Emblem Wiki, Nintendo's official manual, Pegasus Knight, Gamer Guides and Fandom. IDs include multiple sections of the same site; they are not independent confirmations. [SOURCES.md](SOURCES.md) gives exact URLs/scopes/limitations.

## Implemented tools

Offline lookup, combat forecast and conditional hit/crit outcome distribution, Pair Up/dual rates, sequential enemy-phase HP distribution, cap-aware average stats, actual-unit comparison, Avatar/child growth-cap resolver, forge quote, roster CRUD/state settings, explicit death/Casual recovery, inventory consumption, support updates, promotion/reclass history and level-gain recording. Atomic JSON state uses process locking and an append-only event ledger. Python standard library only.

Unsupported combat skills/effects and durability breakage raise errors. Full paired survival probability is not implemented. Class-change tracker records actual stats rather than guessing growth or promotion results. Reclass legality for inherited/DLC/unique class paths requires separate verification. `CURRENT_RUN.md` describes initialization and authoritative state.

## Validation completed

`make audit`: structural/reference/value/difficulty checks pass; 25 regression tests pass. Checks include all chapter1–25/paralogue1–23 IDs, four separate difficulty keys, enemy-to-map/mode consistency, class graph reciprocity, character/class/skill/inventory references, shop/merchant/renown references, source integrity, duplicate IDs, stat/rank ranges and support threshold edges. Fixtures exercise rank cancellation, doubling boundary, magical/effective attacks, Brave lethal interruption, 2RN, probability mass, unsupported refusals, Pair Up thresholds, caps/promotion averages, internal-level limits, Avatar/child formulas, forge quote, sequential HP, death persistence, consumption and failed atomic-update rollback.

Dedicated semantic audit removed a parsed skill header, corrected known icon/name inconsistencies, preserved child absolute bases and separated raw/effective stats. Search contamination is visibly quarantined. `research/audit.json` is the reproducible machine report. Passing tests validate supported implementations and structure, not every game fact. Source numeric cross-check remains incomplete.

## Recommended next research batches

1. Obtain reliable current-map enemy/reinforcement tables by difficulty, cross-check exact turns/conditions/coordinates and mark tactical certification only after verification. Fill deployment/objectives/events/terrain/chests/villages for every map.
2. Resolve EXP sign/convention issues, healing/rescue/rank/terrain formulas and full skill activation/priority/dual combat mechanics with independent game-derived evidence.
3. Audit class/weapon restrictions and child base/autolevel/class inheritance edge cases; expand conditional support legality.
4. Fill remaining weapon/item obtainability, economy details, movement costs, statuses, legacy SpotPass characters and full DLC-specific mechanics.
5. Broaden independent numerical spot checks. Add regression fixtures only for newly supported mechanics; retain explicit uncertainty elsewhere.

Work can resume from the retained factual staging tables and offline build/enrichment scripts. No access controls were bypassed, no full webpages were archived and no external service is required to use this project.

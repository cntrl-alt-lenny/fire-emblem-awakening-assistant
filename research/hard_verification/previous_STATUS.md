# Build status — 2026-10-02, tactical correctness phase

**Expanded and audited; this phase is partially complete. Not sufficiently reliable to begin a Hard/Classic playthrough without relying on unverified tactical information.** No playthrough was initialized. Existing run state was not changed. Phase-one status/audit snapshots are retained in `research/phase1/`.

## Map coverage

All 28 main-story entries and 23 paralogues received a systematic source survey. This is an attempted research inventory, not proof that every map was fully checked. There are 204 explicit story/paralogue difficulty slots; 25 DLC catalog entries remain outside this phase.

| Difficulty | Verified maps | Partial maps | Unresolved maps | Partial reinforcement schedules | Unresolved reinforcement schedules |
|---|---:|---:|---:|---:|---:|
| Normal | 0 | 0 | 51 | 0 | 51 |
| Hard | 0 | 46 | 5 | 10 | 41 |
| Lunatic | 0 | 36 | 15 | 17 | 34 |
| Lunatic+ | 0 | 0 | 51 | 0 | 51 |

[Per-map/mode report](docs/map-coverage.md) and `data/chapters/coverage.json` show every slot. **Zero fully verified reinforcement schedules.** 74 partial wave records retain mode, source, reported turns or event triggers, available unit/equipment/location claims and explicit unknowns. Two Hard maps have unconfirmed no-reinforcement claims; those are not certified absence.

1,104 representative Lunatic enemy rows across 36 maps retain numerical stats, class, equipment strings, known/random skills, source bonus annotations and forge markers. Some are incomplete indexed extracts or have unknown starting/reinforcement phase because the reader omitted a heading. No positions are invented. Enemy `+`/`++` forge values remain UNKNOWN. The rows must not be used as exact spawned units. Lunatic data is never copied to Lunatic+.

Hard deployment/boss/recruitment metadata was obtained for 45 maps; an additional map has a reinforcement claim. Recruitment mentions may describe the previous chapter. Objectives in the existing catalog are not overwritten by guide summaries that use different wording. Coordinates, terrain/interactable coverage, complete Hard enemy rosters, AI activation geometry and map-specific immediate-action confirmation remain major gaps. Normal and Lunatic+ tactical detail remain unresolved.

Investigated discrepancies: Chapter5 grouped Hard/Lunatic turns disagree with the Lunatic table; Chapter7 grouped levels disagree with separate Lunatic values; Chapter22 grave/road excerpt appears contaminated by another map and is quarantined. Source agreement on one field never certifies the complete wave. Some public sources failed access or returned omitted reader content; failures were respected, and unrelated/script/strategy excerpts were discarded from new staging files.

## Combat tools

The existing damage/hit/critical/triangle/rank/effectiveness/range/Brave/terrain-input model now includes supported isolated Luna, Ignis, Vengeance, Sol, Pavise, Aegis, Miracle, Vantage, Wrath, Rightful King/God and enemy Hawkeye/Luna+/Vantage+/Pavise+/Aegis+. Vantage and Wrath use inclusive half-HP boundaries. Critical damage follows offensive effects; defensive halving follows criticals. HP-dependent effects are reevaluated after damage. Stone guard categories distinguish Beaststone from Dragonstone.

Results separate nominal forecasts from modeled HP distributions, minima/maxima, death probability and deterministic classification. Exactness is conditional on effective stats, complete skills, exact weapon/forge, range, terrain/bonuses, enough durability and the independent uniform random model. Expected HP is never a guarantee. Enemy-phase checks now reject insufficient total player weapon durability across the supplied sequence.

**Unresolved/refused:** full Dual Strike/Guard outcomes and support weapon ordering; Aether/Astra/Lethality/Counter/Dragonskin/Nosferatu and other unimplemented effects; multiple probabilistic offensive procs with unverified RNG dependence; combined defensive procs; Luna with terrain defense; Sol overkill healing cap; weapon breakage and post-kill/post-map effects. Pair Up stats, support combat bonuses and dual rates are supported separately; `paired_forecast.py` applies those once and explicitly leaves full outcome UNKNOWN. Restricted weapon eligibility remains separate; dark-tome table color was lost in extraction and is explicitly flagged, not guessed.

## EXP/progression

`experience.py` implements chip/kill/boss/class/unit categories, promoted-enemy levels, support shares, staff/Dance EXP, ordinary-unpromoted difficulty bonuses, clamps and special level exceptions from known internal levels. It passes the original reported 35-entry Champions of Yore sequence and eight Rescue examples. Staff penalty uses final-expression truncation, matching the reported sequence; subtracting a floored penalty overstated some values.

Repeated Lunatic engagement penalty has a published sign contradiction: default refuses engagements four onward; an explicitly labeled interpretation is available. Fractional support/Veteran/Paragon rounding also requires explicit opt-in. Original forum observations are the source behind Serenes formulas, not independent corroboration. Existing seal/internal-level and cap-aware class-path averages remain supported; unknown seal history, child recruited bases and complete inherited class legality remain unresolved. Special classes do not acquire the promoted +20 merely because their level cap is30.

`healing.py` supports sourced Mend/Physic/Recover, effective Magic, staff rank/Healtouch, range, HP caps and durability. Other staff healing coefficients remain unsupported.

## Second-pass audit and queries

Corrected dropped Brave flags for Celica's Gale/Waste, missing Skill/Luck spelling aliases and combined Defense/Resistance weapon bonuses including Micaiah's Pyre. Independently checked 15 numerical fields for Iron Sword/Mend/Physic, plus Pavise General level15, weapon categories and inclusive Vantage/Wrath boundaries against game-derived text. This is a targeted audit, not exhaustive independent validation of all 49 character/55 class/138 weapon/59 item/103 skill records. Robin/gender/child/DLC/SpotPass exception coverage remains partial as documented in `research/UNCERTAINTIES.md`.

`tactical_query.py` returns next-turn reported candidates, event-triggered/unknown-timing waves, source IDs and a permanent incomplete-schedule warning. It cannot conclude no waves from an empty result and does not invent AI zones. No-spoilers output suppresses detailed map claims. `paired_forecast.py`, `enemy_phase.py` and combat distributions help answer supplied-state questions; no automatic enemy template-to-battle conversion is provided.

## Final verification

`make rebuild` completed entirely offline; `make audit` passed structural/provenance/difficulty checks, semantic checks and **60 regression tests**. Two offline rebuilds produced identical SHA-256 hashes for all25 canonical JSON files. `research/audit.json`, `research/phase2/final_audit.json`, `research/phase2/offline_rebuild.log` and `research/phase2/validation_and_tests.log` retain results. Tests validate supported code and specific examples, not missing map facts. All sources remain registered; source IDs are extracts, not independent publishers.

Next priorities: complete and cross-check Hard map schedules/coordinates/triggers/immediate action; obtain game-derived AI/event evidence and Lunatic+ skill rolls; finish full paired combat and proc interaction evidence; resolve EXP multiplier/repeated-engagement rounding; expand independent numeric and class/child/gender legality audits. Current tools are useful for observed-input calculations and tracking, but the requested tactical-readiness standard is not met.

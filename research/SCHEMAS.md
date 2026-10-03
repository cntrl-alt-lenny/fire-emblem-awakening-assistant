# Schemas v1

Canonical entities use ASCII snake_case IDs; display names preserve localization. JSON is the reference store; No SQLite store is needed for this small catalog. Mutable playthrough state is JSON with append-only events and atomic updates.

`data/sources.json`: id, name, URL, accessed date, scope, limitations, retrieval outcome.
`research/*.json`: selected factual table cells only, source_id, caption/section, headers, rows, verification=`extracted_unreviewed`. Never complete HTML or narrative guide prose.
Canonical datasets: `schema_version`, `records`; each entity has `id`, `name`, `source_ids`, `verification`, typed fields. Field-specific sources used when merging tables. Numeric strings are not silently coerced where they contain alternatives. Condition/difficulty-dependent values retain original factual cells in the staging store until reviewed.
Chapters: `kind`, `number`, `difficulty_data` keyed Normal/Hard/Lunatic/Lunatic+; each has explicit status, enemies, reinforcements (null if unknown). No inheritance between difficulties without sourced equivalence.
Run state: difficulty, mode, spoiler_mode, chapter, turn, units keyed canonical ID; each unit has class, level, exp, stats, weapon_ranks, inventory (instances with durability), skills, supports, alive, history. Unknown fields null. Ledger events have timestamp, before/after and note. Death persists until explicit correction. No automatically initialized generic army.
Mechanics: equations/parameters, applicability, sources, confidence, implemented flag, limitations.

## Tactical correctness phase schemas

`data/chapters/coverage.json`:204 records keyed by map/difficulty, with separate overall/reinforcement status, enemy/wave counts, provenance and false tactical certification. `data/chapters/reinforcements.json` retains each mode-specific claim: reported turns versus event triggers, locations/coordinates, unit templates or factual unit/equipment claims, spawn phase/action evidence, source IDs, cross-check status and completeness. `UNKNOWN` or null never means absent.

Expanded enemy records preserve source class spelling, numeric base values plus source bonus annotations, equipment source text and enemy forge markers. Canonical weapon IDs identify base references only; unknown enemy forge parameters cannot be silently replaced. Known/random skill slots, position and initial/scripted phase uncertainty are explicit. Tables are representative, not exact spawned units.

Hard map metadata lives inside its difficulty slot. Existing generic catalog metadata is not overwritten from Hard guide values. `reported_absence`, `hazard_claims` and `conflicts` have individual sources and do not certify an entire map. Normal/Lunatic+ are never populated from Lunatic templates.

Combat output distinguishes nominal forecast, supported outcome states/probabilities/minima/maxima and deterministic classification. Paired preview intentionally has no full HP outcome. EXP results include verification/interpretation state. Canonical progression formula metadata is in `data/mechanics/progression.json`; source records remain in the shared registry.

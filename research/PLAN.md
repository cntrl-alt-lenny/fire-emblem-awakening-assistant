# Research inventory and completion standard

Status: substantial initial build delivered; comprehensive research incomplete. See ../STATUS.md for measured coverage and next work. No complete-coverage claim.

Source hierarchy: observed unmodified game data / official manual for controls and modes; established numerical references (Serenes Forest); independent Fire Emblem Wiki cross-checks; established guides; community reports only with explicit uncertainty. Do not confuse a wiki with primary game data. Region defaults to English international naming; version-specific claims need tags.

| Batch | Required data | Initial status |
|---|---|---|
| Characters | recruitment, bases, growths, caps, ranks, inventory, class sets, Avatar | partial — see STATUS.md |
| Classes | bases, caps, growths, movement, weapons, skills, promotion graph | partial — see STATUS.md |
| Inventory | all weapon types, staves, stones, items, forging, obtainability | partial — see STATUS.md |
| Combat | formulas, rounding, rank/triangle, doubling, probability, skills | partial — see STATUS.md |
| Pair/support | bonuses, compatibility, growth, marriage, inheritance | partial — see STATUS.md |
| Maps | main, paralogues, DLC; separate difficulty enemies/reinforcements | partial — see STATUS.md |
| Progression | seals, EXP, internal levels, caps, growth expectations | partial — see STATUS.md |
| Other systems | shops, merchants, barracks, renown, encounters, movement | partial — see STATUS.md |
| Tools | tracking, calculator, averages, comparison, query, audit | partial — see STATUS.md |
| Audit | schema/reference checks, numerical sanity, omissions, tests | partial — see STATUS.md |

Each dataset carries source IDs and verification state. Empty or null means unknown, never zero or no enemies. A reinforcement schedule cannot be treated as safe until difficulty and triggers are confirmed. Parsed facts require semantic review. Coverage is tracked independently of parser success.

## Tactical correctness phase checklist

- [x] Preserve prior status/audit snapshots; no run initialization.
- [x] Survey every story/paralogue; produce complete204-slot mode coverage report.
- [x] Expand conservative enemy/wave records with provenance and explicit unknowns.
- [ ] Fully check every mode/map enemy position, equipment, skills, stats and events.
- [ ] Independently certify reinforcement turns/triggers/coordinates/action for every map.
- [x] Audit supported combat; add isolated skill events, risk distributions and regression refusals.
- [ ] Full paired combat, remaining multi-hit/reflect/drain interactions and proc RNG ordering.
- [x] Add supported EXP/staff/healing with original worked examples and explicit ambiguity refusals.
- [ ] Resolve repeated Lunatic/multiplier rounding and all staff coefficients.
- [x] Correct strategically important dropped weapon properties and limited independent numerical spot checks.
- [ ] Exhaustive second-source character/class/gender/Robin/child/DLC/SpotPass audit.
- [x] Add conservative current-map query, paired preview and stronger semantic validation.
- [x] Offline rebuild, deterministic hash comparison, source checks and60 passing tests.

This checklist is partial completion, not tactical readiness. Consult ../STATUS.md for the false Hard/Classic readiness judgment and next work.

# 12-play-briefing — Checked plan and prompts

Goal: concise current-map evidence without unsafe omissions. The current
Chapter7 map example prints 333 lines; its JSON remains the detailed reference.

## Worker — send with batches 10 and 11

```text
Fire Emblem Awakening Assistant · BATCH 12-play-briefing · WORKER

Run python3 tools/fw.py status. Read AGENTS.md, framework/Worker/state/full tactical policy. Fetch; resolve origin/brain/roadmap-2026-10-09 and starting origin/main to full commits. Read docs/plans/12-play-briefing.md and docs/plans/roadmap-2026-10-09.md via git show at the recorded plan commit, even if absent from main. Branch worker/12-play-briefing in its own linked checkout from main. Do not wait for planning merge or other batches.

Own only new tools/play_briefing.py, tests/test_play_briefing.py, docs/play-briefing.md and own batch summary/evidence. Do not edit map_info, tactical gates/calculators, canonical/generated data/reports, trackers, shared tests, STATUS/usage/README/framework.

Add one read-only CLI that renders map_info.query results as a concise current-map briefing: selected map/difficulty, explicit current/target phase, useful sourced facts, candidate arrival families, hazards/conflicts and the material unknowns. Preserve confidence and visible uncertainty; unknown or empty schedules never imply absence. Use details/provenance output for complete claims. Deterministic concise output should make the baseline Chapter7 case readable in roughly 30 lines without dropping material risk; document any justified exception. Do not truncate unique dangers merely to meet a line budget.

Accept explicit map/turn/phase/spoiler parameters. Optional explicitly selected --state may read existing run chapter/turn/spoiler settings; state does not record phase, so require it rather than infer. Validate mismatched explicit/state context rather than silently using a different map; reject unsupported difficulties. Do not derive combat-effective stats from tracked raw/displayed values, initialize state, update files or recommend deployment units.

Respect No spoilers: no tactical event/recruit/claim/source-title leaks; explain detailed material withheld and retain general incomplete-map warning. Tactical spoilers stay on selected map. Test player/enemy boundaries, Chapter11 candidate family, known fixed controls, conflicts, supported absence versus certainty, missing/unknown context, malformed/missing state and no future-map output. Use synthetic state only and prove read-only byte preservation plus canonical/private file-set preservation.

Show examples of before/after output and meaningful CLI acceptance. Run make audit, fw.py check, focused tests, branch-wide git diff --check at committed code; retain actual output/exits/failures. Render new reference and inspect links. No rebuild or verified gameplay coverage increase. Commit docs/batches/12-play-briefing.md in four framework sections (500 prose words), push full delivery commit, never merge. Shared questions go to Brain.
```

## Verifier — only after Worker delivery

```text
Fire Emblem Awakening Assistant · BATCH 12-play-briefing · VERIFIER
Start status and all project/Verifier/tactical rules. Brain supplies literal delivery/baseline/plan; fetch-confirm, detach checkout. Before diff/new tests/Worker conclusions, privately list material baseline current-map claims/unknowns and spoiler-filter boundaries. Then inspect production first. Independently compare briefing against raw queries, including phase/fixed/event/conflict/absence controls. Challenge state mismatch/missing phase, spoiler leaks through labels/source titles and unsafe omissions. Require read-only synthetic/data/private preservation, CLI examples, audit/fw/diff evidence and rendered docs/links. Write only docs/batches/12-play-briefing-review.md with exact commit, blind order, classified findings/verdict and real command evidence, <=500 prose words plus tables. No fixes/merges; guard report-only push and report to Brain.
```

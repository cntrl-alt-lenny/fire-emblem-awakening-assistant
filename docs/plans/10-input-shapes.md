# 10-input-shapes — Checked plan and prompts

Goal: close observed-input shape leaks without changing supported mechanics.
At baseline `e78fa7bcc245071556a408f725105ac63ce7a8e9`, Brain reproduced
numeric outcomes for defender skills/weaknesses set to empty objects/strings,
and current_hp set to true or 1.5. These are new broader-contract findings;
08/09 acceptance concerned different bounded criteria.

## Worker — send with batches 11 and 12

```text
Fire Emblem Awakening Assistant · BATCH 10-input-shapes · WORKER

Run python3 tools/fw.py status. Read AGENTS.md, framework, Worker card, standing decisions and full tactical policy. Fetch; record full starting origin/main and pushed origin/brain/roadmap-2026-10-09 plan commit. Read docs/plans/10-input-shapes.md and docs/plans/roadmap-2026-10-09.md via git show at that commit, even if absent from main. Branch worker/10-input-shapes in .worktrees/worker-10-input-shapes from main. Planning need not be merged.

Establish and close malformed live-observation leaks at assess(payload), preserving its API/result contract. Own tools/tactical_combat.py, new tests/test_combat_input_shapes.py, new docs/combat-input-shapes.md and your summary/evidence only. Do not edit general calculator, canonical data, tracker, sequence/briefing files, shared tests, STATUS, usage or framework.

Require skills/weaknesses to be lists of string IDs/categories, without conversion or deletion of effects. Preserve existing supported/unsupported skill and weakness membership checks. Require current_hp to be an actual integer, not boolean/float; preserve existing 1..observed max-HP boundary. Establish any directly related shape leak needed for this contract and report broader issues to Brain. Both combatants, missing/null/malformed collections/elements, unsupported IDs and HP boundaries must refuse with UNKNOWN/null and side/field diagnostics. Explicit [] and legal integer HP remain supported. Keep skill-context checks and unequipped-defender behavior.

Use synthetic inputs only. Privately compare canonical/private file sets/content before/after; never publish run data/hashes. Prove baseline failures by direct call and public JSON CLI, immutable inputs, unchanged full supported outputs, and existing Counter/drain/paired/proc refusals. Run make audit, python3 tools/fw.py check, focused tests and branch-wide git diff --check at committed code; retain actual outputs/exits and failed attempts. Render reference and resolve links. No rebuild/new run/new gameplay coverage.

Commit docs/batches/10-input-shapes.md with Done, Checked, Not checked, Failed or blocked, at most 500 prose words. Push, state full delivery commit and await fresh blind review. Never merge. Technical/shared-contract questions go to Brain. Batches 11/12 may run concurrently.
```

## Verifier — only after Worker delivery

```text
Fire Emblem Awakening Assistant · BATCH 10-input-shapes · VERIFIER
Start with fw.py status and all project/Verifier/tactical rules. Brain supplies literal Worker commit and recorded baseline/plan; fetch and confirm tip before review. Use a separate detached checkout. Before reading changed gate/tests/docs/Worker conclusions, privately challenge original assess on both sides with malformed collections/elements and HP types/bounds. Then inspect production diff, tests and summary. Independently prove refusals and complete supported equality, CLI semantics, input/data/private preservation and unchanged unsupported effects. Run full audit/fw/diff checks, render docs/links. Commit only docs/batches/10-input-shapes-review.md (500 prose words maximum, evidence tables excluded), with exact commit, blind order, commands/output/exits, classified findings and verdict. No fixes or merges; report to Brain. Guard any report-only push against a changed Worker tip.
```

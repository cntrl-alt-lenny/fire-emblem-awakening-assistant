# Two useful independent Worker batches

Owner instruction recorded 2026-10-09. Maintain two active Workers when this
reduces waiting and delivers useful independent progress; never invent busywork.
Existing Worker 08 continues. Worker 09 may start now from main using this pushed
plan. The Brain refresh PR need not be merged for either to read its instructions.

| Batch | Product outcome | Exclusive implementation ownership |
|---|---|---|
| [08-chapter11-candidates](08-chapter11-candidates.md) | Keep unresolved fort-arrival timing visible in phase-filtered queries | Chapter 11 Hard records/authoring; map_info, audit_hard, hard_data; test_hard; affected Hard generated docs/counters and STATUS; its summary/evidence |
| [09-combat-context](09-combat-context.md) | Refuse numerical live-combat outcomes when required skill context is unknown or malformed | tactical_combat; new test_combat_context; new combat-context reference; its summary/evidence |

Both use distinct `worker/<batch>` branches and linked checkouts. Both are
Checked: separate fresh blind Verifier reviews at exact commits, then Brain
re-derivation and owner approval. Tests and builds run within each checkout;
never run another Worker's checks in the shared primary checkout.

No implementation dependency exists: both read stable combat fixtures, but
Worker 09 puts regressions in a new test file and does not edit Worker 08's
fixture file. No concurrent ownership of canonical data or generated reports.
Brain reviews numerical/control behavior after combining accepted branches and
reruns full audits. This combined check genuinely waits for both deliveries;
it does not prevent either implementation or its own review from starting.
Workers report newly discovered shared-file requirements to Brain rather than
editing each other's scope. Brain owns STATUS reconciliation and merge order.

## Worker 08 prompt — continue, do not restart

```text
Fire Emblem Awakening Assistant · BATCH 08-chapter11-candidates · WORKER

Continue your already-running batch on worker/08-chapter11-candidates; do not restart or duplicate it. Run python3 tools/fw.py status in your own checkout, read project rules and tactical policy, and retain the agreed plan, baseline and evidence requirements.

You own Chapter 11 Hard timing records and their authoring/rebuild path, tools/map_info.py, tools/audit_hard.py, tools/hard_data.py, tests/test_hard.py and affected Hard generated docs/counters/STATUS, plus your summary/evidence. Worker 09 separately owns tools/tactical_combat.py and a new combat-context test/reference. Do not edit those files or wait for Worker 09, its review or the Brain refresh merge. Report any newly necessary shared-file change to Brain.

Deliver conservative fort-family filtering without inventing repeated spawns or a last turn. Preserve separate fixed-turn controls, all unknowns, quarantine, other difficulties and private player state. Show failing baseline regressions, phase-boundary controls, two rebuild hash comparisons, full audits and preservation evidence at committed code. Render changed documents and inspect links. Record real output/exits and failed attempts.

Commit docs/batches/08-chapter11-candidates.md with Done, Checked, Not checked, Failed or blocked (500 prose words maximum), then push. No gameplay operations, new runs or merges. Technical questions go to Brain. End with batch, WORKER, outcome and pushed full commit.
```

## Worker 09 prompt — start independently

```text
Fire Emblem Awakening Assistant · BATCH 09-combat-context · WORKER

Run python3 tools/fw.py status. Read AGENTS.md, framework, worker card, standing decisions and full tactical policy. Fetch origin, resolve origin/brain/refresh-2026-10-08 to a full commit, and read docs/plans/09-combat-context.md and docs/plans/parallel-workers.md via git show at that commit. Record the plan commit. The plans need not be on main; the pending framework patch/refresh PR does not block this work.

Start from origin/main in a distinct linked checkout .worktrees/worker-09-combat-context on worker/09-combat-context; record the full starting main commit. Execute the plan: refuse missing/malformed skill-required outdoors/turn context on either side, while preserving supported numerical behavior and optional omissions. Own only tools/tactical_combat.py, new tests/test_combat_context.py, new docs/combat-context.md and your batch summary/evidence. Do not edit map/data/rebuild/shared-test/STATUS/framework/general-calculator files or merge Brain/Worker 08 branches. Report a concrete cross-scope dependency to Brain if found.

Privately snapshot canonical JSON and CURRENT_RUN.md plus every regular state file; compare sets/content after work/checks. Show baseline-failing regressions, both-side malformed and positive boundary/parity cases, supported numerical equality, CLI behavior, input immutability and unchanged refusals. At committed code run make audit, python3 tools/fw.py check, git diff --check and focused tests. Record real commands/output/exits and failures. Render the new reference, visually inspect and resolve links. No canonical/rebuild change or new gameplay coverage; do not rebuild or initialize a run.

Commit docs/batches/09-combat-context.md with Done, Checked, Not checked, Failed or blocked (500 prose words maximum, output tables excluded), stating plan/start/implementation full commits. Push. Do not merge; questions go to Brain. End with batch, WORKER, outcome and pushed full commit.
```

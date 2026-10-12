# 11-observed-sequence — Checked plan and prompts

Goal: make live supplied-attack sequences refuse assumptions. The existing
reference calculator remains available with its documented assumptions.
At baseline `e78fa7bcc245071556a408f725105ac63ce7a8e9`, the example with
player current_hp/durability removed still returns death probability 0,
minimum HP 10. That does not establish an observed survival result.

## Worker — send with batches 10 and 12

```text
Fire Emblem Awakening Assistant · BATCH 11-observed-sequence · WORKER

Run python3 tools/fw.py status. Read AGENTS.md, framework/Worker/state/full tactical policy. Fetch; resolve origin/brain/roadmap-2026-10-09 and starting origin/main to full commits. Read docs/plans/11-observed-sequence.md and docs/plans/roadmap-2026-10-09.md via git show at the recorded plan commit, even if absent from main. Branch worker/11-observed-sequence in its own linked checkout from main; no planning-merge wait.

Own only new tools/tactical_enemy_phase.py, tests/test_tactical_enemy_phase.py, docs/observed-enemy-sequence.md, examples/observed_enemy_sequence.json and your batch summary/evidence. Do not edit enemy_phase, tactical_combat, general calculator/proc engine, trackers, canonical data, shared tests/STATUS/usage/framework or briefing files.

Add a strict read-only Hard/Classic entry point for an explicitly supplied attack order. Define/document a small observed input contract, reuse assess(payload) for each player/enemy duel, and compose only supported state distributions. Require actual effective stats/current HP, weapon/forge/durability, ranks/skills/weaknesses, context, confirmed no partners/support and observation completeness. Enforce this wrapper’s required collection/HP types before assess; the starting gate still has shape gaps. Keep sequence validation narrow and copy no combat formulas. Never infer max HP or sufficient uses. Require distinct explicitly identified attackers; repeated-entity sequences/AI targeting/order/paths remain outside scope. Do not add mechanics or broaden supported procs. Preflight every attacker so unsupported/malformed later inputs invalidate the whole numerical sequence even if an earlier modeled kill would hide them.

For complete supported cases, independently rederive HP-distribution composition, dead-player absorption, early kills and cumulative maximum retaliation durability. Refuse possible breakage; retain existing calculator refusals. Return UNKNOWN with no numerical outcome for incomplete/unsupported sequences; diagnostics identify the entry/side/field. Any accepted zero modeled death stays conditional on this supplied sequence, with map safety false. Preserve input immutability.

Use temporary synthetic states. Show baseline-assumption examples, refusal cases, supported numerical controls, public CLI, all-attackers preflight and preservation. Snapshot canonical/private file sets privately. Run make audit, fw.py check, focused tests and branch-wide git diff --check at committed code; record output/exits/failures. Render reference and inspect links. No rebuild/live run/coverage increase.

The assess API is stable; implement and review independently while batch 10 hardens it. Brain checks both together before release. Report a concrete API/ownership dependency rather than editing batch 10. Commit docs/batches/11-observed-sequence.md in four framework sections (500 prose words maximum), push full delivery commit, never merge.
```

## Verifier — only after Worker delivery

```text
Fire Emblem Awakening Assistant · BATCH 11-observed-sequence · VERIFIER
Start with status and all project/Verifier/tactical rules. Brain supplies exact delivery/baseline/plan; fetch-confirm tip, use detached checkout. Before diff/new tests/Worker conclusions, privately derive baseline assumptions and an independent small ordered-attack HP distribution. Inspect production first. Challenge incomplete inputs, unsupported tails, repeated entities, death absorption, early kills, cumulative durability and conditional zero-risk labels. Require CLI/input/canonical/private preservation, full audit/fw/diff evidence and rendered docs/links. Write only docs/batches/11-observed-sequence-review.md, capped 500 prose words plus evidence tables, exact commit/blind order/classified findings/verdict. No implementations or merges; guard report-only push and return to Brain.
```

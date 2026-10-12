# 15-duel-boundary — Checked plan

Close the direct duel gate's remaining observation-shape gaps. The guided editor
guards them, but direct API/JSON callers still obtain numbers with unknown alive
state, empty forge markers or unknown supplied effects. Starting main:
`ec3bceca1d70a4da240a490601602e97c2466de2`.

## Worker prompt — send together with batch 16

```text
Fire Emblem Awakening Assistant · BATCH 15-duel-boundary · WORKER

Start python3 tools/fw.py status; read AGENTS/framework/Worker/state/full tactical policy. Fetch-confirm Brain's literal pushed planning commit and recorded main ec3bceca1d70a4da240a490601602e97c2466de2. Read this plan and parallel-alpha-entry.md with git show at that plan commit, even if absent main. Create worker/15-duel-boundary in .worktrees/worker-15-duel-boundary from recorded main. No planning/main merge or other Worker review blocks starting.

Own only tools/tactical_combat.py, new tests/test_duel_boundary.py, new docs/duel-boundary.md and your summary/evidence. Harden assess and its public JSON CLI; preserve assess/known_weapon signatures and complete supported results. No calculator/event/sequence/collector/launcher/common/data/rebuild/framework/shared-doc edits. Do not import sequence/collector/launcher modules into this lower-level gate. Batch16 independently owns a launcher against the existing CLI contract.

First reproduce both-side baseline failures from synthetic complete duels: alive '?' or string 'false', forge {}, and status_effects ['unknown'] currently yield numeric outcomes. Establish the accepted input schema from existing documented contracts and valid callers. Reject unknown supplied mechanical fields at root/unit/stats/context/weapon levels without stripping effects. Nonmechanical note and unit/weapon id/name may remain only with explicit compatible types. Distinguish lookup catalog metadata from caller-supplied effect fields; catalog ID resolution must still work. All eight stats, HP, durability, rank, range, terrain/bonuses and optional alive/context/state need honest types/bounds; no bool-to-number, float rounding, truthiness or missing-as-none. Alive false remains refused. Supplied forge markers, including empty/null/unknown nested data, cannot masquerade as no forge; actual complete custom/forged weapon numbers remain supported. Missing rank or effects stay unknown, not defaulted.

Keep raw/effective, explicit support, Counter/drain/proc/paired and durability refusals. UNKNOWN must expose diagnostic plus null outcome/refusal flags, without numeric forecast, partial distributions or survival reassurance. Supported status/probabilities/worst HP/full output remain exactly unchanged. Parse public JSON without duplicate keys or non-JSON constants; malformed/unreadable files get controlled error, valid semantic UNKNOWN remains exit0. Protect named/aliased current_run.json before open and refuse run-shaped inputs. No run initialization/mutation.

Show independent supported/unsupported controls, direct API and CLI malformed matrices, exact full-output equality to baseline for supported catalog/custom/forged/unarmed/skill-context cases, collector and sequence compatibility, immutable inputs and protected private/canonical/research sets. Full make audit, fw check, focused tests and branch diff at committed code; render reference and resolve links. Preserve failures and actual commands/output/exits. Commit capped four-part docs/batches/15-duel-boundary.md and evidence; push literal delivery, never merge or spawn reviewers. Shared questions go to Brain.
```

## Verifier prompt — send only after delivery

```text
Fire Emblem Awakening Assistant · BATCH 15-duel-boundary · VERIFIER
Start status and project/Verifier/tactical rules. Fetch-confirm literal delivery/baseline/plan supplied by Brain; use fresh detached checkout. Before production/new tests/Worker conclusions, derive private valid/invalid observations and supported numerical controls from baseline contracts/calculator. Production-first review, then independently challenge direct API/CLI both-side and nested types/unknown effects/alive/forge/extra keys, duplicate JSON, all UNKNOWN numerical leakage and run paths. Compare full supported outputs, collector/sequence compatibility and immutable inputs/protected files. Run audit/fw/diff and render/link checks. Report classified findings at exact commit in capped docs/batches/15-duel-boundary-review.md only. Guard report-only push; no implementation or merge.
```

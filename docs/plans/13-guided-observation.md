# 13-guided-observation — Checked plan

The owner selected guided prompts before a browser form. Goal: create or revise
a plain existing duel payload without hand-writing nested JSON. Use current
main `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba`; no new mechanics.

## Worker prompt — send with batch 14

```text
Fire Emblem Awakening Assistant · BATCH 13-guided-observation · WORKER

Start fw.py status; read AGENTS/framework/Worker/state/full tactical policy. Fetch and record origin/main and full origin/brain/observed-entry-2026-10-12 plan commit. Read this plan and parallel-observed-entry.md using git show at that commit, even if absent from main. Start worker/13-guided-observation in its own linked checkout from recorded main; do not wait for planning merge.

Own only new tools/observed_input.py, tests/test_observed_input.py, docs/guided-observation.md and your batch summary/evidence. Add a standard-library guided terminal collector/editor for the existing tactical_combat.assess payload. Prompts go to stderr; default stdout is plain duel JSON, compatible with existing tools and batch14. Give a concise assessment/diagnostic on stderr by delegating to assess; UNKNOWN must not print partial forecast numbers. No formula changes or safe labels.

Group the eight named stats and bonus fields for convenient entry. Blank or ? means unknown/null, never zero/none/max HP. Explicit none confirms empty skills/weaknesses/bonuses/support only. Parse integers without rounding booleans/floats. Preserve real unsupported effects. Weapon catalog resolution requires explicit confirmation of exact unforged values; custom/forged values remain actual entered observations. Unknown names must not be guessed. Ask raw/effective basis and overall observation confirmation explicitly; no bonus conversion, roster defaults or inferred completeness. Incomplete known data must never earn observed_inputs_complete true.

Optional --edit selects a prior plain duel draft, never a run. Loaded values need deliberate keep/re-entry and renewed confirmations; blank does not accept stale values. Preserve unknowns and unsupported supplied fields or refuse incompatible shapes rather than drop effects. Cancellation/EOF must not create a complete assessment or overwrite an existing file.

Optional --output may CREATE a new .json only inside this checkout's ignored state/observations subtree; default writes no files. Reject existing destinations, traversal/symlink escapes and current_run.json. No tracker imports, live state reads/updates, canonical/generated/shared-engine/usage/README/framework edits. Batch14 owns a separate assembler using the existing payload schema; report shared-contract needs to Brain.

Show deterministic synthetic input transcripts, complete existing-gate equality, partial/unsupported/forge/edit/cancel cases, explicit file preservation, and measurable JSON-edit reduction. Run full audit/fw/focused/branch diff checks at committed code, render reference and resolve links. Privately snapshot canonical/research/private file sets before/after; publish no private values/hashes. Commit capped four-part docs/batches/13-guided-observation.md with real commands/output/exits/failures; push exact tip. Never merge or spawn reviewers.
```

## Verifier prompt — only after delivery

```text
Fire Emblem Awakening Assistant · BATCH 13-guided-observation · VERIFIER
Start status and project/Verifier/tactical rules. Brain supplies literal delivery and baseline/plan; fetch-confirm, use detached checkout. Before production/new tests/Worker conclusions, privately specify a complete and an incomplete observed duel and truthful confirmation/edit/cancel expectations. Inspect production first. Independently drive public guided transcripts, compare assess results and JSON values, challenge unknown/default/coercion/effect/stale-confirmation/path/overwrite behavior, and prove immutable source/private data. Audit/fw/diff, rendered docs/links and useful input burden evidence are required. Write only the capped exact-commit review with classified findings/real evidence; no implementation/merge. Guard report-only push and report to Brain.
```

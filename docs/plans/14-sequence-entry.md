# 14-sequence-entry — Checked plan

Goal: assemble the existing strict observed sequence payload from explicitly
selected plain duel observations without copying repeated player JSON. Work is
independent of the collector implementation; existing duel files are its input.
Baseline main: `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba`.

## Worker prompt — send with batch 13

```text
Fire Emblem Awakening Assistant · BATCH 14-sequence-entry · WORKER

Start fw.py status; read AGENTS/framework/Worker/state/full tactical policy. Fetch/record full origin/main and origin/brain/observed-entry-2026-10-12 plan commits; read this plan and parallel-observed-entry.md with git show even if absent from main. Start worker/14-sequence-entry in its own linked checkout from recorded main. Do not wait for batch13 or planning merge.

Own only new tools/sequence_input.py, tests/test_sequence_input.py, docs/sequence-entry.md and batch summary/evidence. Add an offline standard-library guided/explicit assembler reading selected existing duel JSON files. Each file's attacker becomes the next distinct enemy, its defender the shared player, and its context remains per entry. Explicit player/enemy entity IDs and argument/prompt order are required. Never infer identities from stats or rename the same entity to obtain numbers. No imports from the new collector; use only existing assess/known_weapon/evaluate contracts where needed.

Require compatible Hard/Classic/effective rulesets and matching player observations across files. Reject incompatible/mismatched data with entry/field diagnostics rather than choose one snapshot. Recognize only the documented existing duel keys (the existing example's note is nonmechanical); unknown supplied observation/effect keys must not disappear. Preserve unknown and unsupported unit/context/effect values as refusals; never fill missing values from another file. Confirm supplied order, unchanged observations and no intervening events separately; valid source files alone do not confer sequence completeness. Incomplete inputs or absent confirmation cannot yield numerical reassurance. Delegate assessment unchanged to tactical_enemy_phase.evaluate.

Prompts/concise status go to stderr; default stdout is the plain existing sequence JSON. Optional --output CREATE-only .json inside this checkout's ignored state/observations subtree, never current_run.json, overwrite or traversal/symlink escape. Default writes no files. EOF/cancel does not write a complete artifact. No run import/init/update, canonical/rebuild/shared engines, collector files, usage/README/framework edits.

Use selected synthetic duel files to demonstrate complete sequence equality, mismatched/stale player data, duplicates, unknown/unsupported tails, missing confirmation, context conflicts, read-only sources, output protection and CLI cancellation. Measure eliminated nested/repeated JSON editing. Privately snapshot canonical/research/private sets/content. Run full audit/fw/focused/branch diff checks at committed code; preserve actual output/exits/failures and render reference/links. Commit capped four-part docs/batches/14-sequence-entry.md, push exact tip, never merge or spawn reviewers. Shared questions go to Brain.
```

## Verifier prompt — only after delivery

```text
Fire Emblem Awakening Assistant · BATCH 14-sequence-entry · VERIFIER
Start status and all project/Verifier/tactical rules. Brain supplies exact delivery/baseline/plan; fetch-confirm and detach. Before production/tests/Worker conclusions, privately derive two observed duels' expected sequence and incomplete/conflicting cases from existing schemas. Inspect production first. Independently drive CLI/guided assembly; compare evaluate outputs, unknown/effect/confirmation retention, entity identity, mismatches, cancellation, source immutability, and output path/no-overwrite safety. Run audit/fw/diff and rendered docs/link checks; verify actual input effort claims. Write only capped exact-commit report with real commands/output and findings; no fixes/merge. Guard report-only push and send verdict to Brain.
```

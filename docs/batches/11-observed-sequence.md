# 11-observed-sequence — Worker delivery

## Done

Added a strict read-only Hard/Classic observed-sequence wrapper, synthetic
example, reference and 11 focused tests. Every supplied attacker is checked;
unknown tails and unsupported reachable HP branches invalidate all numbers.
Distinct IDs, effective observations, confirmed absent support and fixed
turn/outdoors context are required. Supported HP distributions reuse `assess`;
weapon validation reuses its existing `known_weapon(unit, side)` helper.
Player death absorbs later attacks, HP-dependent skills are reassessed, and
aggregate maximum scheduled retaliation uses prevent possible breakage.
Zero modeled player death remains conditional with false survival flags.

Starting main: `e78fa7bcc245071556a408f725105ac63ce7a8e9`.
Approved plan: `ea5eb003d232f1e45a1c31e5ac2bb7412949b56e`.
Reviewed code: `8da558e27212cf808d8d9eb04b38c5ed5c780420`.

## Checked

| Command/evidence at code commit | Result | Exit |
|---|---|---:|
| `make audit` — [output](attachments/11-observed-sequence/audit.log) | Three audits pass; 142 tests OK; inherited uncertainty retained | 0 |
| `python3 tools/fw.py check` — [checks](attachments/11-observed-sequence/checks.log) | 0 errors, 0 warnings | 0 |
| Focused discovery in checks log | 11 tests OK | 0 |
| Baseline-to-HEAD `git diff --check` in checks log | No output | 0 |
| [Direct/CLI controls](attachments/11-observed-sequence/controls.log), [replay](attachments/11-observed-sequence/controls.py) | Composition, death absorption, early kills, cumulative uses, unknown tails/context and dynamic Sol refusal; JSON inputs preserved | 0 |
| Invalid JSON public CLI in controls log | Diagnostic, no result; input preserved | 2 |
| [Preservation](attachments/11-observed-sequence/preservation.log) | 29 worktree canonical/private files and 1 primary private file unchanged; no canonical/research/run/coverage diff | 0 |
| [Rendered reference/link inspection](attachments/11-observed-sequence/visual-qa.log) | Five links resolve; readable full-page render without overflow | 0 |

## Not checked

No new gameplay/source verification, real play session, whole-map safety,
AI/path/order prediction, repeated attacker, between-duel changes, rebuild or
coverage increase. Conservative durability can refuse feasible early-kill cases.
Combined integration with batch 10, blind Verifier and Brain re-derivation
remain required before owner-approved merge. The stable duel/helper contracts
must remain compatible; other Worker files were not edited.

## Failed or blocked

No implementation test failures. Baseline reference missing HP/durability still
returned zero death and minimum HP 10; the new wrapper refuses both omissions.
Two Chrome policy-load failures and Safari local-file sandbox refusal prevented
UI inspection; successful standalone artifact rendering resolved that check.
Initial checks are retained separately. No merge or PR created.

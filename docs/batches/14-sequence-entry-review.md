# 14-sequence-entry — independent Verifier review

## Commit and ordering

Reviewed literal delivery `459b2095f6769c6203097ad0f12b6f968e08f237`, fetched and
confirmed on `origin/worker/14-sequence-entry`; fresh detached checkout.
Baseline `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba`; pinned plan
`7f4553587263772d9539e571c04abb18207704bf`, shared clarification
`b90a1eaf8e7aaf2ec3796d24b4c730a7ea83024d`.

Before production, new tests or Worker conclusions, read baseline
`tactical_enemy_phase.py`, `tactical_combat.py` and existing examples. Privately
recorded expected two-duel assembly and conflicting/incomplete cases at
2026-10-12 08:35:31 UTC; expected JSON SHA-256
`71733723df8314010af7ffdae09c112fc26a46501079c054d2d29da2fc540b43`.
Then inspected production, tests/reference, independently exercised controls,
and finally read Worker conclusions.

## Evidence at reviewed delivery

| Real command | Relevant output | Exit |
|---|---|---:|
| `python3 tools/fw.py status` (primary, before detach) | Batch 14 delivered; project checks pass | 0 |
| `python3 /tmp/fea-verifier-14/verify.py` | `TOTAL 58`; all independent controls PASS | 0 |
| `python3 /tmp/fea-verifier-14/extra.py` | `ADDITIONAL CHECKS 6 PASSED` | 0 |
| `python3 -m unittest discover -s tests -p test_sequence_input.py -v` | `Ran 12 tests`; `OK` | 0 |
| `make audit` | Three audits passed; `Ran 178 tests in 6.479s`; `OK` | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `git diff --check 5c596d42adb3d2a5eeee460032ee20bdd4bb78ba HEAD` | Empty output | 0 |
| Private SHA-256/set comparison before/after controls/audit | 324 canonical/research/private/pointer files unchanged across primary/review checkouts; no protected/shared-engine/coverage branch diff | 0 |
| `node /tmp/fea-verifier-14/render.cjs docs/sequence-entry.md docs/batches/14-sequence-entry.md` | Local links resolve; no overflow; full-page PNGs inspected, readable without clipping | 0 |
| `gh run list --branch worker/14-sequence-entry --limit 5 --json headSha,status,conclusion,url` | Exact delivery: completed/success, [CI run](https://github.com/cntrl-alt-lenny/fire-emblem-awakening-assistant/actions/runs/38224293441) | 0 |

Complete CLI/guided assembly exactly equals the independently derived payload
and unchanged evaluator result: final HP 10/20/30, expected HP 16.972,
minimum 10, death probability 0; both survival guarantees remain false.
Nine guided answers require zero JSON edits/retyped observations.

Controls cover independent confirmations, missing/null observations, stale
player snapshots, rules/support/context conflicts, distinct identity and file
aliases, duplicate keys, unsupported effects and a tail after certain death,
exact forged and unarmed inputs, conditional context without inheritance,
read-only sources, EOF/cancel, live-run symlink/hardlink protection, create-only
nested output, overwrite/traversal/symlink refusal. No unknown became supported
through dropped values or copied defaults.

## Findings and verdict

No BLOCKER, SHOULD FIX or UNPROVEN CLAIM found. Goals met within the supplied
sequence contract. **PASS at the reviewed delivery**; no implementation or merge.

Not checked: human usability, actual gameplay/source accuracy, native Windows,
whole-map safety, AI/order/path prediction, collector integration or new
canonical coverage. Brain re-derivation and owner approval remain gates.

Failed attempts: two baseline lookups used nonexistent example/reference
filenames (exit 128); corrected with baseline tree inventory before derivation.
No failed behavioral checks or fixes.

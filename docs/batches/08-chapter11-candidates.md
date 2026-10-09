# 08-chapter11-candidates — Worker

## Done

| Metadata | Full commit |
|---|---|
| Plan read with `git show` | `b67b91203c02bc7353f497bdfb5473bbbee40ed9` |
| Starting `origin/main` | `d3b646975a5f0686a798aaf12c0e541ed396da08` |
| Checked implementation | `3211c2ff3e39ab86cb903c6ddfff1fde8651c60a` |

Branched from main; no Brain refresh merge. Chapter 11’s fort family now stays
visible from the interpreted turn-3 start without asserting recurrence or a
last turn. Timing is PARTIAL; location support and unknown unit/geometry fields
remain intact. The separate northwest turn-4 report stays fixed. Authoring,
rebuild, audit, regressions and documentation reflect this distinction.
The event-family counter includes this unresolved family; no verified gameplay
coverage or complete schedule was added.

## Checked

Baseline regression failed with six failures; corrected Hard tests passed.
At the implementation commit, both `make rebuild` runs, `make audit`,
`python3 tools/fw.py check`, and `git diff --check` exited 0. All 28 canonical
JSON hashes matched across rebuilds. Only the fort record’s timing changed
against the canonical baseline. Other modes, unrelated Hard records, northwest
record, quarantine, and both checkouts’ private regular-file sets/content
were preserved. Player/enemy boundaries, Chapters 7/16 fixed turns and
Chapter 19/Paralogues 10/14 unknown/event controls were exercised.

Continuation at the existing delivery reproduced the six baseline failures,
two identical rebuilds, passing checks and preservation results without code changes.
Commands, actual outputs, hashes and reproducible preservation logic are in
[check evidence](attachments/08-chapter11-candidates/checks.md).
The [bounded source assessment](../../research/hard_verification/chapter11-candidates.md)
records route, access date, locators, Hard scope and remaining gaps. Changed
Markdown was rendered and visually inspected; local links resolved.

## Not checked

No gameplay, game script, save operation or new run. No independent confirmation
of recurrence, last turn, precise fort geometry, region/version equivalence or
complete map safety. The guide and its scope page are one evidence family.
Tests certify query behavior, not source truth. Blind Verifier and Brain review
remain required before owner-approved merge.

## Failed or blocked

The original start prerequisite caused a wait; Brain’s correction removed it.
The baseline failures are expected evidence. A bounded authoring harness first
failed because `__file__` was missing; its corrected comparison passed.
Python Markdown and Playwright’s default browser were unavailable; Node rendering with installed Chrome succeeded. No blocker remains.

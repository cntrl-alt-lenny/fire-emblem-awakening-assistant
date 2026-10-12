# 16-play-entry — Worker

## Done

Added one-action `tools/play.py`, dedicated public CLI replay tests and
[reference](../play-entry.md). Baseline:
`ec3bceca1d70a4da240a490601602e97c2466de2`; literal pushed plan:
`b9fffaeeea149470e7892106d9e6c6060f104c17`.
Started independently in the requested Worker worktree. Delegation shares stdin,
preserves stdout/warnings/exits and retains helper confirmations and create-only
saving. Assessment selection blocks run aliases before opening and run-shaped
JSON before calculation. No formulas, shared tools, trackers or canonical records
changed. Navigation replaces tool/flag selection; existing observation questions
and zero-manual-JSON workflows remain intact.

## Checked

At code commit `2649577` (full hash in logs):
`make audit` exits 0, 200 tests pass; `python3 tools/fw.py check` exits 0,
zero errors/warnings. Focused replay exits 0, seven test groups compare actual
existing-tool stdout, stderr suffixes and exits across 21 workflows, including
map/spoilers/refusal, complete/partial/Counter/paired, edits with renewed
confirmation, sequence, assessment, EOF/cancellation and protected output.
Synthetic terminal stdin, isolated create-only saves/overwrite/symlink refusal,
wrong-kind/run-shaped inputs and named/symlink/hardlink run aliases also pass.
Private canonical/research/state file sets and bytes match baseline/before checks.
Branch ownership/diff checks pass. Reference and summary local links resolve;
rendered HTML inspected without clipping or horizontal overflow.

Evidence: [audit](attachments/16-play-entry/audit.log),
[framework](attachments/16-play-entry/framework.log),
[workflow transcripts/results](attachments/16-play-entry/focused.log),
[preservation/diff](attachments/16-play-entry/preservation.log),
[render](attachments/16-play-entry/render.log).

## Not checked

Human UAT, actual gameplay, native Windows, complete maps/schedules and source
truth remain unverified. Baseline duel-gate gaps are not certified repaired:
Brain's combined batch 15 acceptance remains required. No new tactical coverage.
No reviewer spawned and no merge performed.

## Failed or blocked

Initial tests wrongly expected collector cancellation exit 2 (actual 1) and
reused a catalog-weapon edit transcript without its fresh exact-match answer.
Corrected the tests, preserving helper behavior. A second test expectation
mistakenly changed protected-output refusal to 1 (actual 2); corrected it.
Both [initial](attachments/16-play-entry/initial-focused.log) and
[second](attachments/16-play-entry/second-focused.log) failures are retained.
No remaining blocker.

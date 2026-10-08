# 08-chapter11-candidates

Path: Checked (legacy Tier 2). Worker implements; fresh blind Verifier reviews;
Brain re-derives and requests owner merge approval. This is a prepared task,
not a Worker summary or a claim of completed gameplay verification.

## Problem and outcomes

`hard_chapter_11_t3_forts` notes arrivals from turn 3 with subsequent waves
unknown, but encodes only fixed turn 3. At the refresh baseline, player-phase
queries for turns 4/5 omit this family. Generic incomplete-schedule warnings
remain, but the known family/location disappears. Establish whether the source
and representation justify this filtering; correct the mismatch conservatively.
Do not assert a wave on every later turn or invent an end turn.

Require a regression failing on the baseline; explicit player/enemy phase
boundaries; persistence of the unresolved family where appropriate; preservation
of Chapter 11's separately fixed northwest report and ordinary fixed-turn
filtering on Chapters 7/16. Unknowns, quarantine, other difficulties, private
state and zero certified complete schedules must survive. A supported start is
not a complete schedule. Any confidence change needs claim-level evidence.

Scope: Chapter 11 fort timing representation and its authoring/rebuild path;
only necessary query/audit/regression changes; affected generated documentation,
coverage counters and source metadata. No broad timing redesign, other-map
research, game/save operations, Windows work or framework edits.

Read the tactical policy, `tools/map_info.py`, `tools/hard_data.py`,
`research/hard_verification/author_review.py`, `reviewed.json`, canonical Hard
records and `tests/test_hard.py`. Re-read only the bounded Chapter 11 paragraph
in [the registered guide](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/beginning-to-chapter/chapter-11-mad-king-gangrel)
and its separate Hard-scope declaration. Record route/date/locator and gaps;
do not count same-publisher pages as independent evidence or bypass restrictions.

## Worker message

```text
Fire Emblem Awakening Assistant · BATCH 08-chapter11-candidates · WORKER

First run python3 tools/fw.py status (py -3 or python if needed). Read AGENTS.md, docs/agents/FRAMEWORK.md, docs/agents/roles/worker.md, docs/state.md and the full tactical policy. Fetch origin. Start only when origin/main contains docs/plans/08-chapter11-candidates.md; otherwise report waiting for Brain's refresh merge. Work from origin/main on worker/08-chapter11-candidates, preferably in .worktrees/worker-08-chapter11-candidates.

Execute docs/plans/08-chapter11-candidates.md on the Checked path. Establish whether Chapter 11's from-turn-3 fort family is incorrectly filtered out later, and correct the evidence-to-query mismatch without inventing recurrence or a final turn. Stay within that plan's scope and acceptance criteria. Preserve unknowns, other-mode data, quarantine and all private run files. No gameplay operation or new run is authorized.

Privately snapshot canonical JSON and CURRENT_RUN.md plus every regular state file before work. Demonstrate a meaningful regression failing at the baseline and passing after the change. At the committed implementation run make rebuild, make audit, python3 tools/fw.py check and git diff --check. Compare all canonical JSON hashes across two rebuilds; prove other-mode data, unrelated Hard records and private file sets/content preserved. Exercise Chapter 11 player/enemy phase boundaries plus fixed-turn and unknown-event controls. Record real commands, relevant output and exits at the full commit. Render changed Markdown, inspect it and resolve local links. Keep source wording, interpretation and observed gameplay separate; no new gameplay coverage from tests.

Commit docs/batches/08-chapter11-candidates.md with Done, Checked, Not checked, Failed or blocked, at most 500 prose words; output tables may be longer. Record failed attempts. Push implementation and summary; state the exact full commit in your final reply. Do not merge. Technical questions go to Brain.
```

## Verifier message

Send only after Worker finishes, in a fresh session. The verifier resolves the
literal delivery commit from the remote branch and freezes it before review.

```text
Fire Emblem Awakening Assistant · BATCH 08-chapter11-candidates · VERIFIER

First run python3 tools/fw.py status (py -3 or python if needed). Fetch origin, resolve origin/worker/08-chapter11-candidates to one literal full commit and pin your review to it. Read AGENTS.md, framework, verifier card, standing decisions, tactical policy and docs/plans/08-chapter11-candidates.md.

Before reading the Worker's summary or changed assessment, independently inspect the origin/main baseline, bounded registered Chapter 11 source/scope, and original query outputs. Record that blind pass privately. Then inspect the real diff and summary. Establish whether the change keeps an unresolved fort family visible without asserting unsupported repeated spawns; verify player/enemy phase boundaries and separate fixed-turn reports. Check every acceptance criterion and source claim independently.

Privately snapshot canonical JSON and CURRENT_RUN.md plus every regular state file before checks. Reproduce the baseline regression failure. At the pinned delivery run make rebuild, make audit, python3 tools/fw.py check and git diff --check; compare hashes across two rebuilds and prove other-mode data, unrelated Hard records and private file sets/content preserved. Run the plan's query controls. Render changed Markdown and inspect local links. Tests do not verify source truth or complete schedules. Classify findings as BLOCKER, SHOULD FIX, NOTE or UNPROVEN CLAIM, with file/line and a demonstrable failure or evidence gap.

Write only docs/batches/08-chapter11-candidates-review.md, at most 500 prose words, including the exact reviewed commit, actual commands/output/exits, findings, limits and verdict. Immediately before pushing, check the remote Worker branch still equals your pinned commit; if it moved, stop and report the mismatch to Brain. Commit the review on the Worker's branch in a separate checkout and push without force. Never implement fixes or merge. End with batch, VERIFIER, outcome and pushed full commit. Technical questions go to Brain.
```

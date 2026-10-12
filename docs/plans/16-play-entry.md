# 16-play-entry — Checked plan

Provide one offline guided starting command for the already delivered map,
observation and assessment tools. The launcher changes navigation, not formulas,
sources, schemas or run tracking. Starting main:
`ec3bceca1d70a4da240a490601602e97c2466de2`.

## Worker prompt — send together with batch 15

```text
Fire Emblem Awakening Assistant · BATCH 16-play-entry · WORKER

Start python3 tools/fw.py status; read AGENTS/framework/Worker/state/full tactical policy. Fetch-confirm Brain's literal pushed plan and recorded main ec3bceca1d70a4da240a490601602e97c2466de2. Read this plan and parallel-alpha-entry.md using git show at the plan commit even if absent main. Create worker/16-play-entry in .worktrees/worker-16-play-entry from recorded main. Start independently; no batch15 or planning-merge wait.

Own only new tools/play.py, tests/test_play_entry.py, docs/play-entry.md and your summary/evidence. Create a standard-library, offline guided one-action launcher: current-map briefing; new duel collection; deliberate draft editing; sequence assembly; assess a selected duel; assess a selected sequence; quit. Existing tools own all facts/calculations/input collection and file saving. Do not edit their modules or shared docs/data/framework/trackers. Do not add a browser, installer, dependency, new schema or formulas. No new batch15 module dependency; its public CLI stays tools/tactical_combat.py FILE.

One invocation selects one action and exits with its actual result. Selection/context prompts go to stderr; stdout preserves the chosen tool's normal text or plain JSON with no menu/envelope contamination. EOF/cancel/invalid selections must not trigger another action or create an artifact. Preserve child exit/error behavior; process exit0 or JSON output never means a supported/safe assessment. Forward semantic UNKNOWN and warnings intact. No automatic retry that drops unsupported fields or changes observations.

Map entry requires actual chapter/difficulty/turn/phase and disclosed spoiler choice/default; no silent phase advance, future-map expansion or guessed context. This first launcher uses manual map context, no run selection/import/init/update. Observation actions invoke existing guided helpers, with output only when explicitly requested under their create-only local rules. Editing never silently accepts previous confirmation or overwrites a draft. Assessment selection must distinguish duel/sequence explicitly, never infer from a run or fix input values. Block named/symlink/hardlink aliases of the standard current_run.json before assessment open; run-shaped JSON cannot produce numbers. Do not read a live run or ledger.

Support both a real terminal and assistant-supplied batched stdin across launcher/child prompts: no swallowed/read-ahead answers, shell interpolation or lost EOF/cancellation. Stable existing CLI/module entry points may be delegated; preserve source payloads, support/context/spoilers and numeric results. At least ten representative public CLI workflows must compare actual existing-tool outputs/exit codes, including map/spoiler refusal, complete/partial/unsupported, edit, sequence, cancellation and protected output. Measure eliminated command/flag choices and JSON edits; do not label scripted trials human UAT. Batch15 integration is a later release gate, not a development dependency.

Use temporary synthetic states/checkouts only. Privately compare canonical/research/run file sets/content. Full audit/fw/focused/branch diff checks at committed code, rendering/link inspection, actual output/exits and failed attempts. Commit capped four-part docs/batches/16-play-entry.md, push exact delivery, never merge or spawn reviewers. Brain owns shared integration and technical decisions.
```

## Verifier prompt — send only after delivery

```text
Fire Emblem Awakening Assistant · BATCH 16-play-entry · VERIFIER
Start status and all project/Verifier/tactical rules. Fetch-confirm literal delivery/baseline/plan supplied by Brain; detach fresh checkout. Before production/tests/Worker conclusions, define private representative workflow transcripts and expected existing-tool outputs/exits. Inspect production first. Independently execute actual menu-plus-child batched stdin, cancellation/EOF/invalid choice, map/spoiler/context, new/edit/sequence/assessment and create-only/path/run boundaries. Require no source mutation, lost stdin, confirmation reuse or invented interpretation of UNKNOWN. Compare actual delegated results and measured input effort. Audit/fw/diff/render/links and protected-file checks. Write only capped exact-commit review; guard report-only push. No fixes or merge; combined batch15 acceptance remains Brain's gate.
```

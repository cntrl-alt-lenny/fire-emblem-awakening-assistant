# 001-foundation-audit: Establish the tactical foundation and next bounded task

Tier: 2
Mode: audit
Supersedes: none

## Goal

Give Brain an independently reproduced account of the existing Hard/Classic
assistant's useful capabilities, material failure paths and evidence gaps,
then recommend one bounded next round. This is onboarding and investigation;
it does not certify the whole game or change gameplay behavior.

## Context

The owner has appointed GPT as Brain and the other agent as Worker. The
project has been moved, published publicly, and bootstrapped with framework
3.1.0. Read `AGENTS.md`, the framework and Worker card, the full tactical
policy, `docs/state.md`, `STATUS.md`, `CURRENT_RUN.md`, `research/audit.json`,
`research/phase2/final_audit.json` and the Hard manual audit. Then read only
the canonical records and tool code needed for the checks below.

The current Hard forensic layer takes precedence over historical readiness
claims and legacy Hard chapter slots. There is no initialized run and no
certified complete schedule. Native Windows is not currently supported:
the initial CI attempt hit default text encoding; tracking also imports
Unix-only `fcntl`. Linux/macOS CI is green after declaring the supported
platforms. Do not confuse framework portability with project portability.

## Scope and non-goals

Allowed changes: your report and supporting audit artifacts inside this
round's folder. You may rebuild offline to inspect reproducibility, but
restore only generated differences you created after documenting them;
leave a clean delivered diff outside this round. Do not change canonical
data, tools, tests, instructions, CI, repository settings or licensing.
Do not fix findings in this round, initialize a playthrough, or touch a
player's state. Do not expand the encyclopedia or browse the whole campaign.

## Invariants

- Source: full tactical policy. Missing/empty data is unknown; difficulty,
  phase, support, effects and quarantine must never be silently discarded.
- Source: `AGENTS.md`. Actual state is authoritative; tests/rebuilds must
  preserve it. Facts need source-level evidence beyond passing tests.
- Source: framework. Work on the Worker branch, report exact commit and real
  commands/output/exit codes on every exit; never accept or merge your work.
- Source: owner instruction and `docs/state.md`. GPT remains Brain. Findings
  inform the next brief; the Worker does not enlarge project scope.

## Acceptance criteria

1. Reproduce the audit and framework hygiene checks. Distinguish structural
   validation, numerical regression coverage and externally verified facts.
2. Establish whether a fresh offline rebuild is deterministic across two
   passes. Record before/after SHA-256 values or a compact machine-readable
   comparison for canonical JSON, `CURRENT_RUN.md` and any run files. Report
   any drift, including original canonical changes, rather than hiding it.
3. Exercise at least these concrete failure paths: Chapter 7 player-phase
   turn 5 versus enemy-phase turn 5 targeting; Chapter 15 quarantined
   reinforcement leakage; Chapter 5/17 unresolved conflicts; empty waves
   mistaken for absence; and missing support/unsupported combat effects.
   Use existing fixtures or temporary inputs, and cite the actual output or
   code/test location that establishes each result. A scenario not reproduced
   stays explicitly unverified.
4. Spot-check up to three load-bearing tactical/mechanics claims against
   accessible sources, including their difficulty and phase context. Treat
   copied/mirrored text as dependent evidence. Preserve disagreement and
   access limitations. No bypasses, bulk crawls or full-guide archives.
5. List concrete findings with severity, file/line, failure path and scope;
   separate proven defects from unresolved coverage. A clean audit is a
   valid outcome. Do not invent a blocker or call partial data certified.
6. Recommend exactly one bounded next round, with rationale, proposed tier,
   acceptance criteria and evidence needed. Default research candidates are
   the inherited Chapter 5/17 conflicts; a demonstrated tooling defect may
   take priority if it undermines safe use. Windows support is a separate
   product decision and must not be silently implemented here.
7. Push the framework-stamped Worker report and artifacts. No claim that
   the project is ready for unconditional Ironman safety or that a run began.

## Required evidence

Include the reviewed full commit, OS/Python version, command output and exit
status. Use equivalent Python subprocesses if make is unavailable.

```sh
python3 tools/fw.py check
make audit
make rebuild
make rebuild
python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase player
python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase enemy
python3 tools/map_info.py --chapter 15 --difficulty hard --turn 5 --phase player
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 5 --phase player
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 5 --phase player
make audit
git diff --check
```

Record the hash comparison command/script and actual results for criterion 2,
and all extra commands/inputs used for criterion 3. Source checks need URLs,
short compliant excerpts or factual summaries, and applicability/uncertainty.
If a check fails, report it; do not edit production files to turn it green.
Finish with `python3 tools/fw.py report --role worker --round
001-foundation-audit --push` after committing your audit artifacts.

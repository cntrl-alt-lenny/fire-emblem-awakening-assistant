<!-- fw-report
round: 003-chapter5-research
role: worker
branch: worker/003-chapter5-research
head: 74a6a3d1ea22f30c0f3e2115aa4ee5984e97fe77
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T16:48:02Z
-->
## Verified

Reviewed artifact commit: `74a6a3d1ea22f30c0f3e2115aa4ee5984e97fe77`.
The start command selected the supplied brief at
`91193ff3be91cdc3c1957f19c66022ea3b5204f8`; only seven round-local
attachments changed after that base. No production implementation or merge.

Environment read by the evidence runner using `platform.platform()` and
`sys.version`: `macOS-27.0-arm64-arm-64bit`; Python
`3.9.6 (default, Aug 25 2026, 21:26:21) [Clang 21.0.0 (clang-2100.3.34.2)]`.

At the reviewed full commit, ran
`python3 docs/rounds/003-chapter5-research/attachments/verify.py /tmp/fea-worker003-exact-checks`
→ exit 0. This invokes the following actual commands; relevant output follows.
The committed `attachments/checks.txt` contains the earlier full run at the
start commit, including full CLI JSON; the exact-commit rerun results below
supersede that run for review. The runner replaces the checkout prefix with
`<worktree>` in captured output; no protected files are written.

- `make audit` → exit 0. Actual excerpts from its three validators and tests:

```text
python3 tools/validate_data.py
  "passed": true,
  "errors": [],
  "verified_safe_reinforcement_schedules": 0,
python3 tools/audit_phase2.py
  "passed": true,
  "errors": [],
  "fully_verified_schedules": 0,
  "Hard_Classic_ready_without_unverified_tactical_data": false
python3 tools/audit_hard.py
  "passed": true,
  "errors": [],
  "campaign_maps": 44,
  "reinforcement_records": 29,
  "source_truth_not_proven_by_tests": true,
python3 -m unittest discover -s tests -v
Ran 115 tests in 0.599s
OK
```

Warnings retain incomplete tactical coverage and limited numeric/source
verification. These results verify repository consistency, not source truth.
Tests used their existing temporary-state fixtures; protected-state comparison
below found no change.

- `python3 tools/fw.py check` → exit 0:

```text
0 error(s), 0 warning(s)
```

- `python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase player`
  → exit 0, actual JSON excerpts:

```json
  "current_turn": 3,
  "current_phase": "player",
  "map_confidence": "CONFLICTED",
  "target_enemy_phase_turn": 3,
  "safe_to_conclude_no_reinforcements": false,
```

- `python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase enemy`
  → exit 0, actual JSON excerpts:

```json
  "current_turn": 3,
  "current_phase": "enemy",
  "map_confidence": "CONFLICTED",
  "target_enemy_phase_turn": 4,
  "safe_to_conclude_no_reinforcements": false,
```

- `python3 tools/map_info.py --chapter 5 --difficulty hard --turn 5 --phase player`
  → exit 0, actual JSON excerpts:

```json
  "current_turn": 5,
  "current_phase": "player",
  "map_confidence": "CONFLICTED",
  "target_enemy_phase_turn": 5,
  "safe_to_conclude_no_reinforcements": false,
```

All three retain `hard_chapter_5_disputed_schedule`, null event turns/phase/
units, and unknown schedule completeness. The enemy-phase query advances its
target to the next enemy phase; this is CLI behavior, not an observed arrival.

- `git diff --check` → exit 0, no output.
- Protected-file comparison in the same runner: SHA-256 plus exact file-set
  equality against `attachments/preservation-before.json`, after all checks
  → exit 0. Actual output:

```json
{
  "protected_files": 30,
  "canonical_json_files": 28,
  "added": [],
  "removed": [],
  "changed": [],
  "live_run_exists": false,
  "state_files": ["state/.gitkeep"]
}
```

This covers every `data/**/*.json`, `CURRENT_RUN.md` and every state file,
including other difficulty records. No live run was initialized. No rebuild
was run or authorized. Initial and final manifests are committed.

- `git diff --name-only 91193ff3be91 HEAD` → exit 0: only the seven
  `docs/rounds/003-chapter5-research/attachments/` files listed below.
- Markdown local-link resolution using Python `re.findall` and `Path.exists()`
  → exit 0: `3 local links resolved; exit 0`. Rendered both research Markdown
  artifacts using installed marked, then inspected screenshots/accessibility
  in the browser. Matrix, URL wrapping and observation plan were readable;
  inspection procedure is in `attachments/presentation-qa.md`.

## Not verified

The actual Hard Chapter 5 arrival turns, phases, unit groups, exact locations,
conditions, fort effectiveness, boss suppression and completeness remain
unverified. The claim matrix distinguishes retrieved source reports from game
facts. No canonical amendment or certified gameplay coverage is justified.

External research on 2026-10-03 used focused web searches and original page
contexts as logged in `attachments/search-log.md`; exact URLs and source
locators are in `attachments/research.md`. The Japanese Hard comment and
all-difficulties guide were readable. The western wiki table/prose were only
available through public indexed context after direct failure/robots denial;
its current direct page revision was not reproduced. No restricted source was
retried after a definite access denial or bypassed.

Two independently authored Chapter 5 Hard forum discussions were accessible,
but did not enumerate spawn phases. An unscoped reinforcement thread was
excluded because it did not establish this map. A Hard/Classic-labelled video
could not be observed because its player required sign-in/bot confirmation;
no frames/timestamps, setup, cuts or reset sequence were inspected. A further
playthrough summary returned 403. No game files, footage or whole guides were
acquired. Missing observations never establish absent arrivals.

Source boundaries are clearer, but the event conflict is unresolved. The
Japanese unlabelled table must not provide the Hard comment's phase; the
western combined-difficulty table and general guide do not independently
certify a Hard-only schedule. Region/version and phase-convention hypotheses
remain unproved. Verifier and Brain review have not occurred; no merge.

## Changed

All changes are beneath `docs/rounds/003-chapter5-research/`:

- `attachments/research.md`: source families/locators, claim matrix, honest
  unresolved outcome and exactly one bounded next observation task.
- `attachments/search-log.md`: focused retrieval attempts and access limits.
- `attachments/verify.py`: round-local standard-library evidence runner;
  preserves protected files and introduces no runtime/build dependency.
- `attachments/checks.txt`: complete initial audit/CLI output, base SHA and
  environment; exact artifact-commit rerun excerpts are above.
- `attachments/preservation-before.json` and `preservation-after.json`:
  matching protected-file manifests.
- `attachments/presentation-qa.md`: rendered-document/local-link inspection.
- `worker.md`: this report, to be framework-stamped and pushed.

Canonical data, registry, tools, tests, framework, CI, coverage counters,
`STATUS.md`, `docs/state.md` and player state were not changed. No new
verified gameplay coverage is claimed.

## Open questions

Which conflicting early-turn account, if either, describes the relevant Hard
setup? Are differences due to actual conditions, mixed difficulties, phase
conventions, transcription or version? No causal explanation was established.

Exactly one next task is recommended: a separate Tier 2 controlled-observation
round confined to Hard Chapter 5, with visible Hard/Classic setup, declared
region/version and continuous phase boundaries through turns 1–6 and player
turn 7. It should separate initial movement from arrivals and compare matched
fort/range conditions, recording any boss-defeat map-ending censoring. Full
protocol is in `attachments/research.md`. That bounded horizon does not prove
a last wave or whole-map safety, and this Worker did not start the next task.

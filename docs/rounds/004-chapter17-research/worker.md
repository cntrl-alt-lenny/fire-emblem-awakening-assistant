<!-- fw-report
round: 004-chapter17-research
role: worker
branch: worker/004-chapter17-research
head: 159f99496f352a42fb3f25cfa1039e7dfeb9f398
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T18:47:51Z
-->
## Verified

Reviewed artifact commit: `159f99496f352a42fb3f25cfa1039e7dfeb9f398`. Start/brief base: `867b6648cf633c66d547592100445f36080b3b2b`.
Only five round-local attachments changed after the start command selected the
supplied brief; no implementation, adoption or merge occurred.

Environment from `platform.platform()` / `sys.version` in the evidence runner:
`macOS-27.0-arm64-arm-64bit`; Python
`3.9.6 (default, Aug 25 2026, 21:26:21) [Clang 21.0.0 (clang-2100.3.34.2)]`.

At the full reviewed commit ran
`python3 docs/rounds/004-chapter17-research/attachments/verify.py /tmp/fea-worker004-exact-checks`
→ exit 0. The runner actually executes each command below. The committed
`attachments/checks.txt` is the full initial audit output and parsed CLI
excerpts at the start base; the exact-commit rerun results here supersede it
for review. Raw command outputs and protected hashes stay in private temporary
files. Audit output sanitizes the checkout prefix to `<worktree>`; CLI excerpts
are explicitly parsed selections, not newly authored game data.

- `make audit` → exit 0. Actual relevant validator output excerpts:

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
Ran 115 tests in 0.617s

OK
```

Existing warnings retain incomplete map coverage and limited numerical/source
verification. Passing tests show consistency, not truth of the arrival claims.
The existing tests use temporary-state fixtures; preservation below confirms
no protected file changed. No rebuild was authorized or run.

- `python3 tools/fw.py check` → exit 0:

```text
0 error(s), 0 warning(s)
```

- `python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase player`
  → exit 0. Parsed JSON excerpts:

```json
{
  "current_turn": 8,
  "current_phase": "player",
  "target_enemy_phase_turn": 8,
  "map_confidence": "CONFLICTED",
  "safe_to_conclude_no_reinforcements": false
}
```

- `python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase enemy`
  → exit 0. Parsed JSON excerpts:

```json
{
  "current_turn": 8,
  "current_phase": "enemy",
  "target_enemy_phase_turn": 9,
  "map_confidence": "CONFLICTED",
  "safe_to_conclude_no_reinforcements": false
}
```

- `python3 tools/map_info.py --chapter 17 --difficulty hard --turn 9 --phase player`
  → exit 0. Parsed JSON excerpts:

```json
{
  "current_turn": 9,
  "current_phase": "player",
  "target_enemy_phase_turn": 9,
  "map_confidence": "CONFLICTED",
  "safe_to_conclude_no_reinforcements": false
}
```

- `python3 tools/map_info.py --chapter 17 --difficulty hard --turn 10 --phase player`
  → exit 0. Parsed JSON excerpts:

```json
{
  "current_turn": 10,
  "current_phase": "player",
  "target_enemy_phase_turn": 10,
  "map_confidence": "CONFLICTED",
  "safe_to_conclude_no_reinforcements": false
}
```

All four outputs retain three conditional event candidates, including
`hard_chapter_17_first` with `CONFLICTED` confidence, null fixed turns and
`UNKNOWN` map-specific spawn phase/completeness. Reported turns remain metadata;
queries do not filter these conditional candidates into certified fixed waves.
The enemy-phase query targets the following numbered enemy phase. This is
present software behavior, not observed game timing or a safety forecast.

- `git diff --check` → exit 0, no output.
- Protected file-set/SHA-256 comparison, performed by the same runner after
  all commands against the private pre-work baseline → exit 0. Actual output:

```json
{
  "protected_file_count": 30,
  "canonical_json_count": 28,
  "state_file_count": 1,
  "added_count": 0,
  "removed_count": 0,
  "changed_hash_count": 0,
  "live_run_exists": false
}
```

Baseline creation used Python `hashlib.sha256(p.read_bytes()).hexdigest()` on
sorted `data/**/*.json`, `CURRENT_RUN.md` and every file recursively under
`state/` immediately after start/context inspection, before round writes.
Exact file-set equality and every hash matched after the checks. This includes
all difficulty datasets. Neither baseline nor player-state contents/hashes
were committed. No run was created or modified.

- `git diff --exit-code 867b6648cf63 HEAD -- data CURRENT_RUN.md state`
  → exit 0, no output, independently confirming tracked protected files.
- `git diff --name-only 867b6648cf63 HEAD` → exit 0, only
  `attachments/checks.txt`, `presentation-qa.md`, `research.md`,
  `search-log.md` and `verify.py` under this round.
- Local Markdown link check with Python `re.findall` / `Path.exists()`
  → exit 0: `3 local links resolved; exit 0`. Rendered both research documents
  with installed marked and inspected browser screenshots/accessibility text,
  including corrected wording, matrix rows, URL wrapping and observation plan.
  Procedure is in `attachments/presentation-qa.md`; layouts were readable.

## Not verified

Actual Hard Chapter 17 first staircase, event phase, warning turn/trigger,
warning-to-arrival interval, independently verified first-wave inventory,
activation geometry and suppression remain unresolved. No complete schedule,
route safety or new certified gameplay coverage is claimed. No canonical
amendment is justified or applied in this round.

Source-reading findings are recorded separately from tests in
`attachments/research.md`: exact URLs, dated locators, retrieval date
2026-10-03, difficulty/mode boundaries, translation versus inference and
source families. The guide and Japanese chapter contexts were readable.
The western wiki was available only through indexed context after direct
402/robots restriction; its current direct revision was not reproduced.
A truncated sentence was not repaired, and uncertain ordinal/directional
interpretations remain explicit. Duplicate guide registry IDs are one family.
Provenance and nearby inventory reproduction gaps are review questions,
not claims that either recorded inventory is false.

Bounded independent searches found chapter-scoped forum/firsthand accounts,
but their settings or phase inventories were insufficient. A separate
Hard/Casual commenter cannot supply another author's difficulty. One
misnumbered indexed complaint is corrected in its own thread; direct context
was unavailable. Two direct forum opens returned reader errors. The normally
opened Hard/Classic-labelled video displayed a sign-in/bot gate: no frames,
setup, timestamps, cuts or reset chronology were observed. The second video
candidate was not opened. No restricted source was bypassed, no footage or
whole guide archived, no game files acquired and no new playthrough controlled.

Region/version equivalence, causal triggers and explanations for the reports
were not established. Source silence and access failure never establish
absence or agreement. General ordinary Hard action rules do not observe this
map-specific event. Verifier and Brain review have not occurred; Worker never
accepts or merges this work.

## Changed

Only `docs/rounds/004-chapter17-research/`:

- `attachments/research.md`: bounded evidence catalog, per-claim matrix,
  unresolved outcome, provenance questions and one discriminating next task.
- `attachments/search-log.md`: exact focused searches, candidate scopes,
  exclusions, access failures and stopping boundary.
- `attachments/verify.py`: round-local standard-library evidence runner;
  private protected-hash comparison and public count/excerpt output.
- `attachments/checks.txt`: initial audit output, parsed CLI uncertainty
  excerpts and preservation counts; exact-commit results are above.
- `attachments/presentation-qa.md`: rendered research and local-link evidence.
- `worker.md`: this report for framework stamping and push.

No canonical JSON, source registry, production tools/tests, rebuild code,
coverage counters, standing decisions, framework, CI, licensing or player
state changed. `STATUS.md` and `docs/state.md` remain unchanged.

## Open questions

Do the differently worded accounts describe the same wave at all? What is the
visible warning phase, first appearance/conversion/action order, oriented
staircase identity and trigger? Can the exact inventory provenance be reproduced
without borrowing attributes across source/difficulty boundaries?

Exactly one bounded next task: a separate Tier 2 Hard Chapter 17 observation
round, contingent on normally accessible or owner-provided continuous footage
with visible setup and declared region/version. Input is currently unavailable.
The protocol in `attachments/research.md` covers turns 1 through player turn
11, warning-relative phase boundaries, mapped stairs, occupancy and boss
censoring, first/second/central ordering and initial movement versus spawning.
Matched progression comparisons are conditional on matched recordings existing;
a single run yields correlation/observed sequence, not a causal trigger or
universal fixed turn. No next task, campaign expansion or adoption was started.

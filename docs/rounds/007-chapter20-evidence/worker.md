<!-- fw-report
round: 007-chapter20-evidence
role: worker
branch: worker/007-chapter20-evidence
head: 7747d2ee79044eaa6f18a2673c26325e3b8e344a
os: macOS 27.0.1
python: 3.9.6
written: 2026-10-05T09:42:22Z
-->
## Verified

Evidence commit: `7747d2ee79044eaa6f18a2673c26325e3b8e344a`.
Checks below ran after committing both research artifacts and before stamping
this report. The report commit adds only this file.

- Start — `python3 tools/fw.py start --role worker --round 007-chapter20-evidence` → exit 0; `seat ok: worker, round 007-chapter20-evidence, branch worker/007-chapter20-evidence at 1675abf9f657`.
- Environment — `python3` querying `platform.platform()` and `sys.version` → exit 0; `macOS-27.0.1-arm64-arm-64bit`, Python `3.9.6`, Clang `21.0.0 (clang-2100.3.34.2)`.

| Command at evidence commit | Relevant actual output | Exit |
|---|---|---:|
| `make audit` | Data validation, phase-two audit and Hard audit each `passed: true`; Hard `campaign_maps: 44`, `reinforcement_records: 29`, `registered_sources: 217`, `source_refs_resolve: true`, `source_truth_not_proven_by_tests: true`; `Ran 118 tests in 9.147s`, `OK`. Verified safe schedules remain 0. | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard` | Hard/Classic, map `CONFLICTED`; objective `Defeat Walhart`, confidence `CONFLICTED`, catalog/guide conflict with resolution null; `schedule_complete: false`, `safe_to_claim_move_safe: false`. | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase player` | `target_enemy_phase_turn: 6`; same objective conflict and incomplete schedule retained. | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase enemy` | `target_enemy_phase_turn: 7`; same objective conflict and incomplete schedule retained. | 0 |
| `git diff --check` | Empty output. | 0 |

Source checks on 2026-10-05: bounded direct reader contexts recovered the
catalog Chapter 20 objective field, Gamer Guides Chapter 20 Condition and its
separate Hard-default declaration, and Vandal's Victoria field. Indexed MK
retrieval recovered Chapter 20 metadata and its completion footnote. The
introductory overlap with Gamer Guides is a dependency lead; independent
derivation remains unknown. One indexed exact-thread lookup did not recover
the specific player topic; it remains explicitly inherited/unreproduced.
Exact URLs, durable locators, route, source family and scope limitations are
in the corrected evidence attachment. No denied direct URL was retried.
Repository checks do not verify source truth.

Preservation commands: `python3` sorted path/SHA-256 snapshot before work,
then recomputation after checks; `git ls-tree -r --name-only <ref> data` and
`git show <ref>:<path>` for each canonical JSON file, comparing with the starting
commit `1675abf9f657cec6c5c70be9479d9a5b05c0404e` and `origin/main` → exit 0.
Actual output: `Data before/after equal: True count: 28`; `Private before/after
equal: True count: 2 live run present: False`; canonical file sets/content match
both starting commit and origin/main, count 28. Whole-file equality includes
all other-mode records. Private comparison includes CURRENT_RUN.md plus every
regular state file; contents and digests remain outside public artifacts.
No rebuild was run. This proves preservation in this worktree only.

Reproducible snapshot/comparison method (executed in private temporary storage):

```python
from pathlib import Path
import hashlib, subprocess
root = Path.cwd()
def snapshot(paths):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths) if p.is_file()}
data = snapshot(root.glob('data/**/*.json'))
private = snapshot([root / 'CURRENT_RUN.md'] + list((root / 'state').rglob('*')))
# Save privately before work; recompute after work/checks and compare dictionaries.
# Print counts, equality and live-run presence only.
for ref in (starting_commit, 'origin/main'):
    paths = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', ref, 'data'], text=True).splitlines()
    previous = {p: hashlib.sha256(subprocess.check_output(
        ['git', 'show', ref + ':' + p])).hexdigest()
        for p in paths if p.endswith('.json')}
    assert data == previous
```

Historical-artifact comparison — `git diff <starting-commit> --` round 006
brief, worker.md, verifier.md and attachments/brain-review.md → exit 0,
empty output; `Historical artifacts unchanged: True`. After checks,
`git status --short` → exit 0, empty output before writing this report.

Presentation — bundled Node `node /tmp/fea007-render.cjs`, marked, Playwright
and installed Chrome → exit 0. Actual output: `evidence { headings: 6,
tables: 2, overflow: false }`; `correction { headings: 1, tables: 1,
overflow: false }`. Both complete rendered screenshots visually inspected:
readable text/tables, no clipping or overlap. Rendered content equals the
committed artifact bytes; render files remain outside Git. Python Markdown
local-link scan of both artifacts → exit 0, `Local links: 2 all resolve`.

## Not verified

No visible Hard/Classic objective or continuous surviving-boss completion
sequence was inspected. Region/game version, source lineage and source
accuracy remain unknown. The forum account was not freshly recovered; no
exact quotation from it is claimed. New preservation/rendering evidence
cannot recreate round 006's missing private CURRENT_RUN baseline or historical
render record. No main-checkout private run inspection was performed.

This Worker read the historical reports and Brain review as required by the
brief; it did not perform a blind Verifier pass. Fresh Verifier and Brain
exact-commit review remain outstanding. Model family is GPT-6 per session
instructions; specific variant, reasoning effort and speed are not inspectable.
No owner-reported configuration was supplied.

## Changed

- Round 006 attachments/objective-evidence.md — dated superseding correction;
  fresh versus inherited retrieval accounting; unknown source independence;
  neutral treatment of recovered MK sentence; separated attribution, editorial
  assertion, reported observation and visible gameplay; corrected settings and
  continuous completion observation prerequisites.
- Round 007 attachments/correction-record.md — maps material historical findings
  to dispositions and retains unavailable historical evidence gaps.
- Round 007 worker.md — this report. No other project files changed.

No canonical data, source registry, tools, tests, coverage, STATUS.md, standing
decisions, framework, CI, settings or license changes. Zero new verified
gameplay coverage; no canonical amendment proposed or applied. No merge.

## Open questions

Independent source derivation and actual Hard/Classic completion remain
unresolved. Exactly one next observation task: review an owner-supplied
continuous Chapter 20 capture showing a display that actually exposes Hard
and Classic tied to the same save, the displayed objective, both Cervantes
and Excellus alive through Walhart's defeat, and immediate completion.
Record region/version when available; cuts, resets or hidden boss state prevent
the required inference. Suitable capture is unavailable; no game/save operation
is authorized by this correction round.

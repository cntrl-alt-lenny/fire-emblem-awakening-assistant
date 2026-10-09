# 09-combat-context — Worker summary

## Done

The strict live gate now requires actual boolean `outdoors` for either side's
Indoor/Outdoor Fighter and a positive nonboolean integer `turn` for Lucky Seven,
Even Rhythm or Odd Rhythm. Missing/null/malformed context returns `UNKNOWN`,
null outcome and a side/field diagnostic. Optional omissions remain accepted
without the relevant skill. Equipped skills and all existing refusals remain.

Ownership: gate, new focused tests/reference and batch evidence only; no
canonical, rebuild, map, shared-test, general-calculator or framework edits.

| Anchor | Full commit |
|---|---|
| Plan | `4c18202f428c736a10643865e7ba2ef7c9244515` |
| Starting main | `d3b646975a5f0686a798aaf12c0e541ed396da08` |
| Audited implementation | `cf1e62d7742a8729eaabc0e0b1da72e794931cc5` |

## Checked

Actual output and exits are in [attachments](attachments/09-combat-context/).
Baseline gate plus new regressions failed 139 subcases (exit 1); delivery passes
all nine focused tests, including both sides, malformed shapes, boundaries/parity,
CLI, input immutability and paired/unsupported-effect controls. All 34 complete
supported assessments equal the baseline gate's outputs exactly.

| Command at audited implementation | Result | Exit |
|---|---|---|
| `make audit` | Validation/audits pass; 127 tests OK | 0 |
| `python3 tools/fw.py check` | 0 errors, 0 warnings | 0 |
| `git diff --check` | No output | 0 |
| `python3 -m unittest discover -s tests -p test_combat_context.py -v` | 9 tests OK | 0 |
| `python3 docs/batches/attachments/09-combat-context/check_controls.py d3b646975a5f0686a798aaf12c0e541ed396da08` | 34 complete numerical results preserved | 0 |

Canonical JSON and private file sets/content were privately hashed before/after;
all preserved. No run initialized or used as test input. New reference rendered,
visually inspected and local links resolved. No rebuild required by scope.

## Not checked

Independent Verifier and Brain acceptance remain pending. Tests establish the
input contract/numerical preservation, not new gameplay truth, complete combat
mechanics or map safety. No gameplay coverage counters changed.

## Failed or blocked

Expected baseline regression failures retained in the evidence log. Main's
framework 4.0.0 status warns about 4.0.1 and mislabels legacy reports `EADME`;
Brain owns those existing housekeeping issues. Neither blocks this batch.
The first headless renderer created a valid reference screenshot but timed out
during browser shutdown (30 seconds); retained output was inspected, and a
bounded screenshot-and-cleanup path rendered the summary. No implementation
failure or cross-scope dependency found. Branch-wide `git diff --check` at the
first report commit found trailing whitespace emitted in the baseline transcript
(exit 2). The shell still pushed that commit; transcript whitespace was trimmed
and checks rerun before Verifier handoff.

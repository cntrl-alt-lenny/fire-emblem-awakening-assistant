# 10-input-shapes — Worker summary

## Done

The live gate now requires both combatants' skills/weaknesses to be lists of
string IDs/categories and current HP to be an actual integer within the existing
observed maximum. Missing/null/malformed inputs, unknown membership and HP
boundaries return UNKNOWN/null with side/field diagnostics. No coercion or
removal of effects; supported API/results, context checks and unequipped-defender
behavior remain.

Only the assigned gate, new tests/reference and batch evidence changed.

| Anchor | Full commit |
|---|---|
| Fetched origin/main and starting checkout | `e78fa7bcc245071556a408f725105ac63ce7a8e9` |
| Fetched origin/brain/roadmap-2026-10-09 plan | `ea5eb003d232f1e45a1c31e5ac2bb7412949b56e` |
| Audited implementation | `d45e0d49fb8460d0afa1678d9ddb65fc9ef512a4` |

## Checked

[Evidence](attachments/10-input-shapes/) retains commands, actual output and
exits. Synthetic direct and public CLI probes reproduce 14 baseline numeric
leaks on both sides; delivery refuses every case without mutation. All 288
complete supported assessments and 17 full CLI controls equal baseline exactly.
Tests cover missing/null/collection/element types, unsupported IDs, HP boundaries,
context, Counter/drain/paired/proc refusals and unequipped defenders.

| Command at audited implementation | Result | Exit |
|---|---|---:|
| `make audit` | Three audits pass; 140 tests OK | 0 |
| `python3 tools/fw.py check` | 0 errors, 0 warnings | 0 |
| `python3 -m unittest discover -s tests -p 'test_combat*.py' -v` | 31 tests OK | 0 |
| `python3 docs/batches/attachments/10-input-shapes/check_controls.py` | Baseline leaks reproduced; full results preserved | 0 |
| `git diff e78fa7bcc245071556a408f725105ac63ce7a8e9 --check` | No output | 0 |

Canonical/private file sets/content were privately compared before/after in
primary and Worker checkouts: identical. No run initialized or used as input.
New reference and summary rendered, visually inspected and local links resolved.

## Not checked

Fresh blind Verifier, Brain review, combined batches and owner merge approval
remain pending. These checks validate the input contract, not gameplay truth or
complete mechanics/map survival. No canonical edits, rebuild or coverage added.

## Failed or blocked

Baseline tests intentionally failed 228 subcases (exit 1). Initial full audit
and framework check failed because tracebacks exposed machine-specific paths;
paths were redacted, the unpushed implementation commit replaced, and checks
passed. Failed output is retained. First reference screenshot succeeded, but
Chrome shutdown exceeded 20 seconds; inspected PNG and bounded cleanup completed
visual checks. No remaining implementation blocker or shared-contract change.

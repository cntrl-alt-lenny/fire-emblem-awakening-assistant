<!-- fw-report
round: 002-combat-gate
role: worker
branch: worker/002-combat-gate
head: 1e5bad74b7fb200da14197bd45cc503e11067d6c
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T16:08:03Z
-->
## Verified

Reviewed implementation commit: `1e5bad74b7fb200da14197bd45cc503e11067d6c`.
Baseline: `0af85f83df6e` (full baseline is recorded in `attachments/evidence.py`).
Environment from Python `platform`: `Darwin 27.0.0`, Python `3.9.6`.
The following required checks were rerun at the exact implementation commit:

```text
$ make audit
Ran 115 tests in 0.562s
OK
exit_status: 0

$ python3 tools/fw.py check
0 error(s), 0 warning(s)
exit_status: 0

$ python3 -m unittest discover -s tests -v
Ran 115 tests in 0.571s
OK
exit_status: 0

$ python3 -m unittest discover -s tests -p test_combat_gate.py -v
Ran 13 tests in 0.222s
OK
exit_status: 0

$ git diff --check
(no output)
exit_status: 0

$ git status --short
(no output before this report)
exit_status: 0
```

Full earlier command outputs from the same implementation are committed in
`attachments/audit.txt`, `tests.txt`, `framework.txt`, `focused.txt` and
`diff-check.txt`. All three audit validators report passed true, errors empty.
These are structural and regression checks, not new external source proof.

`python3 docs/rounds/002-combat-gate/attachments/evidence.py` → exit 0:

```text
OS/Python: Darwin 27.0.0 3.9.6
Baseline: 8 expected assertion failures, 0 errors (test exit 1)
Numerical comparison: 10 complete fixtures, identical forecasts/outcomes
CLI: 7 temporary inputs, all exit 0
Preservation: 30 files; added/deleted/changed: []/[]/[]; live run: False
```

At the exact reviewed commit, this evidence was rerun through `python3 -`
using `runpy.run_path` to load the committed script, redirecting only its
artifact output directory to a temporary folder:

```python
ns = runpy.run_path('docs/rounds/002-combat-gate/attachments/evidence.py')
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp)
    shutil.copyfile('docs/rounds/002-combat-gate/attachments/preservation-before.json',
                    out / 'preservation-before.json')
    ns['main'].__globals__['OUT'] = out
    ns['main']()
```

Actual output was the same five lines above, followed by
`Temporary-output evidence rerun: exit_status 0`; repository status stayed
clean. The normal evidence script command reproduces the same checks.

- Baseline regression demonstration loads the old wrapper directly from
  `git show BASE:tools/tactical_combat.py` while using complete new fixtures.
  Six omission assertions (effect/Brave/effectiveness, each side) fail because
  old output is NO_MODELED_DEATH_IN_THIS_DUEL instead of UNKNOWN. Two certainty
  assertions fail because old output is POTENTIALLY_LETHAL instead of LETHAL.
  `attachments/baseline-failures.txt` contains actual assertion output:
  `FAILED (failures=8)`; intended test exit 1, no execution errors. Traceback
  repository roots were removed to avoid publishing personal paths.
- `attachments/numerical-comparison.json`: complete ordinary, certain
  attacker/defender, possible-risk, effective, unequipped, forged, canonical,
  canonical Brave and supported-proc inputs have identical old/new forecasts
  and full outcome numbers. This includes fixtures whose old defaults are
  now explicitly supplied. Only wrapper classification/metadata changes.
- `attachments/cli.json`: seven actual `python3 tools/tactical_combat.py
  TEMP_INPUT.json` executions with temporary inputs and exit 0 each. Canonical,
  forged and unequipped cases calculate; certain attacker/defender cases are
  LETHAL with the correct side named; possible risk is POTENTIALLY_LETHAL;
  missing defender effect is UNKNOWN, outcome null, diagnostic names
  `defender:weapon.effect`. The test suite also exercises the public CLI.
- Focused tests cover both combatants, missing/null/malformed fields, explicit
  known absence, incomplete canonical lookup, unknown IDs, custom/forged
  values, contradictory Brave text/boolean, explicit unequipped handling,
  both risk roles, zero risk and a probability below one that must not round
  to certainty. Continued refusals cover missing/null support, adjacent/paired
  outcomes, drain (canonical/custom), Counter, Dragonskin, Aether, unresolved
  proc combinations and durability breakage.
- `attachments/preservation.json`: standard-library SHA-256 and sorted file-set
  comparison of all 28 canonical JSON files, CURRENT_RUN.md and every existing
  state file. Added/deleted/changed are all empty. Only state/.gitkeep exists;
  there is no live run, so this is not a live-play preservation test. Tests
  and CLI inputs used temporary/in-memory state.
- Rendered changed Markdown with bundled marked/Playwright and installed Chrome
  (exit 0), then visually inspected four committed `render-*.png` screenshots.
  Usage contract, formula scope, status update and count row are readable.
  Standard-library link resolution → `Local Markdown links resolved: 11`,
  exit 0; `attachments/link-check.json` lists targets. Rendering's initial
  default-browser attempt failed because the bundled browser was absent;
  installed Chrome succeeded without adding project dependencies.

## Not verified

No new external mechanics facts, canonical truth, game execution, complete
map schedules, enemy geometry or whole-map survival were verified. No Linux,
Windows or current remote CI run was checked in this seat. No rebuild was
required: canonical data and rebuild scripts are unchanged. No live run was
present or initialized. Independent blind Verifier review and Brain acceptance
remain outstanding; no merge was performed.

The general calculator's permissive legacy defaults remain by design;
live safety advice must use the strict wrapper. Canonical lookup does not
prove class eligibility or actual observed equipment/durability. Supported
effect text retains existing calculator meanings; active stat bonuses still
belong in effective stats once. Unsupported mechanics remain unsupported.

## Changed

- `tools/tactical_combat.py`: resolves canonical IDs and validates live weapon
  properties before calling the unchanged calculator. Rejects unknown material
  fields and Brave contradictions with side/property diagnostics. Uses a copy
  so normalization cannot mutate caller inputs. Explicit unequipped defender
  requires null weapon plus weapon_state unequipped; null alone is unknown.
  Exposes LETHAL, affected sides and unrounded probabilities while retaining
  worst HP, existing forecast/outcome and map-safety refusal. Exact equality
  to one classifies certainty; no tolerance rounds a lower probability up.
- `tests/test_combat_gate.py`: 13 focused regression methods with per-side
  matrices and real CLI calls. `tests/test_hard.py`: supplies explicit empty
  effectiveness and consistent Brave text in the inherited complete fixtures.
- `examples/battle.json`: existing example now also satisfies the strict
  Hard/Classic observed-input contract; remains illustrative rather than a run.
- `docs/usage.md`, `docs/combat-formulas.md`: explain explicit absence,
  canonical/custom distinction, unequipped defender, contradictions, attack
  roles, certainty labels and unchanged conditional numerical scope.
- `STATUS.md`: current 115-test count and bounded capability repair; historical
  forensic evidence and gameplay/map coverage remain explicitly separate.
- Round attachments: reproduction script, real logs, old/new comparisons,
  temporary CLI inputs/results, preservation snapshots and rendered docs.
- `docs/state.md`: unchanged; no sentences added or removed. No canonical
  data, proc engine, general calculator, map tools, trackers, CI, framework,
  repository settings or licensing changed.

## Open questions

None blocking this brief. The new certainty fields identify attack roles,
not player allegiance; callers must map the observed player's role before
interpreting LETHAL. Missing weapon fields now intentionally refuse old
incomplete live inputs; docs/examples provide explicit replacements.

Inherited Chapter 5/17 research conflicts remain pending. This input repair
earns no new verified gameplay coverage and does not certify a safe route.

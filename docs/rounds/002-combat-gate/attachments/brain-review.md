# Brain review — round 002

Decision: accept at delivered commit
`9a54577880d8f86a751b3e6facb2393467082fbb`, pending owner approval to merge.
Worker evidence describes `1e5bad74b7fb200da14197bd45cc503e11067d6c`;
Verifier reviewed `bce8e4241a43db0fa64ef24aa06f57eb4ed90414`.
The final delivery adds only the Verifier report. Brain checked both reports,
the actual implementation/tests/documentation diff, independent failure
reproductions and CI at the final delivered commit. No blocker identified.

## Commands and relevant results

Commands ran at the exact final delivery on Darwin 27.0 / Python 3.9.6,
2026-10-03. All commands below exited 0; expected baseline assertions were
captured inside a successful independent Python probe.

```text
python3 tools/fw.py delivery --round 002-combat-gate
origin/verifier/002-combat-gate (9a54577880d8): delivered
verifier: report describes bce8e4241a43
worker: report describes 1e5bad74b7fb

make audit
All three validators: passed true, errors []
Ran 115 tests in 0.943s
OK

python3 tools/fw.py check
0 error(s), 0 warning(s)

git diff --check
(no output)

python3 -m unittest discover -s tests -p test_combat_gate.py -v
Ran 13 tests in 0.236s
OK

python3 tools/tactical_combat.py examples/battle.json
status: POTENTIALLY_LETHAL
at_risk_sides: [defender]
attacker_death_probability: 0
defender_death_probability: 0.0591
safe_to_claim_map_survival: false

gh run view 37136068162 --json conclusion,headSha,url
headSha: 9a54577880d8f86a751b3e6facb2393467082fbb
conclusion: success

gh run view 37136068162 --json jobs --jq '.jobs[] | {name,conclusion}'
Audit (ubuntu-latest, Python 3.9): success
Audit (ubuntu-latest, Python 3.13): success
Audit (macos-latest, Python 3.13): success
```

## Independent re-derivation

Brain's `python3 -` probe loaded the old wrapper using
`git show 0af85f8:tools/tactical_combat.py` into a temporary module, without
editing production files. It imported the current complete `battle()` fixture
and compared old/new results. For each combatant independently, deleting each
of `effect`, `brave` and `effectiveness` gave old status
`NO_MODELED_DEATH_IN_THIS_DUEL`, new status `UNKNOWN`, null outcome and the
correct side/property diagnostic. Both certain-death fixtures produced
`LETHAL`, probability 1.0, minimum HP 0 and the correct certain side. A
possible-death fixture produced `POTENTIALLY_LETHAL`, probability 0.009565.

Nine independent complete fixtures (ordinary, both certainty cases, actual
example, each-side canonical ID, each-side forged values and explicit
unequipped defender) had identical old/new forecast and outcome values.
Caller inputs remained unchanged; every supported map-survival flag was false.

Brain also ran the new omission/certainty assertions against the old wrapper:
eight expected assertion failures and zero execution errors. The new focused
suite passes those assertions. This independently establishes that the tests
detect the intended failures rather than merely mirroring successful code.

Relevant actual probe output:

```text
certain attacker LETHAL 1.0 ['attacker']
certain defender LETHAL 1.0 ['defender']
possible POTENTIALLY_LETHAL 0.009565
complete_fixtures_equal 9
baseline_expected_failures 8 errors 0
protected_files_identical_to_baseline 30 live_run_exists False
local_links 11 missing []
working_tree [empty]
```

Protection check used SHA-256 of all `data/**/*.json`, `CURRENT_RUN.md` and
all state files. The sorted file set and hashes matched the Worker's before
snapshot; every current file also matched its baseline git blob. No live run
exists. Diff review independently establishes that data, rebuild code,
general calculator, proc engine, map tools, trackers, framework and standing
decisions are untouched. No rebuild was required.

Brain resolved all 11 local links in the three changed Markdown documents
and visually inspected the four committed renders for usage, formulas, status
and counters. The new contract/labels are readable; the source preserves the
historical audit separately from the current count.

## Findings judged and remaining limits

All seven acceptance criteria and the Verifier's supporting claims were
checked against code, focused tests, independent probes, protected-file
comparisons, document renders and actual CI. Missing/malformed/unsupported
weapons refuse; canonical/custom/forged and explicit unequipped paths are
covered; the exact-one test does not round near-one risk into certainty.
Unsupported support/effect/proc/durability cases remain refused in the suite.
No change to numerical mechanics or new game-source assertion is delivered.

The general calculator intentionally retains its legacy defaults; tactical
advice must use the strict wrapper. Attack roles do not identify player
allegiance. Numerical comparisons cover the stated fixtures, not every battle.
No gameplay execution, full mechanics/source certification, complete map
schedule, enemy geometry, live-state experiment or map-survival guarantee.
Gameplay coverage counters do not increase because of these regressions.

## Next direction

Recommend a bounded Tier 2 research round on the Hard Chapter 5 conflicting
reinforcement reports: establish whether accessible, difficulty-specific
evidence can resolve arrival turns, unit groups, spawn phase and conditions.
An unresolved outcome with precise evidence gaps is valid; do not invent
certainty from source agreement or passing tests. Chapter 17 follows, then
other reinforcement/event gaps. Complex combat expansion remains separate.
This recommendation is not a new brief or an executed research task.

## Merge card

Changed: strict weapon completeness, certain-death labels with affected sides,
focused regressions and input documentation/examples.
Verified: 115 tests, hygiene, Linux/macOS CI, baseline failures, unchanged
supported fixture numbers and all 30 protected data/state files.
Not verified: complete mechanics/source truth, live play or full map safety.
Risk: old incomplete live inputs now refuse and need explicit observations;
unsupported combat and incomplete map coverage remain explicit limitations.

No merge performed. The owner-approves rule still applies to both the earlier
audit and this implementation delivery.

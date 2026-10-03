<!-- fw-report
round: 002-combat-gate
role: verifier
branch: verifier/002-combat-gate
head: bce8e4241a43db0fa64ef24aa06f57eb4ed90414
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T16:13:33Z
-->
Reviewed commit: `bce8e4241a43db0fa64ef24aa06f57eb4ed90414`.
Environment: `macOS-27.0-arm64-arm-64bit`, Python `3.9.6`.

## Findings

None blocking or requiring correction found in this round's implementation.
I completed the independent code/documentation diff, required checks, baseline
failure demonstration, numerical comparisons and CLI probes before opening
`docs/rounds/002-combat-gate/worker.md`. Then I compared that report and reran
its evidence with output redirected to a temporary directory.

### Acceptance criteria

1. Met. `tools/tactical_combat.py:10`–35 validates each side's resolved weapon,
   including explicit nonempty supported effect text, exact boolean Brave and
   category-list effectiveness. Omission/null/malformed matrices refuse with
   side/property diagnostics; explicit absence remains supported. Null defender
   weapon requires explicit unequipped state; missing knowledge and unequipped
   attacker refuse. The gate copies rather than changes caller inputs.
2. Met. Canonical/custom/forged paths tested. Unknown IDs, incomplete lookup,
   ambiguous forge markers, unsupported custom/canonical drain and contradictory
   Brave text/boolean refuse. The documented separate effectiveness field is
   retained; `–` does not silently clear it. General calculator unchanged.
3. Met. `tools/tactical_combat.py:62`–65 uses exact equality to one, names
   certain/at-risk sides and exposes both probabilities and minima. Either-side
   certainty, possible risk, no modeled risk and a value immediately below one
   covered. Attack roles explicitly do not imply player allegiance. Map-safety
   flag remains false for all supported outputs examined.
4. Met for the bounded evidence. Thirteen independent complete fixtures had
   byte-equivalent Python forecast/outcome values before/after. Rerun of the
   Worker's ten-fixture comparison also passes, including canonical Brave and
   supported Ignis. No formula/proc code change; compatibility intentionally
   tightened only at the live boundary.
5. Met. All 13 focused methods pass, including per-side subtests and continued
   support/effect/proc/durability refusals. Key six omission and two certainty
   assertions fail against pre-fix code for the intended status differences,
   with no execution errors. Public CLI exercised independently and by tests.
6. Met. Example passes public CLI; documentation matches the enforced contract.
   Local Markdown link targets resolve. Independently inspected all four
   committed rendered images: changed usage/formula/status/count sections are
   readable and correspond to the source additions. No new mechanics facts
   or expanded tactical coverage claimed.
7. Met. Full audit, suite, focused suite, framework check and whitespace check
   pass at the reviewed commit. File-set and SHA-256 preservation confirmed
   across checks for 28 canonical JSON files, run pointer and state placeholder.
   No live run exists. Protected paths also have empty baseline/delivery diffs.

### Commands and actual results

All verification ran in the designated linked worktree at the exact reviewed
commit. No production or test files were edited by this Verifier.

```text
git diff --stat origin/main HEAD
exit 0; includes inherited round 001, brief/history and round 002 changes.
git diff origin/main HEAD -- tools/tactical_combat.py tests/test_combat_gate.py tests/test_hard.py docs/usage.md docs/combat-formulas.md STATUS.md examples/battle.json
exit 0; inspected full implementation/documentation/test diff.
git diff --name-only origin/brain/002-combat-gate HEAD
exit 0; only scoped wrapper/tests/example/docs/status and round evidence/report.
make audit
exit 0; Ran 115 tests in 0.635s; OK
python3 tools/fw.py check
exit 0; 0 error(s), 0 warning(s)
python3 -m unittest discover -s tests -v
exit 0; Ran 115 tests in 0.596s; OK
python3 -m unittest discover -s tests -p test_combat_gate.py -v
exit 0; Ran 13 tests in 0.225s; OK
git diff --check
exit 0; no output
```

Independent `python3 -` baseline/fixture/CLI probe exited 0. Baseline module
was reconstructed without checking out or changing production files:

```python
import subprocess, types, sys, unittest, io, copy
sys.path[:0] = ['tools', 'tests']
import tactical_combat, test_combat_gate
from test_hard import battle
old = types.ModuleType('baseline_gate')
exec(subprocess.check_output(
    ['git', 'show', 'origin/main:tools/tactical_combat.py'], text=True), old.__dict__)
suite = unittest.TestSuite(test_combat_gate.CombatGateTests(n) for n in
    ['test_missing_properties_both_sides', 'test_certain_death_both_sides'])
saved = test_combat_gate.assess
try:
    test_combat_gate.assess = old.assess
    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
finally:
    test_combat_gate.assess = saved
```

Actual baseline result: `Ran 2 tests`, `FAILED (failures=8)`, zero errors.
Six omission cases: `NO_MODELED_DEATH_IN_THIS_DUEL != UNKNOWN`.
Both certainty cases: `POTENTIALLY_LETHAL != LETHAL`.
The enclosing probe treats these as expected failures; its exit is 0.
The focused delivery command above passes the same assertions.

For old/new comparisons I called `old.assess(copy.deepcopy(p))` and
`tactical_combat.assess(copy.deepcopy(p))`, asserting identical `forecast`
and `outcome`. Inputs were `battle()`, the actual JSON example, explicit
unequipped defender, and each side independently with forged numbers,
certain death, possible death, effectiveness, and canonical ID. Actual:
`13` comparisons passed. Forged numbers: might `8`, hit `110`, crit `3`;
canonical ID `iron_sword`, rank `D`; effectiveness `['flying']` against
other side weakness `['flying']`. Certainty used `test_combat_gate.lethal(side)`;
possible risk set that side HP `20` and other side weapon crit `1`.

CLI probe used `tempfile.TemporaryDirectory`, `json.dumps(p)` and
`subprocess.run(['python3','tools/tactical_combat.py',str(path)],
capture_output=True,text=True)`. Actual outputs, each exit 0:

```text
input                    status                         attacker p   defender p   certain sides
examples/battle.json     POTENTIALLY_LETHAL             0            0.0591       []
explicit unequipped      NO_MODELED_DEATH_IN_THIS_DUEL  0            0            []
certain attacker         LETHAL                         1.0          0            [attacker]
certain defender         LETHAL                         0            1.0          [defender]
possible attacker        POTENTIALLY_LETHAL             0.009565     0            []
missing defender effect  UNKNOWN                        outcome null
```

All supported CLI results had `safe_to_claim_map_survival: false`.
Omission reason: `defender:weapon.effect missing, unknown or unsupported;
use explicit – for no special effect`. Outcome null and refusal flag false.

After reading the Worker report, reproduced its full evidence in temporary
output storage with this `python3 -` command (exit 0):

```python
import runpy, tempfile, shutil
from pathlib import Path
ns = runpy.run_path('docs/rounds/002-combat-gate/attachments/evidence.py')
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp)
    shutil.copyfile('docs/rounds/002-combat-gate/attachments/preservation-before.json',
                    out / 'preservation-before.json')
    ns['main'].__globals__['OUT'] = out
    ns['main']()
```

```text
OS/Python: Darwin 27.0.0 3.9.6
Baseline: 8 expected assertion failures, 0 errors (test exit 1)
Numerical comparison: 10 complete fixtures, identical forecasts/outcomes
CLI: 7 temporary inputs, all exit 0
Preservation: 30 files; added/deleted/changed: []/[]/[]; live run: False
Worker snapshot matches independent snapshot: True
```

The Worker's claims agree with the independent results. No unproven numerical
or command claim found. No canonical or external factual change needed source
research; imported legacy fact accuracy remains outside this review.

### Preservation and document evidence

Independent before/after snapshot (`python3 -`, exit 0) used:

```python
import pathlib, hashlib
root = pathlib.Path('.')
paths = sorted(root.glob('data/**/*.json')) + [root/'CURRENT_RUN.md']
paths += sorted(p for p in (root/'state').rglob('*') if p.is_file())
snapshot = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
```

Snapshots retained temporarily outside the repository and compared both key
sets and hashes: `file sets identical True`, `hashes identical True`, `files 30`,
`live run exists False`. `git diff --name-only REF HEAD -- data CURRENT_RUN.md
state docs/state.md tools/combat_calculator.py` returned no output, exit 0,
for each of `origin/main` and `origin/brain/002-combat-gate`. This also confirms
unchanged other-mode canonical records and unchanged standing decisions.

Before and after SHA-256 values are identical for every entry below:

```text
CURRENT_RUN.md 03f89cdc45587a056abd04f8dda732da99872bacb13fb951e632aa814b62b0b7
data/chapters/chapters.json 301678441555a989c2ada13e699fa8cbf365cf3f9d30f5465076229f0beecec0
data/chapters/coverage.json 1e5686b0f9d7d5a85b0594a1398eb7e0e106b83dc0680a5a76e956579ac77968
data/chapters/hard_quarantine.json ff5a462725798c2de9a67a1dd0718801a550419bcc0a917239ac246115b66c0d
data/chapters/hard_reinforcements.json cbe0edaa388f310e9fe32d7f16296e88a857788f8c40e63211f89d02299fd7b8
data/chapters/hard_tactics.json b258d40f39a9623a3870f7ce5c83ad05c0b02eb47e16b6621cac755574e0b83a
data/chapters/reinforcement_candidates.json 0e7d1d4894738006fcdec262d1b0657f99b8b450c27af1d6b166e486e6a9c936
data/chapters/reinforcements.json bf46d31ea7ad831b52383c33667d4974e6dcad85641626d74eb6b9b6154a82c1
data/characters/avatar.json 3b588a14fb35c77d42b2547171998b20a816edbbbf12a422873fac94224ddeac
data/characters/characters.json 4f54400942c687b496e40af06a3a7e7cc20f2a34c77cd14044ae957eae9bb82b
data/classes/classes.json f07f10b348b1835a4c1a4ec84fb978646bc6b2aaaf86d913bce48b4e9fd0482d
data/difficulty/modes.json 1c6a0baa882721b3bfde4b269aff7037012d076182c0db01c26d54c8dfe60172
data/enemies/enemies.json f2d0e7719310e7c49da13157bdf6379143d6c30616a080564c3c6a8bb1f2a62a
data/items/economy.json 03e18dad1cd970cde9a717e6617dbf1aee4a33e3a903be279acd4cd0c759cc9e
data/items/items.json 1b94b2cecd0de4a2d26fd6c1de79d0e757c776570476f73e0494f72f26c5d596
data/items/merchant_rare_pool.json f1a902dafcd3eaa4e116279f2200f3f8b951b9f1d87ac0ced32615dad93f4f4c
data/items/merchants.json 8530a6d6bfe4fb9c34801081a4a596db0f289862f4c546bcac6c7d14f78d4110
data/items/renown.json 8072580f2791cfe3a0f4eb6ab7d507192d92da91945e3476d05466d731142ee7
data/items/shops.json d599bc212b256f8e8119f8193e721c9e7865cba0f799dd3fbb5d4d28e69ef022
data/mechanics/availability_and_barracks.json 0e550caeaa78d1e75604e75c2c51239e8b250f4af04d4b76420fcb01f69458cd
data/mechanics/formulas.json cf0e9f4e27649d7ab75ece623ad492755149686a21887db8821d11c6aaa6e52a
data/mechanics/progression.json 2568cb81a61cb30536d5f40dc5eec5939105226711d90d5be202e1819410b191
data/mechanics/world_and_boosts.json 99c3530d9cf6afed1b4e6223bd44d0b44ba00a8ae2de999484a9ce39ff02d1a2
data/skills/skills.json 6d2c5e58a50f72347ff742067a26c377ef0dd8def9522a662eafb30ca4707369
data/sources.json 047738b771fc103269f386facd58e518b9eab1fcca26a84e75781bf2ad46b7c1
data/supports/compatibility.json 3ec4ca0113c107b9748acc89e89d922e5f64a9edbe19f96af6321e76e3e92086
data/supports/rules.json 3fbe849617c84f1f7ec97b0504ce2fdbfd8823c4773c29edf3f2a1c4049cb642
data/supports/support_growth.json c7a76da8ef3aa892e6603014cf07151ca9f6922571b349c68aaed1ab1eb3cf5f
data/weapons/weapons.json f49806a31eb8b93115135f98e52eb0012266b45ddf8d6b9a935db1950d85024c
state/.gitkeep e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Local links in `docs/usage.md`, `docs/combat-formulas.md`, `STATUS.md` parsed
with Markdown target regex, remote/fragment targets excluded, and resolved
against the source parent. Actual missing targets: `[]` for all three (exit 0).
Viewed `attachments/render-usage.png`, `render-formulas.png`, `render-status.png`
and `render-counts.png` with the image viewer after the blind pass. This inspects
provided rendered sections; it does not prove full-document layout across clients.

## Not verified

No external game-mechanics certification, canonical source-truth audit, game
execution, full map schedules/geometry or whole-map survival. No Linux/Windows
or current remote CI verification in this seat. No live player run exists;
preservation concerns current files and temporary tests, not a live-play
experiment. No rebuild needed or run: rebuild code and data are unchanged.
Numerical equivalence covers stated fixtures, not every conceivable battle.
The general calculator retains permissive legacy defaults; the stricter live
wrapper is required for this contract. Canonical lookup cannot prove class
eligibility, actual equipment or observed bonuses. Chapter 5/17 conflicts and
other inherited coverage limits remain unresolved. No merge or acceptance
performed by this seat.

## Verdict

At the reviewed commit, the scoped live weapon-completeness and death-certainty
repair satisfies the brief with strong local regression and preservation
evidence. The independently failing baseline assertions demonstrate that the
new tests detect the intended defects. Supported calculations retain their
numbers, unsupported cases remain refused, and no full-map guarantee is added.
No blocking finding identified. This report informs Brain's exact-commit
review and re-derivation; it is not merge approval or gameplay certification.

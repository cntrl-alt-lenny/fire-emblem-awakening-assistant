# 09-combat-context

Path: Checked. Independent of Chapter 11, with a fresh blind Verifier before
Brain review and owner-approved merge. No planning-document merge prerequisite.

## Goal and evidence

The strict live gate must refuse missing or malformed context needed by either
combatant's equipped supported skills. Actual unknown context cannot produce a
numerical outcome. Preserve numerical behavior for well-formed supported inputs.

Brain reproduced these baseline cases using `battle()` from `tests/test_hard.py`
and `assess()` without mutating files: attacker Outdoor Fighter with
`outdoors: null` returns `NO_MODELED_DEATH_IN_THIS_DUEL`, displayed hit 85,
outcome non-null; `outdoors: "unknown"` returns that status with hit 95.
Lucky Seven with turn 0, -1 or true also produces a numerical outcome. These are
input-contract failures, not new claims about game mechanics.

## Ownership and acceptance

Own only `tools/tactical_combat.py`, new `tests/test_combat_context.py`, new
`docs/combat-context.md`, your batch summary and evidence under
`docs/batches/attachments/09-combat-context/`. Do not edit the general calculator,
proc engine, canonical data, rebuild code, STATUS, shared tests, framework or
Worker 08's files. If a necessary fix exceeds ownership, report the concrete
dependency to Brain without expanding scope.

For Indoor/Outdoor Fighter on either side, require an actual boolean outdoors
value. For Lucky Seven, Even Rhythm or Odd Rhythm on either side, require an
actual positive integer turn (booleans are not integers for this contract).
Missing/null/wrong-shaped inputs return UNKNOWN, outcome null and a useful
diagnostic. Exercise 0, negative numbers, booleans, floats, strings and containers.
Do not require absent optional fields when neither side has the relevant skill.
No defaulting or coercion; do not drop equipped skills to calculate an outcome.

Show meaningful regressions failing on the baseline and passing on delivery;
positive controls for indoor/outdoor values and turn boundaries 1/7/8 and parity;
both sides; supported before/after numerical equality; public JSON CLI behavior;
input immutability; existing paired/unsupported-effect refusals. Preserve all
other rules and never claim whole-map safety or new gameplay coverage.

Privately snapshot sorted canonical JSON and CURRENT_RUN.md plus every regular
state file before work/checks, and compare file sets/content afterwards. Do not
initialize or inspect a live run for test inputs. At the committed implementation,
run `make audit`, `python3 tools/fw.py check`, `git diff --check` and focused
regressions, recording actual output and exits. No rebuild is needed because
canonical data and rebuild code are outside scope. Render the new reference,
inspect appearance and resolve local links. Python 3.9+, standard library only.

Commit and push `docs/batches/09-combat-context.md` with Done, Checked, Not checked,
Failed or blocked; at most 500 prose words, output tables excluded. Record the
literal plan, starting main and implementation commits. Keep failures and limits.

## Verifier prompt

Send only after Worker finishes, to a fresh session:

```text
Fire Emblem Awakening Assistant · BATCH 09-combat-context · VERIFIER

Run python3 tools/fw.py status. Fetch origin and pin origin/worker/09-combat-context to one literal full commit. Read project rules, framework, verifier card, standing decisions and tactical policy. Read the plan via git show at the plan commit recorded by Worker; no plan merge prerequisite. Read only starting/plan commit metadata before the blind pass.

Independently reproduce malformed-context behavior at the recorded starting main commit before reading Worker conclusions or new tests. Then inspect the real diff and assess every goal in docs/plans/09-combat-context.md. Challenge both sides, missing/null/wrong-type outdoors and turn values, legitimate optional omissions, actual booleans versus integers, turn boundaries/parity, supported numerical equality, public CLI, unchanged inputs and existing refusals. Verify scope excludes map/data/rebuild/general-calculator changes.

Privately snapshot canonical JSON and CURRENT_RUN.md plus all regular state files; compare file sets/content after checks. Run make audit, python3 tools/fw.py check, git diff --check and focused regressions at the pinned commit. Show baseline regression failure, actual commands/output/exits and limits. Render the new reference, visually inspect it and resolve local links. Tests establish the input contract, not new gameplay truth.

Write only docs/batches/09-combat-context-review.md, at most 500 prose words excluding output tables: reviewed full commit, evidence, classified findings with file/line and a demonstrated failure or unproven claim, verdict and limits. Before pushing, check the remote Worker branch still equals your reviewed commit; stop and tell Brain if it moved. Commit the review on that Worker's branch in a separate checkout and push without force. Never implement or merge. End with batch, VERIFIER, outcome and pushed full commit. Technical questions go to Brain.
```

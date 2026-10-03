<!-- fw-report
round: 001-foundation-audit
role: worker
branch: worker/001-foundation-audit
head: 12119085ff05d4a87369ae01b345d5dac41eff3e
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T15:35:03Z
-->
## Verified

Reviewed full commit: `12119085ff05d4a87369ae01b345d5dac41eff3e`.
Production baseline: `c3eeb41e06a0a65fd76de6dafbdb454343cb2a9b`;
the reviewed commit adds only this round's audit artifacts. OS/Python from
`platform.system()`, `platform.release()`, `platform.python_version()`:
`Darwin`, `27.0.0`, `3.9.6`. No live run was initialized.

- At the reviewed commit, `python3 tools/fw.py check` → exit 0:
  `0 error(s), 0 warning(s)`.
- At the reviewed commit, `make audit` → exit 0:
  `Ran 102 tests in 0.321s`, `OK`. At baseline, both before/after audit logs
  also show exit 0, 102 tests and `OK`. Validator and phase-two/Hard audits
  report `passed: true`, empty errors; Hard inventory is 44 maps, 29
  reinforcement records, 217 registered sources. See
  `attachments/audit-before.txt` and `attachments/audit-after.txt`.
  Structural/reference hygiene and numerical regression checks passed;
  this does not verify source truth. Historical phase-two evidence counts
  15 independent numeric fields and zero fully verified schedules.
- `python3 docs/rounds/001-foundation-audit/attachments/reproduce.py` →
  exit 0, all subprocess exit statuses 0. This executes the brief's exact
  commands, including two `make rebuild` passes. Actual summary:
  `original drift: []`, `second-pass drift: []`.
  SHA-256 values for all 28 canonical data JSON files, `CURRENT_RUN.md` and
  every existing state file are in `attachments/reproduction.json` for
  before/first/second. Both rebuilds match the originals byte for byte;
  consequently Normal/Lunatic/Lunatic+ records also remain identical.
  State contained only `.gitkeep`; no `current_run.json` existed before or
  after. No generated difference needed restoration.
- The five required `python3 tools/map_info.py --chapter N --difficulty
  hard --turn 5 --phase PHASE` commands → exit 0 each. Actual JSON:
  Chapter 7 player targets 5 with one three-Wyvern candidate; enemy targets
  6 with no candidate and `safe_to_conclude_no_reinforcements: false`.
  Chapter 15 has no candidate, `none_supported`, and the same false flag.
  Chapter 5 returns a conflicted family; Chapter 17 returns three families
  including the conflicted first stairs, with `turns: null` and warning
  context retained. Full output: `attachments/map-*-*.txt`.
- At baseline and again at the reviewed commit,
  `python3 docs/rounds/001-foundation-audit/attachments/scenarios.py` →
  exit 0. Inputs/full outputs: `attachments/scenarios.json`; terminal
  output and command: `attachments/scenarios.txt`.
  Chapter 15 legacy turns 3/4/5 all return `[]` (queries target 4/5/6):
  quarantined waves do not leak through either query. Chapter 7 turn99 and
  Chapter 3 empty-wave queries retain false absence certainty and UNKNOWN
  warnings. Missing support state/partners, adjacent support, Counter,
  Dragonskin, Aether and explicit drain all return `UNKNOWN` with no
  outcome. Useful supported duel baseline returns worst HP 30/30 and
  `safe_to_claim_map_survival: false`.
- Three scoped source-report checks succeeded through the public reader;
  URLs, reader locations, dated authors/comments, access failures and
  applicability are recorded as code in `attachments/source-checks.md`.
  The original GBAtemp Hard report supports enemy-turn-start danger;
  Chapter 17's explicitly Hard 2012 comment supports the stored left-first
  alternative; Chapter 15's explicitly Hard comment reports absence.
  These are observations of source content, not new script certification.
- At the reviewed commit, `git diff --check` → exit 0, no output.
  `git diff --name-only c3eeb41e06a0a65fd76de6dafbdb454343cb2a9b -- .
  ':(exclude)docs/rounds/001-foundation-audit'` → exit 0, no output.
  Production, instructions, coverage, run state and other modes are untouched.

## Not verified

No game execution, controlled Hard/Classic footage, script extraction,
complete enemy geometry, full schedule, whole-map survival or unconditional
Ironman readiness was verified. No Linux/Windows run or current CI check
was performed; local results are macOS only. No gameplay coverage increased.
The stated 101-test historical status differs from the actual 102-test
suite; this audit does not edit status or certify an extra gameplay fact.

The three source checks do not establish Classic/Casual or precise software
version. Japanese comment context does not prove regional equivalence.
Chapter 17 phase/trigger and Chapter 5 alternatives remain unresolved.
The west/east guide alternative, Chapter 7 exact game arrivals and Chapter
15 contamination's Chapter 16 origin were not independently re-researched;
the quarantine exclusion itself was reproduced. Mirrors/repeated wiki
comments do not become independent corroboration. Initial wiki timeouts
were recorded; later ordinary reader navigation succeeded without bypasses.
Rendered Markdown appearance was not independently checked; artifacts are
plain audit text/JSON, with no live local links or designed layout.

## Changed

- `docs/rounds/001-foundation-audit/attachments/`: offline reproduction and
  in-memory scenario scripts, full command outputs, canonical/state hash
  comparison and three scoped source-check summaries.
- `docs/rounds/001-foundation-audit/worker.md`: evidence, findings and exactly
  one next-round recommendation. No production fix, merge or acceptance.
- `docs/state.md`: unchanged; no sentences added or removed.

## Open questions

Proven defects (priority is proposed for Brain review):

1. **P1 — missing custom weapon effects silently default to absence.**
   `tools/tactical_combat.py:22` validates the outer weapon field only;
   `tools/combat_calculator.py:60` defaults an omitted `effect` to `–`.
   In `missing_weapon_effect`, both custom weapons omit effect while the
   observed-completeness flag remains true. Actual output is
   `NO_MODELED_DEATH_IN_THIS_DUEL`, worst HP 30/30, death probabilities 0/0.
   An explicit unsupported drain instead returns UNKNOWN. Thus the strict
   gate does not enforce unknown weapon effects as unknown. Scope: custom
   weapon objects in the live wrapper; not evidence that a correctly supplied
   supported battle is numerically wrong. `brave`/`effectiveness` also have
   defaults at lines 62–63, but their omission was not separately reproduced.
2. **P2 — certainty is not reflected in the top-level risk label.**
   `tools/tactical_combat.py:30`–31 treats any positive death probability as
   `POTENTIALLY_LETHAL`. `certain_death` reproduces defender death probability
   `1.0`, worst HP 0, with that status instead of LETHAL. The numeric output
   is correct and available; the label fails the tactical policy's explicit
   certainty distinction. Scope: supported duel status, no map guarantee.

Unresolved coverage (not new defects):

- **High tactical consequence:** Chapter 5 schedule/classes conflict,
  `data/chapters/hard_reinforcements.json:5`; Chapter 17 first stairs/timing,
  same file line 1059. Both queries preserve alternatives. Planning around
  one side or an assumed last wave is not supported.
- **High tactical consequence:** `tools/map_info.py:54`–58 explicitly retains
  missing schedule/geometry. No observed regression turned empty waves into
  absence. Chapter 15's absence is single-source SUPPORTED, not verified.
- **Support/mechanics limits:** `tools/tactical_combat.py:16`–29 refuses
  missing support and explicit unsupported effects in reproduced cases;
  full dual outcome remains unavailable. A generic supported fixture is a
  useful calculation demonstration, not an exhaustive mechanics audit.

Exactly one recommended next round: **strict live-combat weapon completeness
and certainty gate**, proposed **Tier 2**. The reproduced omission undermines
safe use across maps, so it takes priority over the inherited Chapter 5/17
research candidates. Keep scope to the live wrapper, necessary validation,
focused regressions and input documentation; no mechanics expansion,
canonical research changes or Windows work.

Proposed acceptance: custom weapon effects and other material effect fields
must be explicitly known or resolved through a canonical record; missing
fields return UNKNOWN without silently dropping effects. Explicit unsupported
skills/drain/dual outcomes still refuse. Complete supported inputs retain
their existing numbers; certain death is LETHAL and non-certain positive
risk is POTENTIALLY_LETHAL, with both sides' probabilities preserved. Map
survival remains unclaimed. Exercise both sides, canonical-ID/custom/forged
inputs, missing/null fields, harmless explicit absence, certain/possible/no
modeled death. Run full audit/framework checks and prove run/data preservation.
Evidence needed: exact input/output regressions and independent blind Verifier
review at one literal commit, then Brain re-derivation. Any new factual
mechanics assertion needs separately scoped source evidence; tests cannot
certify one. Chapter 5/17 research remains outstanding after this bounded fix.

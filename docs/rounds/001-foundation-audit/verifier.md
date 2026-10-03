<!-- fw-report
round: 001-foundation-audit
role: verifier
branch: verifier/001-foundation-audit
head: 6c8e49a445c77cad25f6e3e4c3a9e0bfdb8c632b
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T15:41:47Z
-->
Reviewed commit: `6c8e49a445c77cad25f6e3e4c3a9e0bfdb8c632b`.
OS/Python: `macOS-27.0-arm64-arm-64bit`, `3.9.6`.

## Findings

- [SHOULD FIX, existing P1 defect] `tools/tactical_combat.py:22` and
  `tools/combat_calculator.py:60` — custom weapon effect omission bypasses
  the strict completeness gate. After my blind pass I independently reproduced
  the Worker's case: delete both weapon `effect` fields from `test_hard.battle()`;
  `assess` returns `NO_MODELED_DEATH_IN_THIS_DUEL`, worst HP `30/30`, death
  probabilities `0/0`. Explicit `Drains HP` instead returns `UNKNOWN`.
  Missing effects can therefore be modeled as absent despite the project policy.
  This is an inherited defect identified correctly by the audit, not introduced
  by this documentation-only delivery; it does not block recording the audit.
- [SHOULD FIX, existing P2 defect] `tools/tactical_combat.py:30`–31 — setting
  the fixture attacker's `brave=True`, skills to `['hawkeye']`, and defender HP
  to `20` produces defender death probability `1.0`, worst HP `0`, status
  `POTENTIALLY_LETHAL`. The probability remains available, but the status loses
  the policy's required certain-death distinction. Independently reproduced
  after reading the Worker report; no production correction made.
- [NOTE] `docs/rounds/001-foundation-audit/worker.md:135` — the one proposed
  Tier 2 weapon-completeness/certainty round is justified by reproduced failures.
  Acceptance should cover both combatants, canonical/custom/forged weapons,
  missing/null/explicit-absence fields, preserved supported numbers, continued
  unsupported-effect/support refusals and certain/possible/no modeled death.
  Require full audit, hygiene, run/data preservation, blind Verifier and Brain
  re-derivation. This is exactly one next round; Chapter 5/17 research stays pending.
- [NOTE] `docs/rounds/001-foundation-audit/worker.md:64` — all three claimed
  source-report observations reproduced. These prove source contents, not all
  game events, Classic applicability or precise version. No unsupported readiness
  certification was added. No new tests were delivered; existing tests can pass
  despite the two defects above. No removed state decision or production change.

### Independent first pass and commands

I completed the diff/policy review, audit, two rebuilds, map and support/effect
probes, and initial source checks before opening `worker.md`. Then I read the
Worker report and its scripts/evidence and independently reproduced its defects
and its two Japanese source comments. Commands below ran at the reviewed commit.

```text
git diff --stat origin/main HEAD
exit 0; 22 files changed, 5716 insertions; only this round's files.
git diff origin/main HEAD -- ':!docs/rounds/001-foundation-audit/worker.md' ':!docs/rounds/001-foundation-audit/attachments/*'
exit 0; brief only (attachments reviewed separately after blind pass).
python3 tools/fw.py check
exit 0; 0 error(s), 0 warning(s)
make audit
exit 0; Ran 102 tests in 0.363s; OK
make rebuild
exit 0; original drift {}
make rebuild
exit 0; second-pass drift {}; two passes identical True
make audit
exit 0; Ran 102 tests in 0.339s; OK
git diff --check
exit 0; no output
git diff --stat
exit 0; no output after rebuilds
```

Validators report structural/reference consistency, and regression fixtures check
selected numerical cases. Neither establishes source truth or complete map safety.
No game coverage increased. Historical 101-test text is not this run's 102 result.

The exact five CLI commands ran via Python subprocess, parsed as JSON; each exit 0:

```text
python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase player
EP5; [hard_chapter_7_t5]; PARTIAL; absence certainty false
python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase enemy
EP6; []; PARTIAL; absence certainty false
python3 tools/map_info.py --chapter 15 --difficulty hard --turn 5 --phase player
EP5; []; reported absence SUPPORTED; absence certainty false
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 5 --phase player
EP5; [hard_chapter_5_disputed_schedule]; CONFLICTED; alternatives retained
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 5 --phase player
EP5; [hard_chapter_17_first, hard_chapter_17_second, hard_chapter_17_central];
CONFLICTED; east/left alternatives and warning-relative null turns retained
```

Additional in-memory probes (`python3 -`, exit 0) used this import/input pattern:

```python
import sys
sys.path[:0] = ['tools', 'tests']
from test_hard import battle
from tactical_combat import assess
from tactical_query import query as legacy
from map_info import query
for t in (3, 4, 5):
    print(legacy('chapter_15', 'Hard', t)['possible_reported_waves'])
q = query(7, turn=99, phase='player')
print(q['candidate_reinforcements'], q['safe_to_conclude_no_reinforcements'])
for key in ('partners', 'support_state'):
    p = battle(); del p[key]; print(assess(p))
p = battle(); p['support_state'] = 'adjacent'; print(assess(p))
for skill in ('counter', 'dragonskin'):
    p = battle(); p['defender']['skills'] = [skill]; print(assess(p))
p = battle(); p['attacker']['weapon']['effect'] = 'Drains HP'; print(assess(p))
p = battle()
for side in ('attacker', 'defender'): del p[side]['weapon']['effect']
r = assess(p)
print(r['status'], r['worst_attacker_hp'], r['worst_defender_hp'],
      r['outcome']['attacker_death_probability'], r['outcome']['defender_death_probability'])
p = battle(); p['attacker']['weapon']['brave'] = True
p['attacker']['skills'] = ['hawkeye']; p['defender']['current_hp'] = 20
r = assess(p)
print(r['status'], r['outcome']['defender_death_probability'])
```

Actual results: legacy Chapter 15 `[]` three times; Chapter 7 turn99 `[] False`
plus `Complete schedule not established. No matching fixed-turn wave does NOT
mean no spawn.` Missing partners/support each `UNKNOWN`, outcome null;
adjacent `UNKNOWN`, full dual outcome unsupported; Counter/Dragonskin `UNKNOWN`
with unsupported skill reason; drain `UNKNOWN`, `Unsupported weapon effect:
Drains HP`. Defect outputs are quoted above. Chapter 15 quarantine exclusion
is demonstrated; external Chapter 16 contamination origin is not re-derived.

### Rebuild hash evidence

My Python snapshot used sorted `Path('.').glob('data/**/*.json')`,
`CURRENT_RUN.md` and every file under `state`, hashing raw bytes with
`hashlib.sha256(...).hexdigest()` before and after each `subprocess.run(['make',
'rebuild'], capture_output=True, text=True)`. Both subprocesses exited 0.
All 30 before/first/second entries were equal. This preserves the entire canonical
files, including other modes. Only `state/.gitkeep` existed; no live run to test.
After comparison, my hashes also matched all three Worker snapshots exactly.
Below each hash applies to before, first and second (no original or subsequent drift):

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

### Source checks, 2026-10-03

Public reader retrieval only; no bypass, page archive or source-family multiplication.
URLs and excerpts below are code, as required for this report.

1. `https://gbatemp.net/threads/fire-emblem-awakening-reinforcements.435653/`
   — original Prior22 post #1, 2016-07-26, reader lines 148–149:
   `reinforcements spawn at the beginning of the enemy turn`.
   Explicit Awakening Hard player report describes resulting deaths. This is
   firsthand reported evidence, with no visible game reproduction, Classic/Casual,
   region/version or exhaustive exceptions. Direct retrieval succeeded. Gamer
   Guides' Starting a New Game page line 340 independently states immediate action
   on Hard or above; publisher prose is corroboration, not primary game proof.
2. `https://www.pegasusknight.com/wiki/fe13/マップ攻略/章別攻略/17章+死の運命`
   — original anonymous 2012-04-27 comment, reader line 140: `（ハード）`.
   My reading: roughly three turns after Say'ri's warning, four reinforcements
   from the four left stairs, including a Sniper. Lines 142–143 preserve uncertain
   trigger/timing and an unlabelled right-first report. Conflicting alternative
   remains unresolved; phase, Classic/Casual and version unspecified.
3. `https://www.pegasusknight.com/wiki/fe13/マップ攻略/章別攻略/15章+解放の狼煙`
   — anonymous 2012-04-30 comment, reader line 140: `増援もないし` and `(ハード)`.
   My reading: no reinforcements in that Hard play report. Same original evidence
   family as stored absence; no exhaustive script/trigger/version guarantee.

I additionally read Serenes Forest Calculations' five-speed doubling threshold
and saw it agrees with the existing boundary regression; its page credits other
wikis, so it supplies no independent primary-game certification. The Incursion
Fandom page returned an internal retrieval error; the accessible Chapter 7 guide
reader had no western-arrival text. Exact Chapter 7 arrivals remain unverified
externally in this session, rather than inferred from passing data tests.

## Not verified

No controlled game footage, game-script audit, complete reinforcement schedule,
complete coordinates/enemy threat geometry, region/version equivalence, complete
mechanics, unconditional Ironman safety or newly initialized playthrough.
Chapter 5/17 factual disagreements and Chapter 15 contamination origin remain
unresolved/unrederived respectively. Linux/Windows and current CI not rerun.
No live run preservation test: state contained only `.gitkeep`; tests use temporary
state. Source access failures cannot establish absence. Markdown visual appearance
of Worker artifacts was not independently rendered; plain text/code/JSON reviewed,
JSON parsed successfully, no new local Markdown links requiring resolution.
No broad factual certification follows from the structural and numerical audit.

## Verdict

The audit delivery meets the substantive investigation criteria at the reviewed
commit with strong local reproducibility and explicitly bounded source evidence.
Its production files, state decisions, canonical data, other modes and run pointer
are unchanged. I independently confirm both reported inherited combat-gate defects
and support the single Tier 2 next-round recommendation above. No blocker to
recording this audit was found; these findings inform Brain's review, not merge
approval, and do not certify unconditional tactical safety.

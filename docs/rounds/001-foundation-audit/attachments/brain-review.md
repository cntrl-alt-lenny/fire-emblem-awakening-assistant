# Brain review — 001-foundation-audit

Decision: accept the audit as an investigation record at delivered commit
`3da1cd4408fd51d28606058ae74b956d587c72eb`, pending owner approval to merge.
Worker evidence describes `12119085ff05d4a87369ae01b345d5dac41eff3e`;
Verifier reviewed `6c8e49a445c77cad25f6e3e4c3a9e0bfdb8c632b`. The final
delivery adds the Verifier report only. Brain reviewed both reports, the
scripts/artifacts and actual diff and reran checks at the final delivery.
No production change or new tactical coverage was delivered.

## Independent evidence

Brain commands ran at the exact delivered commit on Darwin 27.0 / Python
3.9.6 on 2026-10-03. Every command below exited 0.

```text
python3 tools/fw.py delivery --round 001-foundation-audit
origin/verifier/001-foundation-audit (3da1cd4408fd): delivered
verifier: report describes 6c8e49a445c7
worker: report describes 12119085ff05

make audit
All three validators: passed true, errors []
Hard: 44 campaign maps, 29 reinforcement records, 217 sources
Ran 102 tests in 0.332s
OK

python3 tools/fw.py check
0 error(s), 0 warning(s)

git diff --check
(no output)

git diff c3eeb41..HEAD -- . ':(exclude)docs/rounds/001-foundation-audit'
(no output)

gh run view 37134154412 --json conclusion,headSha,jobs,url
headSha: 3da1cd4408fd51d28606058ae74b956d587c72eb
conclusion: success
Audit (ubuntu-latest, Python 3.9): success
Audit (ubuntu-latest, Python 3.13): success
Audit (macos-latest, Python 3.13): success

make audit (after the two independent rebuilds below)
Ran 102 tests in 0.336s
OK
```

Independent `python3 -` probes imported `battle` from `test_hard`, `assess`
from `tactical_combat`, `query` from `map_info` and the legacy query from
`tactical_query`. Relevant inputs and actual results:

```python
for side in ('attacker', 'defender'):
    p = battle()
    del p[side]['weapon']['effect']
    r = assess(p)
    print(side, r['status'], r['outcome']['attacker_death_probability'],
          r['outcome']['defender_death_probability'])
    p = battle()
    p[side]['weapon']['effect'] = 'Drains HP'
    print(side, assess(p)['status'], assess(p).get('reason'))
p = battle()
p['attacker']['weapon']['brave'] = True
p['attacker']['skills'] = ['hawkeye']
p['defender']['current_hp'] = 20
r = assess(p)
print(r['status'], r['outcome']['defender_death_probability'],
      r['worst_defender_hp'])
```

```text
attacker NO_MODELED_DEATH_IN_THIS_DUEL 0 0
attacker UNKNOWN Unsupported weapon effect: Drains HP
defender NO_MODELED_DEATH_IN_THIS_DUEL 0 0
defender UNKNOWN Unsupported weapon effect: Drains HP
POTENTIALLY_LETHAL 1.0 0
```

Missing `partners` or `support_state` returned `UNKNOWN`, outcome null.
Defender `counter`, `dragonskin` and `aether` each returned `UNKNOWN` with
the corresponding unsupported-skill diagnostic. The map probes retained
the following behavior (all absence-certainty flags were false):

```text
chapter 7, turn 5 player: target EP5, 1 candidate
chapter 7, turn 5 enemy: target EP6, 0 candidates
chapter 15, turn 5 player: 0 candidates
chapter 5, turn 5 player: 1 candidate, CONFLICTED retained
chapter 17, turn 5 player: 3 candidates, CONFLICTED/PARTIAL retained
chapter 7, turn 99 player: 0 candidates, UNKNOWN retained
chapter 3, turn 5 player: 0 candidates, UNKNOWN retained
legacy chapter_15 Hard queries turns 3/4/5: [] / [] / []
```

Brain independently hashed sorted `data/**/*.json`, `CURRENT_RUN.md` and
all files under `state` using `hashlib.sha256(path.read_bytes()).hexdigest()`.
Two `subprocess.run(['make', 'rebuild'], capture_output=True, text=True)`
passes each exited 0. Both file-set/hash comparisons covered 30 files and
had original drift `[]`. All final hashes matched all three Worker snapshots
in `reproduction.json`. Only `state/.gitkeep` existed; no live run was
initialized. `git status --porcelain` after rebuilds produced no output.

## Findings judged

The two combat failures are independently reproduced inherited defects, not
audit regressions. They do not block recording the investigation, but justify
the next Tier 2 round before more map research. All Verifier findings were
checked: scope is audit-only, existing tests pass despite those defects,
the bounded recommendation is appropriate and source claims are limited.

Brain reread the original public source contexts through the web reader:

- `https://gbatemp.net/threads/fire-emblem-awakening-reinforcements.435653/`
  — Prior22, 2016-07-26, post 1: firsthand Hard report states enemy-turn-start
  reinforcements and deaths. Mode/region/version and exceptions unspecified.
- `https://www.pegasusknight.com/wiki/fe13/マップ攻略/章別攻略/17章+死の運命`
  — 2012-04-27 Hard comment: approximately three turns after the warning,
  four arrivals from the left stairs, including a Sniper. Subsequent comments
  retain uncertain trigger/timing and a right-first report without difficulty.
- `https://www.pegasusknight.com/wiki/fe13/マップ攻略/章別攻略/15章+解放の狼煙`
  — 2012-04-30 Hard comment reports no reinforcements in that play report.

These observations match the reports' summaries, not complete script proof.
No game execution, region/version equivalence, full map geometry/schedule or
unconditional Ironman readiness is certified. Chapter 5/17 conflicts and
Chapter 15 contamination origin remain unresolved/unrederived respectively.
No native Windows run or live-state preservation test was performed.

## Merge card

What changed: a reproducible foundation audit and independent reports only.
Verified: 102 local tests, required audits/hygiene, Linux/macOS CI, unchanged
rebuild hashes and independently reproduced failure paths at the delivery.
Not verified: complete mechanics, map schedules, live play or map survival.
Risk: recording the audit leaves its two demonstrated combat defects present;
round 002 addresses them without increasing gameplay certification.

Merge requires the owner's approval under `AGENTS.md`. No merge performed.

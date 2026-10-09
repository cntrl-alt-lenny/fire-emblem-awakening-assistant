# Batch 08 command evidence

Implementation checked: `3211c2ff3e39ab86cb903c6ddfff1fde8651c60a`.

## Baseline regression

Starting main: `d3b646975a5f0686a798aaf12c0e541ed396da08`. Only the four new test methods were added before this command:

```text
$ python3 -m unittest discover -s tests -p test_hard.py -v
exit 1
Ran 45 tests in 0.149s
FAILED (failures=6)
test_chapter11_family_not_recurrence: fixed != conditional_report
test_chapter11_fort_family_phase_boundaries: False != True at
(3, enemy), (4, player), (4, enemy), (5, player), (99, player)
```

Fixed-turn and unknown/event controls passed at baseline.

## Committed checks

The following commands ran at the implementation commit. Output excerpts are real; source truth is outside the test guarantee.

| Command | Relevant output | Exit |
|---|---|---:|
| `make rebuild` (first) | Hard audit: passed true; 44 maps; 29 records; 217 sources | 0 |
| `make rebuild` (second) | Hard audit: passed true; 44 maps; 29 records; 217 sources | 0 |
| `make audit` | Ran 122 tests in 0.629s; ; OK; validation and both semantic audits passed | 0 |
| `python3 tools/fw.py check` | 0 error(s), 0 warning(s) | 0 |
| `git diff --check` | No output | 0 |

## Preservation and query checks

`python3 /tmp/fea08-checks.py` exited 0. The reproduction script below uses an external private snapshot directory. Snapshot contents and private filenames are never committed. Snapshot creation occurred before implementation: all `data/**/*.json` copied privately; SHA-256 maps captured for canonical files, primary and Worker `CURRENT_RUN.md`, and every regular nonsymlink `state/**/*` file. No run files were copied into the Worker checkout.

```text
Two rebuilds: all 28 canonical JSON hashes identical
$ make audit
exit 0
it (test_phase2.ProcTests) ... ok
test_basic_damage_and_doubling_boundary (test_tools.CombatTests) ... ok
test_dual_explicitly_partial (test_tools.CombatTests) ... ok
test_effective_triples_might (test_tools.CombatTests) ... ok
test_magic_targets_res (test_tools.CombatTests) ... ok
test_probability_and_early_death (test_tools.CombatTests) ... ok
test_rank_and_triangle (test_tools.CombatTests) ... ok
test_true_hit (test_tools.CombatTests) ... ok
test_unsupported_and_invalid (test_tools.CombatTests) ... ok
test_comparison_rejects_wrong_level (test_tools.ExtraToolsTests) ... ok
test_enemy_phase_accumulates_damage (test_tools.ExtraToolsTests) ... ok
test_forge (test_tools.ExtraToolsTests) ... ok
test_low_level_promotion_refused (test_tools.ExtraToolsTests) ... ok
test_avatar (test_tools.GrowthTests) ... ok
test_cap (test_tools.GrowthTests) ... ok
test_child (test_tools.GrowthTests) ... ok
test_growth_and_projection (test_tools.GrowthTests) ... ok
test_internal (test_tools.GrowthTests) ... ok
test_dual (test_tools.PairTests) ... ok
test_threshold_support (test_tools.PairTests) ... ok
test_atomic_failure (test_tools.StateTests) ... ok
test_casual (test_tools.StateTests) ... ok
test_class_history (test_tools.StateTests) ... ok
test_consumption (test_tools.StateTests) ... ok
test_death_and_no_resurrection (test_tools.StateTests) ... ok
test_level_history (test_tools.StateTests) ... ok

----------------------------------------------------------------------
Ran 122 tests in 0.629s

OK

$ python3 tools/fw.py check
exit 0
0 error(s), 0 warning(s)

$ git diff --check
exit 0

Canonical baseline changes: ['data/chapters/hard_reinforcements.json']
Unrelated Hard waves, fixed northwest record, other-mode records and quarantine: preserved
primary private regular file set/content: preserved
worker private regular file set/content: preserved
query 11 1 player => EP 1 (none) complete=False
query 11 1 enemy => EP 2 (none) complete=False
query 11 2 player => EP 2 (none) complete=False
query 11 2 enemy => EP 3 hard_chapter_11_t3_forts complete=False
query 11 3 player => EP 3 hard_chapter_11_t3_forts complete=False
query 11 3 enemy => EP 4 hard_chapter_11_t3_forts,hard_chapter_11_t4_nw complete=False
query 11 4 player => EP 4 hard_chapter_11_t3_forts,hard_chapter_11_t4_nw complete=False
query 11 4 enemy => EP 5 hard_chapter_11_t3_forts complete=False
query 11 5 player => EP 5 hard_chapter_11_t3_forts complete=False
query 11 5 enemy => EP 6 hard_chapter_11_t3_forts complete=False
query 11 99 player => EP 99 hard_chapter_11_t3_forts complete=False
query 11 99 enemy => EP 100 hard_chapter_11_t3_forts complete=False
query 7 3 player => EP 3 (none) complete=False
query 7 3 enemy => EP 4 (none) complete=False
query 7 4 player => EP 4 (none) complete=False
query 7 4 enemy => EP 5 hard_chapter_7_t5 complete=False
query 7 5 player => EP 5 hard_chapter_7_t5 complete=False
query 7 5 enemy => EP 6 (none) complete=False
query 7 6 player => EP 6 (none) complete=False
query 7 6 enemy => EP 7 (none) complete=False
query 7 99 player => EP 99 (none) complete=False
query 7 99 enemy => EP 100 (none) complete=False
query 16 3 player => EP 3 (none) complete=False
query 16 3 enemy => EP 4 hard_chapter_16_t4 complete=False
query 16 4 player => EP 4 hard_chapter_16_t4 complete=False
query 16 4 enemy => EP 5 hard_chapter_16_t5 complete=False
query 16 5 player => EP 5 hard_chapter_16_t5 complete=False
query 16 5 enemy => EP 6 hard_chapter_16_t6 complete=False
query 16 6 player => EP 6 hard_chapter_16_t6 complete=False
query 16 6 enemy => EP 7 (none) complete=False
query 16 99 player => EP 99 (none) complete=False
query 16 99 enemy => EP 100 (none) complete=False
query 19 3 player => EP 3 hard_chapter_19_forts complete=False
query 19 3 enemy => EP 4 hard_chapter_19_forts complete=False
query 19 4 player => EP 4 hard_chapter_19_forts complete=False
query 19 4 enemy => EP 5 hard_chapter_19_forts complete=False
query 19 5 player => EP 5 hard_chapter_19_forts complete=False
query 19 5 enemy => EP 6 hard_chapter_19_forts complete=False
query 19 6 player => EP 6 hard_chapter_19_forts complete=False
query 19 6 enemy => EP 7 hard_chapter_19_forts complete=False
query 19 99 player => EP 99 hard_chapter_19_forts complete=False
query 19 99 enemy => EP 100 hard_chapter_19_forts complete=False
query para10 3 player => EP 3 hard_paralogue_10_severa_join complete=False
query para10 3 enemy => EP 4 hard_paralogue_10_severa_join complete=False
query para10 4 player => EP 4 hard_paralogue_10_severa_join complete=False
query para10 4 enemy => EP 5 hard_paralogue_10_severa_join complete=False
query para10 5 player => EP 5 hard_paralogue_10_severa_join complete=False
query para10 5 enemy => EP 6 hard_paralogue_10_severa_join complete=False
query para10 6 player => EP 6 hard_paralogue_10_severa_join complete=False
query para10 6 enemy => EP 7 hard_paralogue_10_severa_join complete=False
query para10 99 player => EP 99 hard_paralogue_10_severa_join complete=False
query para10 99 enemy => EP 100 hard_paralogue_10_severa_join complete=False
query para14 3 player => EP 3 hard_paralogue_14_village_visits complete=False
query para14 3 enemy => EP 4 hard_paralogue_14_village_visits complete=False
query para14 4 player => EP 4 hard_paralogue_14_village_visits complete=False
query para14 4 enemy => EP 5 hard_paralogue_14_village_visits complete=False
query para14 5 player => EP 5 hard_paralogue_14_village_visits complete=False
query para14 5 enemy => EP 6 hard_paralogue_14_village_visits complete=False
query para14 6 player => EP 6 hard_paralogue_14_village_visits complete=False
query para14 6 enemy => EP 7 hard_paralogue_14_village_visits complete=False
query para14 99 player => EP 99 hard_paralogue_14_village_visits complete=False
query para14 99 enemy => EP 100 hard_paralogue_14_village_visits complete=False
Coverage: complete_schedules=0
```

Two manifest columns are equal for every canonical file:

| Canonical JSON | First and second SHA-256 |
|---|---|
| `data/chapters/chapters.json` | `301678441555a989c2ada13e699fa8cbf365cf3f9d30f5465076229f0beecec0` |
| `data/chapters/coverage.json` | `1e5686b0f9d7d5a85b0594a1398eb7e0e106b83dc0680a5a76e956579ac77968` |
| `data/chapters/hard_quarantine.json` | `ff5a462725798c2de9a67a1dd0718801a550419bcc0a917239ac246115b66c0d` |
| `data/chapters/hard_reinforcements.json` | `86f251086e9185e3a4a2fc3bf16a2c46dc3dc34ebfdf5c169e9a9b14603e736d` |
| `data/chapters/hard_tactics.json` | `b258d40f39a9623a3870f7ce5c83ad05c0b02eb47e16b6621cac755574e0b83a` |
| `data/chapters/reinforcement_candidates.json` | `0e7d1d4894738006fcdec262d1b0657f99b8b450c27af1d6b166e486e6a9c936` |
| `data/chapters/reinforcements.json` | `bf46d31ea7ad831b52383c33667d4974e6dcad85641626d74eb6b9b6154a82c1` |
| `data/characters/avatar.json` | `3b588a14fb35c77d42b2547171998b20a816edbbbf12a422873fac94224ddeac` |
| `data/characters/characters.json` | `4f54400942c687b496e40af06a3a7e7cc20f2a34c77cd14044ae957eae9bb82b` |
| `data/classes/classes.json` | `f07f10b348b1835a4c1a4ec84fb978646bc6b2aaaf86d913bce48b4e9fd0482d` |
| `data/difficulty/modes.json` | `1c6a0baa882721b3bfde4b269aff7037012d076182c0db01c26d54c8dfe60172` |
| `data/enemies/enemies.json` | `f2d0e7719310e7c49da13157bdf6379143d6c30616a080564c3c6a8bb1f2a62a` |
| `data/items/economy.json` | `03e18dad1cd970cde9a717e6617dbf1aee4a33e3a903be279acd4cd0c759cc9e` |
| `data/items/items.json` | `1b94b2cecd0de4a2d26fd6c1de79d0e757c776570476f73e0494f72f26c5d596` |
| `data/items/merchant_rare_pool.json` | `f1a902dafcd3eaa4e116279f2200f3f8b951b9f1d87ac0ced32615dad93f4f4c` |
| `data/items/merchants.json` | `8530a6d6bfe4fb9c34801081a4a596db0f289862f4c546bcac6c7d14f78d4110` |
| `data/items/renown.json` | `8072580f2791cfe3a0f4eb6ab7d507192d92da91945e3476d05466d731142ee7` |
| `data/items/shops.json` | `d599bc212b256f8e8119f8193e721c9e7865cba0f799dd3fbb5d4d28e69ef022` |
| `data/mechanics/availability_and_barracks.json` | `0e550caeaa78d1e75604e75c2c51239e8b250f4af04d4b76420fcb01f69458cd` |
| `data/mechanics/formulas.json` | `cf0e9f4e27649d7ab75ece623ad492755149686a21887db8821d11c6aaa6e52a` |
| `data/mechanics/progression.json` | `2568cb81a61cb30536d5f40dc5eec5939105226711d90d5be202e1819410b191` |
| `data/mechanics/world_and_boosts.json` | `99c3530d9cf6afed1b4e6223bd44d0b44ba00a8ae2de999484a9ce39ff02d1a2` |
| `data/skills/skills.json` | `6d2c5e58a50f72347ff742067a26c377ef0dd8def9522a662eafb30ca4707369` |
| `data/sources.json` | `ce813be7d7ca117625857eda17d86b949359e87e08a850a71b374f133f89f8a6` |
| `data/supports/compatibility.json` | `3ec4ca0113c107b9748acc89e89d922e5f64a9edbe19f96af6321e76e3e92086` |
| `data/supports/rules.json` | `3fbe849617c84f1f7ec97b0504ce2fdbfd8823c4773c29edf3f2a1c4049cb642` |
| `data/supports/support_growth.json` | `c7a76da8ef3aa892e6603014cf07151ca9f6922571b349c68aaed1ab1eb3cf5f` |
| `data/weapons/weapons.json` | `f49806a31eb8b93115135f98e52eb0012266b45ddf8d6b9a935db1950d85024c` |

## Reproduction script

Run from the Worker checkout with the private baseline under `/tmp/fea08-private`; this path is local evidence staging, not a repository dependency.

```python
import hashlib,json,pathlib,subprocess
root=pathlib.Path.cwd();out=pathlib.Path('/tmp/fea08-private')
def hashes():return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'data').rglob('*.json'))}
def run(cmd,name):
 p=subprocess.run(cmd,shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/(name+'.log')).write_text(p.stdout)
 print('$ '+cmd+'\nexit '+str(p.returncode)+'\n'+p.stdout[-1500:]);assert p.returncode==0
run('make rebuild','rebuild1');h1=hashes();(out/'rebuild1-hashes.json').write_text(json.dumps(h1,indent=2))
run('make rebuild','rebuild2');h2=hashes();(out/'rebuild2-hashes.json').write_text(json.dumps(h2,indent=2));assert h1==h2;print('Two rebuilds: all '+str(len(h1))+' canonical JSON hashes identical')
run('make audit','audit');run('python3 tools/fw.py check','fwcheck');run('git diff --check','diffcheck')
before=json.loads((out/'canonical-baseline.json').read_text());changed=[p for p in h2 if h2[p]!=before[p]];assert changed==['data/chapters/hard_reinforcements.json'];assert set(h2)==set(before);print('Canonical baseline changes: '+str(changed))
old=json.loads((out/'data/chapters/hard_reinforcements.json').read_text())['records'];new=json.loads((root/'data/chapters/hard_reinforcements.json').read_text())['records']
assert [w for w in old if w['id']!='hard_chapter_11_t3_forts']==[w for w in new if w['id']!='hard_chapter_11_t3_forts']
a=next(w for w in old if w['id']=='hard_chapter_11_t3_forts');b=next(w for w in new if w['id']==a['id']);assert {k:v for k,v in a.items() if k!='timing'}=={k:v for k,v in b.items() if k!='timing'}
print('Unrelated Hard waves, fixed northwest record, other-mode records and quarantine: preserved')
for name,r in [('primary',root.parents[1]),('worker',root)]:
 ps=[r/'CURRENT_RUN.md']+list((r/'state').rglob('*'));actual={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ps if p.is_file() and not p.is_symlink()}
 assert actual==json.loads((out/(name+'-private.json')).read_text());print(name+' private regular file set/content: preserved')
import sys;sys.path.insert(0,str(root/'tools'));from map_info import query
for c in [11,7,16,19,'para10','para14']:
 for turn in ([1,2,3,4,5,99] if c==11 else [3,4,5,6,99]):
  for phase in ['player','enemy']:
   q=query(c,turn=turn,phase=phase);print('query',c,turn,phase,'=> EP',q['target_enemy_phase_turn'],','.join(w['id'] for w in q['candidate_reinforcements']) or '(none)','complete='+str(q['schedule_complete']))
print('Coverage: complete_schedules='+str(json.loads((root/'research/hard_verification/coverage_counts.json').read_text())['complete_schedules']))
```

## Failed attempts and limits

The first bounded authoring comparison used `exec` without `__file__` and exited 1 (`NameError`). Supplying the authoring file location fixed the harness; the bounded Chapter 11 authoring and reviewed timing matched (exit 0). The bundled Python environment lacked `markdown` (`ModuleNotFoundError`, exit 1); rendering used bundled Node `marked` and Playwright instead. Playwright’s default browser executable was missing (exit 1); selecting installed Chrome resolved it. An executable inventory found Chrome but no Edge (exit 1). The initial session stopped because the original plan-on-main prerequisite was absent (Git exit 128); the corrected prompt superseded it. No implementation or run changes occurred during that wait.

No gameplay observation, independent source corroboration, full fort schedule, regional equivalence or complete map safety was established.

## Continuation verification — 2026-10-09

Rechecked the existing delivery `3fd7282116feb054626b87265f5821e8779a5ad0`;
no implementation changes or branch restart. `git fetch origin` exited 0 and
the remote Worker branch matched that commit. Framework status passed its
project checks; the tracked 4.0.1 patch warning remains Brain-owned.

The reproduction script above ran again against the retained private baseline.
Actual output:

```text
$ python3 /tmp/fea08-checks.py
exit 0
make rebuild (first): exit 0; Hard audit passed true
make rebuild (second): exit 0; Hard audit passed true
Two rebuilds: all 28 canonical JSON hashes identical
make audit: exit 0
Ran 122 tests in 0.665s

OK
python3 tools/fw.py check: exit 0; 0 error(s), 0 warning(s)
git diff --check: exit 0; no output
Canonical baseline changes: ['data/chapters/hard_reinforcements.json']
Unrelated Hard waves, fixed northwest record, other-mode records and quarantine: preserved
primary private regular file set/content: preserved
worker private regular file set/content: preserved
Coverage: complete_schedules=0
```

The full phase-control matrix above was reproduced unchanged. The temporary
baseline reproduction extracted `git archive` of starting main outside the
checkout and copied only the current `tests/test_hard.py` into that extraction.
`python3 -m unittest discover -s tests -p test_hard.py -v` there exited 1:
`Ran 45 tests in 0.143s`, `FAILED (failures=6)`, with the same representation
and five phase-boundary failures listed above. The harness exited 0 after
asserting that expected failure result. No live state was copied or modified.

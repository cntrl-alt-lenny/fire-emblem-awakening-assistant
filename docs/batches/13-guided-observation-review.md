# 13-guided-observation — Verifier review

Verdict: **PASS — no outstanding findings at the revised delivery.** Brain
acceptance and owner merge approval remain required.

| Anchor | Exact commit |
|---|---|
| Reviewed revised delivery, fetch-confirmed Worker remote | `56193e1c38e784a8ad77eed4e65b177239dabf9e` |
| Original reviewed delivery | `872259eef43594b3371327d6f0a90d5f6b02a1ad` |
| Preserved failed review, ancestor of revised delivery | `517315b6f652c347c3c54dbf217e246c4cee8a63` |
| Independent baseline | `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba` |
| Plan / clarification | `7f4553587263772d9539e571c04abb18207704bf` / `b90a1eaf8e7aaf2ec3796d24b4c730a7ea83024d` |

## Findings disposition

**RESOLVED BLOCKER — retained unknown effects/state.** The original public edit
with `attacker.forge: {"might": null}`, 27 deliberate `keep` answers and final
`yes`, preserved unknown data but earned completeness. Retained `alive: "?"`
or string `"false"` additionally produced supported numeric diagnostics; empty
forge list/object did too. The previous report and Git history preserve these
failures. The revised production recursively checks retained forge observations
and validates alive/metadata types before confirming completeness.

Independently replayed both sides: null/unknown/empty and malformed nested forge,
alive strings/objects/integers, unit/weapon metadata and nested containers stay
unchanged, incomplete and UNKNOWN without numbers. Known nonempty forge markers
remain complete but unsupported; no effect was removed. Boolean true preserves
supported results; actual boolean false still refuses dead-unit combat.

**RESOLVED NOTE — measured input burden.** Supported two-catalog entry takes 27
answers. Reference, current summary and runner footer now agree; custom entry
still takes 41 answers and groups 16 stats into two answers, with zero manual
JSON edits. Scripted burden does not establish human usability.

## Independent evidence

The original private complete/incomplete expectations came from baseline schema
and policy before production, new tests or Worker conclusions. Follow-up ordering:
actual correction diff, independent CLI/matrix, new tests, Worker narrative.
Symmetric 30 HP/12 strength/5-might swords still give damage 9, displayed hit 87
and no modeled death. Existing public gate/full assessment equality and engine
byte comparisons agree with baseline.

| Command/control at reviewed revised delivery | Actual result | Exit |
|---|---|---:|
| `make audit` | All three audits pass; 181 tests OK | 0 |
| `python3 tools/fw.py check` | 0 errors, 0 warnings | 0 |
| `python3 -m unittest discover -s tests -p test_observed_input.py -v` | 15 tests OK | 0 |
| `git diff --check 5c596d42adb3d2a5eeee460032ee20bdd4bb78ba HEAD` | Empty | 0 |
| `gh run list --branch worker/13-guided-observation --limit 3 --json headSha,status,conclusion,url,name` | Exact delivery CI completed/success, run 38226786912 | 0 |
| Independent private public-CLI runner / edit matrix | 30 controls / 150 controls pass | 0 |
| Existing `tools/tactical_combat.py` public CLI | Exact baseline full assessment equality | 0 |
| Private headless Markdown render/link checks | Reference/summary/attempts readable; 8 links resolve; zero overflow | 0 |

Controls additionally cover partial/blank stats, integer retries, raw basis,
Counter/drain, forged values, unarmed/paired, explicit context null, renewed
confirmation, duplicate/extra/run-shaped sources, cancellation/EOF and
create-only overwrite/traversal/symlink/run-name refusals. Drafts and existing
outputs stay unchanged. Fresh private snapshots prove primary/detached canonical,
research and private file sets/content unchanged; no private values/hashes
published. Canonical data, research and shared engines have no baseline diff.

First follow-up replay hit a leftover private synthetic symlink; cleaned only
harness artifacts and reran successfully. No production failure resulted.
Only this report changes. No implementation, merge, new gameplay fact, coverage,
human usability, native Windows or whole-map safety verification occurred.
Combined Batch14/Brain acceptance remains pending.

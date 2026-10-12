# 13-guided-observation — Verifier review

Reviewed literal delivery `872259eef43594b3371327d6f0a90d5f6b02a1ad`,
fetch-confirmed against `origin/worker/13-guided-observation`, in a fresh detached
checkout. Baseline: `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba`;
plan: `7f4553587263772d9539e571c04abb18207704bf`; clarification:
`b90a1eaf8e7aaf2ec3796d24b4c730a7ea83024d`.

## Findings and verdict

**BLOCKER — unknown forge observations earn completeness.**
`tools/observed_input.py:294-296` checks only top-level null unit values.
Starting with this collector's complete custom output, add
`attacker.forge = {"might": null}`. Run `python3 tools/observed_input.py --edit`
with that explicitly selected synthetic draft; enter 27 deliberate `keep`
answers followed by `yes`. Exit 0 preserves the unknown forge but emits
`observed_inputs_complete: true`. A retained `forge: "?"` also reproduces it.
The diagnostic remains UNKNOWN: “Supply forged might/hit/crit as a full weapon
object; forge offsets are ambiguous”; no numeric result leaks. Nevertheless,
the confirmation flag violates the explicit incomplete-input contract, exactly
as the previously corrected unknown-range case did. Preserve these observations
with completeness false or refuse their incompatible shape; add public CLI
regressions without removing real forge/effect data.

**NOTE — burden count disagrees with measured output.**
`docs/guided-observation.md:68`, the summary and workflow footer say catalog
entry uses 29 answers. Independent supported two-catalog entry uses 27;
`corrected-workflows.log:161` agrees. Correct the prose/footer.

Verdict: **CHANGES REQUIRED**. Other bounded entry, preservation and refusal
goals passed; truthful completeness is not met.

## Independent evidence

Before production/new tests/Worker conclusions, privately specified complete
and incomplete duels from baseline schemas/policy: symmetric 30 HP, 12 strength,
5-might swords yield damage 9, displayed hit 87 and no modeled death. Review
order: expectations, production, independent public CLI, new tests, Worker
narrative. Existing public gate/full assessment equality and hand-derived values
agree. Shared engines, canonical data and research have no baseline diff.

| Command/control at reviewed delivery | Actual output/result | Exit |
|---|---|---:|
| `make audit` | All three audits pass; 179 tests OK | 0 |
| `python3 tools/fw.py check` | 0 errors, 0 warnings | 0 |
| `gh run list --branch worker/13-guided-observation --limit 3 --json headSha,status,conclusion,url,name` | Exact reviewed SHA: CI completed/success, run 38225177698 | 0 |
| `python3 -m unittest discover -s tests -p test_observed_input.py -v` | 13 tests OK | 0 |
| `git diff --check 5c596d42adb3d2a5eeee460032ee20bdd4bb78ba HEAD` | Empty | 0 |
| Independent private public-CLI runner | 30 controls pass; unknown forge failures above reproduced separately | 0 |
| Existing `tools/tactical_combat.py` public CLI | Exact complete assessment equality | 0 |
| Private headless Markdown render/link check | Reference/summary/attempts readable; 8 links resolve; zero overflow | 0 |

Controls covered partial/blank stats, integer retries, raw basis, Counter/drain,
forge values, unarmed/paired, explicit context null, keep/reconfirmation,
extra effects, duplicate/run-shaped sources, cancel/EOF and create-only output,
overwrite/traversal/symlink/run-name refusals. UNKNOWN diagnostics expose no
partial numbers. Synthetic drafts/existing outputs stayed unchanged. Privately
verified canonical/research/private file sets and contents unchanged in primary
and review checkouts; no private values/hashes published. Custom entry: 41
answers, 16 stats in two groups, zero manual JSON edits. Catalog: 27 answers.

No new mechanics, coverage, gameplay facts, human usability, native Windows or
whole-map safety were verified. Combined Batch14/Brain acceptance remains pending.
Exploratory nonexistent baseline filenames failed before file search found the
actual schema; they changed nothing. Only this review is changed; no implementation
or merge performed.

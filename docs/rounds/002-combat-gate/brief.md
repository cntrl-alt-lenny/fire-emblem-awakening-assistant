# 002-combat-gate: Require known weapon properties and expose certain death

Tier: 2
Mode: implementation
Supersedes: none

## Goal

The Hard/Classic live-combat wrapper must refuse unknown material weapon
properties and distinguish certain death from possible death for either
combatant, while preserving existing supported numerical results and the
conditional single-duel scope.

## Context

Read the project rules, full tactical policy, role card, `docs/state.md`,
`tools/tactical_combat.py`, the relevant preparation/forecast paths in
`tools/combat_calculator.py`, `tests/test_hard.py`, the combat input examples,
and the relevant sections of `docs/usage.md` and `docs/combat-formulas.md`.
Inspect canonical weapon records only as needed to establish the existing
input contract; this round does not certify those records' external truth.

Round 001's accepted audit independently demonstrated two inherited defects:
omitting a custom weapon's `effect` still yields an outcome because the
calculator defaults it to absence; a duel with defender death probability
1.0 is labeled `POTENTIALLY_LETHAL`. Exact reproductions and Brain's decision
are in `docs/rounds/001-foundation-audit/attachments/brain-review.md`.
Weapon `brave` and `effectiveness` also have defaults and need assessment in
this same completeness boundary. The completeness assertion at the payload
level does not supply a missing field's value.

This brief follows the accepted audit, rather than superseding it. Its branch
contains the delivered audit unchanged plus Brain's review; the audit's merge
remains a separate owner decision. Do not merge either round. The demonstrated
live-tool defect takes priority over the inherited Chapter 5/17 research
conflicts; those conflicts remain pending.

Verifier: complete your independent first pass before opening this round's
Worker report. Read the delivered diff and independently reconstruct the
failure paths, then compare the report. Prior-round audit findings are context,
not proof that the new implementation works.

## Scope and non-goals

Allowed: the strict live wrapper, narrowly necessary shared validation,
focused regressions, existing input examples and user-facing input/risk
documentation. Preserve the general calculator's documented compatibility
unless a necessary change is explicitly explained and covered. Update
`STATUS.md` only for changed capability/limitations or current validation
counts; no new verified gameplay coverage is earned by these regressions.

Do not change canonical data, rebuild scripts, map queries, proc mechanics,
paired outcomes, run trackers, framework files, CI, repository settings or
licensing. Do not initialize a run, research the campaign, add Windows
support, or expand supported mechanics. Report adjacent findings separately
instead of silently enlarging this task.

## Invariants

- `AGENTS.md` and tactical policy: missing/null values remain unknown;
  unsupported skills/effects and incomplete support must never be discarded.
- Tactical policy: effective displayed stats include active bonuses exactly
  once; Pair Up, equipped stat bonuses and innate weaknesses retain their
  existing meanings. Canonical lookup does not establish weapon eligibility.
- Tactical policy: `LETHAL` means certain death, `POTENTIALLY_LETHAL` means
  possible death. Neither no modeled death nor a complete duel proves map
  safety. Keep both sides' probabilities and worst HP available.
- `AGENTS.md`: offline use/build, Python 3.9+, standard library only; preserve
  canonical data, other difficulty modes, player state and event/history.
- Framework: Worker implements, blind Verifier reviews one exact commit,
  Brain independently re-derives; only Brain may merge after owner approval.

## Acceptance criteria

1. On both combatants, custom/forged weapon objects cannot silently default
   missing material `effect`, `brave` or `effectiveness` to absence. Missing,
   null or malformed values produce `UNKNOWN`, no full outcome, and a useful
   diagnostic identifying the combatant/property. Explicit known absence is
   documented and supported. Do not treat empty/unknown effect text as proof
   of absence. Establish and document valid unequipped-defender handling;
   preserve explicitly known absence without inventing a weapon.
2. Canonical weapon IDs remain usable when lookup supplies the required known
   properties. Unknown IDs or incomplete resolved properties refuse safely.
   Fully specified supported custom weapons and actual forged might/hit/crit
   remain supported; ambiguous forge markers/offsets and unsupported canonical
   or custom effects still refuse. Contradictory effect/behavior fields must
   not silently remove a material effect; refuse or document a justified
   existing normalization without introducing new mechanics.
3. Top-level risk distinguishes certain death (`LETHAL`) for either side,
   non-certain positive risk (`POTENTIALLY_LETHAL`), and zero modeled risk
   (`NO_MODELED_DEATH_IN_THIS_DUEL`). Identify which side is at risk so a
   certain enemy defeat cannot be mistaken for certain player death. Keep
   both probabilities, minimum HP and conditional map-safety refusal. Do not
   round a probability below one up to certain death.
4. Complete supported inputs retain their forecasts and outcome numbers.
   Where old fixtures relied on omitted properties, supply explicit known
   values and compare numbers using that complete input at the old and new
   commits. No numerical mechanics change is authorized by a label change.
5. Focused regression evidence covers each side independently, omission,
   null, invalid and explicit absence values, canonical/custom/forged paths,
   certain attacker death, certain defender death, possible death and no
   modeled death. Include continued refusals for missing/null support,
   adjacent/paired outcomes, drain, Counter, Dragonskin, unresolved procs and
   durability breakage. Exercise the public CLI as well as function inputs.
   Demonstrate that the key new omission/certainty regressions fail against
   the pre-fix implementation for the intended reason, then pass at delivery.
6. Input examples/documentation agree with the gate and explain the certainty
   labels, explicit absence and canonical/custom weapon distinction. Resolve
   changed local links and inspect the rendered Markdown. Tests and input
   contract repairs do not certify new gameplay facts or complete schedules.
7. Required audits/hygiene pass at the reported exact implementation commit.
   Canonical JSON, `CURRENT_RUN.md` and every existing state file remain
   byte-identical, with file-set comparison detecting additions/deletions.
   Tests use temporary state; no live-run mutation. Record absence honestly
   when no live run exists, rather than claiming a live preservation test.

## Required evidence

Paste real commands, relevant output and exit status, full reviewed commit,
OS/Python version and the focused inputs/results. Required commands:

```sh
make audit
python3 tools/fw.py check
python3 -m unittest discover -s tests -v
git diff --check
```

Also record the focused regression command, baseline-failure demonstration,
old/new numerical comparison, representative
`python3 tools/tactical_combat.py TEMP_INPUT.json` outputs, and the SHA-256
snapshot/file-set comparison script and results. Do not write battle inputs
to a live run. If make is unavailable, use the audit command equivalents
listed in `AGENTS.md` and report their exit statuses separately. Canonical or
rebuild changes are out of scope: stop and report any necessity for them.

No external mechanics change is planned. Any new external factual assertion
requires independently scoped evidence with difficulty/phase/version and
remaining uncertainty; tests alone cannot establish it.

Finish with the framework-stamped report and push even on an early exit:
`python3 tools/fw.py report --role worker --round 002-combat-gate --push`
(Verifier substitutes `--role verifier`). Neither seat merges.

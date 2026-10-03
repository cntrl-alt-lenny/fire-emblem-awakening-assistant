# 005-chapter17-provenance: Audit Chapter 17 inventory provenance

Tier: 2
Mode: data
Supersedes: none

## Goal

Establish what evidence supports each stored Hard Chapter 17 reinforcement
inventory, and correct attribution, counts or confidence where justified.
The reviewed inputs and offline regeneration must preserve the resulting
claims. An unresolved inventory remains explicitly uncertain; this round
does not resolve the actual staircase or warning-to-arrival schedule.

## Context

Read the project rules, full tactical policy, your role card, `docs/state.md`,
`STATUS.md`, `SOURCES.md`, `research/UNCERTAINTIES.md`,
`docs/hard-reinforcements.md` and `docs/map-coverage.md`.
Inspect Chapter 17 in `research/hard_verification/author_review.py`,
`reviewed.json`, `additional_sources.json`,
`data/chapters/hard_reinforcements.json`, `hard_tactics.json` and
`data/sources.json`. Trace generation through `tools/hard_data.py` and the
`make rebuild` pipeline; inspect `tools/map_info.py` and relevant tests as
needed to understand consumers. Use Git history to trace inherited values.

The three stored inventories total four, four and six units. Their unit
claims currently credit `hr_fandom17`, `p2_guide_16_2` and `hr_jp_17` together.
These are claims to investigate, not facts to endorse. Generic construction
and later note rewriting may obscure field-specific evidence.

Start with those registry URLs. `p2_survey_16_2` shares a publisher/URL with
the guide and is not independent corroboration. Distinguish an initial enemy
table from reinforcement inventory, local difficulty headings from guide-wide
defaults, and dated comments from editorial tables. Later rows whose mode
boundary was lost remain excluded.

Round 004 is accepted bounded research, not a gameplay resolution. Its
[Brain review](../004-chapter17-research/attachments/brain-review.md) records
the outstanding inventory/provenance questions. The source matrix and
reports are comparison material after the Verifier's blind source pass.
Neither inability to reproduce a six-unit entry nor an inaccessible page
alone proves the actual central wave has a different number of units.

## Scope and non-goals

Audit and, where supported, amend the three Chapter 17 inventory claims and
their claim-level attribution, confidence and limitations. Preserve unresolved
alternatives and distinguish source-reported composition from an observed
gameplay inventory. Correct related source scope descriptions only where
needed to avoid misrepresenting those inventories.

Allowed changes: targeted reviewed inputs and their authoring code, generated
Chapter 17 Hard inventory/provenance fields, targeted source registry entries,
meaningful regressions, this round's research/report attachments, and affected
source/uncertainty/coverage documentation. Update `STATUS.md` and coverage
counters if coverage changes. Modify the rebuild producer only as needed to
keep the narrow amendment reproducible. Prefer existing claim structures;
no general evidence-schema redesign or tactical-tool feature work.

Keep all other chapters and difficulties, Chapter 17 timing/location/phase
claims and conflict, and quarantine unchanged. A changed source list may
propagate to a containing record, but must not erase sources still supporting
its other claims. Unrelated regeneration drift is not authorized data adoption:
identify and resolve it within scope or report the limitation.

No new playthrough, run initialization, footage acquisition, game-file
extraction, complete roster/schedule research, combat/mechanics change,
framework/CI/license/settings change, or new gameplay safety guarantee.
Do not repeat the broad footage search from round 004. Bound external lookup
to the existing source contexts and directly relevant provenance leads.

## Invariants

- `AGENTS.md` and tactical policy: Hard and other modes stay separate; null,
  empty and missing remain unknown. Preserve claim-level sources, conflict,
  source families and quarantine. No complete schedule or map safety claim.
- Tactical policy: initial activation is not a reinforcement trigger by
  association. General Hard immediate action does not observe this event's
  phase. Reported turns 8/9/10 remain conditional, not certified fixed turns.
- Tactical policy: no access-control bypass, bulk crawl, full-guide archive,
  downloaded footage or game assets. A search excerpt belongs to its source
  family; unavailable context is neither agreement nor contrary evidence.
- `AGENTS.md`: tests establish repository behavior, not external game facts.
  State exact difficulty, phase, region/version where known, and separate
  source wording, translation, inference and observation. Language/date alone
  do not establish region/version. Do not silently discard disputed evidence.
- `AGENTS.md`: actual player reports and local run state are authoritative.
  Tests use temporary states. Preserve `CURRENT_RUN.md` and all `state/`
  files, including their event/history ledger; no player contents or hashes
  enter public artifacts.
- Framework: Worker implements; Verifier independently reviews one exact
  commit after a blind source pass; Brain re-derives and judges. Neither seat
  merges. Build and use remain offline, Python 3.9+, standard library only.

## Acceptance criteria

1. Trace each inventory's class/count/equipment attributes from canonical
   records through reviewed inputs, authoring code and relevant Git history.
   Identify the earliest recoverable basis of the central six-unit value,
   without treating a historical literal as external proof. Provide exact
   file/field or commit locators and a concise account of any missing origin.
2. Independently inspect accessible original contexts for all three source
   families. Build a field-level matrix for the three inventories: short
   factual observation, URL/section or dated-comment locator, retrieval date,
   difficulty/phase/version scope, source family, supplied attributes,
   confidence, conflicts and unknowns. State exactly which inventory portions
   each source supports; partial overlap cannot corroborate every attribute.
3. Make a justified disposition for each existing claim: retain, narrow,
   correct, downgrade or leave explicitly unresolved. Explain source report
   versus actual gameplay certainty. Do not select a replacement count merely
   because it is the only currently accessible one. Preserve an unsupported
   inherited alternative as such where needed to explain the discrepancy;
   do not leave it presented as supported or silently erase the evidence gap.
4. Ensure the offline producer and reviewed inputs agree on the amendment,
   including field-specific notes/confidence. Regeneration must not restore
   broad attribution or unsupported values. Add meaningful regression
   coverage for the failure addressed; explain what could fail before the
   change. Structural assertions alone do not validate the game inventory.
5. Preserve Chapter 17's staircase/timing conflict, unknown spawn phase,
   conditional turn reports and incomplete schedule. Inspect current-map CLI
   output for affected units and preserved warnings. Keep the Chapter 5
   conflict and all unrelated Hard records unchanged. Make no new verified
   gameplay coverage claim unless the evidence actually meets project policy.
6. Prove deterministic canonical output across two complete `make rebuild`
   runs using file-set and SHA-256 comparisons. Compare against the brief's
   base by record/field to prove all other chapters, other-mode records
   (including mixed-mode JSON) and quarantine were preserved. Account for
   every changed canonical field. Separately prove private run file-set/content
   preservation, reporting only counts/results and whether a live run exists.
7. Verifier records an independent blind pass before opening Worker results
   or round 004 conclusions: inspect source contexts and baseline data/code,
   seek contrary or insufficient evidence, and record findings. Then inspect
   the exact Worker commit, reproduce the claim dispositions, regressions,
   two rebuilds and preservation comparisons independently. Report unavailable
   context and unproven claims explicitly; do not implement corrections.
8. Render changed documentation, resolve changed local links, and summarize
   what this round establishes and leaves unresolved. Recommend exactly one
   bounded next task based on the result, with any unavailable input stated.

## Required evidence

At the reported full commit, paste OS/Python version, actual commands,
relevant output and exit statuses:

```sh
make audit
make rebuild
make audit
make rebuild
make audit
python3 tools/fw.py check
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase player
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase enemy
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 9 --phase player
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 10 --phase player
git diff --check
```

Record the comparison commands and results required above, including canonical
hash equality after both rebuilds, exact approved differences from the base,
other-mode/unrelated-map/quarantine preservation and private run preservation.
Run meaningful new regressions and show the relevant pre-change failure if
feasible. If make is unavailable, use all audit equivalents from `AGENTS.md`
and every rebuild pipeline command from `Makefile`; record exit statuses.

External evidence needs precise source locators, short compliant observations,
scope, translations/inferences and limitations. Repository checks and CLI
output cannot establish actual game composition, timing or full-map safety.
Do not retry definitely denied access or collect unrelated guide content.

Commit artifacts before producing the stamped report. Push even on an early
exit: `python3 tools/fw.py report --role worker --round 005-chapter17-provenance --push`
(Verifier substitutes `--role verifier`). Neither seat merges.

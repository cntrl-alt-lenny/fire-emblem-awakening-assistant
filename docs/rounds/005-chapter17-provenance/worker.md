<!-- fw-report
round: 005-chapter17-provenance
role: worker
branch: worker/005-chapter17-provenance
head: 4409b66f1b7a79b0715bf4b660fa87af831b853d
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T19:42:22Z
-->
## Verified

Reviewed implementation/artifact commit: `4409b66f1b7a79b0715bf4b660fa87af831b853d`.
Base: `a97ee2d8a528d7f8fef62b06978a3c3861599e69`.

- History traced through canonical records, reviewed inputs and the author. Earliest recoverable central six-unit literal is root commit `cf17834fd6a8867d06c25faa772a5d8700f32167`; no external basis was recovered. Exact locators and independently reinspected source contexts are recorded in `attachments/inventory-audit.md`. Source reports do not establish actual gameplay composition.
- Meaningful regressions before the production change: `python3 -m unittest discover -s tests -p test_chapter17_provenance.py -v` → exit 1, `Ran 3 tests`, `FAILED (failures=6)`. Broad attribution, a promoted central inventory and fresh-author attribution each failed; four query phase subcases failed. Real failure output, with personal paths removed, is in `attachments/prechange-regressions.log`. The initial temporary test fixture was corrected to include its legacy reinforcement input before this recorded run.
- All required checks below ran at the reviewed full commit through `python3 docs/rounds/005-chapter17-provenance/attachments/verify-commit.py /tmp/fea-worker005-before-private.json` → exit 0. It computes every canonical file's SHA-256 after each complete rebuild and requires identical file sets and hashes. The private baseline stays outside Git; no player contents or run hashes appear here.
- The strict base comparison accounts for exactly 12 canonical fields. Everything else is unchanged, including all mixed-mode JSON, Chapter 5 conflict, other Hard chapters, quarantine, and Chapter 17 non-unit fields/conflict. Reviewed inputs outside the approved inventory/source fields also match the base. Private preservation covers two files; no live run exists in this worktree.
- Rendered `SOURCES.md`, `STATUS.md`, `docs/hard-reinforcements.md`, `research/UNCERTAINTIES.md` and the inventory audit with the installed marked renderer; inspected the local browser output. Table/paragraph presentation was readable. All three relative links resolved. The report was separately rendered and inspected before stamping. These checks establish presentation, not external fact accuracy.

Actual command/output evidence follows. Make output is excerpted; exit statuses apply to whole commands. Only repeated CLI inventory JSON is omitted after the first query.

```text
$ git rev-parse HEAD
exit 0
4409b66f1b7a79b0715bf4b660fa87af831b853d
$ uname -s -r
exit 0
Darwin 27.0.0
$ sw_vers -productVersion
exit 0
27.0
$ python3 --version
exit 0
Python 3.9.6
$ make audit
exit 0
python3 tools/validate_data.py
{
  "passed": true,
  "counts": {
[relevant output excerpt]

----------------------------------------------------------------------
Ran 118 tests in 0.717s

OK
$ make rebuild
exit 0
python3 tools/build_data.py
{
  "classes": 55,
  "characters": 49,
[relevant output excerpt]
  "registered_sources": 217,
  "source_refs_resolve": true,
  "source_truth_not_proven_by_tests": true,
  "readiness_requires": "Evidence-aware claims, no unconditional route-safety advice, complete observed inputs and refusal for unsupported interactions."
}
$ make audit
exit 0
python3 tools/validate_data.py
{
  "passed": true,
  "counts": {
[relevant output excerpt]

----------------------------------------------------------------------
Ran 118 tests in 0.697s

OK
$ make rebuild
exit 0
python3 tools/build_data.py
{
  "classes": 55,
  "characters": 49,
[relevant output excerpt]
  "registered_sources": 217,
  "source_refs_resolve": true,
  "source_truth_not_proven_by_tests": true,
  "readiness_requires": "Evidence-aware claims, no unconditional route-safety advice, complete observed inputs and refusal for unsupported interactions."
}
$ make audit
exit 0
python3 tools/validate_data.py
{
  "passed": true,
  "counts": {
[relevant output excerpt]

----------------------------------------------------------------------
Ran 118 tests in 0.707s

OK
Two complete rebuilds: file sets and every SHA-256 equal; 28 canonical JSON files
Canonical manifest SHA-256: 44cb0c0444d2ef40718b65659cb63ce590a5bf4950cdc31ff7b4c9ce15a11529
$ python3 tools/fw.py check
exit 0
0 error(s), 0 warning(s)
$ python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase player
exit 0
{
  "chapter_id": "chapter_17",
  "difficulty": "Hard",
  "mode": "Classic",
  "current_turn": 8,
  "current_phase": "player",
  "target_enemy_phase_turn": 8,
  "map_confidence": "CONFLICTED",
  "schedule_complete": false,
  "safe_to_claim_move_safe": false,
  "safe_to_conclude_no_reinforcements": false,
  "warning": "Known facts are source-supported, not a complete threat map. Hard beginning-enemy-phase spawns can move/attack immediately. Never rely on enemy-phasing an unknown wave."
}
Candidate inventory claims:
{
  "hard_chapter_17_first": {
    "value": [
      {
        "count": 2,
        "class_id": "hero",
        "equipment": [
          "silver_sword"
        ],
        "level": null,
        "location": null
      },
      {
        "count": 1,
        "class_id": "war_monk",
        "equipment": [
          "silver_axe"
        ],
        "level": null,
        "location": null
      },
      {
        "count": 1,
        "class_id": "sniper",
        "equipment": [
          "silver_bow"
        ],
        "level": null,
        "location": null
      }
    ],
    "confidence": "SUPPORTED",
    "source_ids": [
      "hr_fandom17"
    ],
    "notes": "Reported class/count/equipment only: single-source indexed Hard reinforcement turn-8 row (hr_fandom17, accessed 2026-10-03); not independently observed gameplay. Gamer Guides lists no inventory. The Hard-labelled Pegasus 2012-04-27 comment reports four arrivals including a Sniper, but supplies neither all class counts nor equipment and does not identify a table wave unambiguously. Classic/Casual, region/version and event phase are unspecified. Null level/location and unlisted skills/forges remain UNKNOWN. Timing/location conflict and incomplete schedule remain unchanged."
  },
  "hard_chapter_17_second": {
    "value": [
      {
        "count": 2,
        "class_id": "hero",
        "equipment": [
          "silver_sword"
        ],
        "level": null,
        "location": null
      },
      {
        "count": 1,
        "class_id": "sniper",
        "equipment": [
          "silver_bow"
        ],
        "level": null,
        "location": null
      },
      {
        "count": 1,
        "class_id": "war_monk",
        "equipment": [
          "silver_axe"
        ],
        "level": null,
        "location": null
      }
    ],
    "confidence": "SUPPORTED",
    "source_ids": [
      "hr_fandom17"
    ],
    "notes": "Reported class/count/equipment only: single-source indexed Hard reinforcement turn-9 row (hr_fandom17, accessed 2026-10-03); not independently observed gameplay. Gamer Guides lists no inventory. The Hard-labelled Pegasus 2012-04-27 comment reports four arrivals including a Sniper, but supplies neither all class counts nor equipment and does not identify a table wave unambiguously. Classic/Casual, region/version and event phase are unspecified. Null level/location and unlisted skills/forges remain UNKNOWN. Timing/location conflict and incomplete schedule remain unchanged."
  },
  "hard_chapter_17_central": {
    "value": null,
    "confidence": "CONFLICTED",
    "source_ids": [
      "hr_fandom17"
    ],
    "notes": "Inherited six-unit alternative: 3 Heroes with Silver Sword, 2 War Monks with Silver Axe, 1 Sniper with Silver Bow; earliest recoverable literal is cf17834fd6a8867d06c25faa772a5d8700f32167 author_review.py, with no recoverable external basis. Accessible indexed two-unit alternative: 1 War Monk with Silver Axe and 1 Hero with Silver Sword (Hard reinforcement turn-10 row, accessed 2026-10-03). Neither alternative is selected as actual gameplay; null inventory is UNKNOWN, not zero. hr_fandom17 supports only the indexed alternative. Gamer Guides supplies no inventory; the Hard-labelled Pegasus comment does not enumerate central classes/counts/equipment. Classic/Casual, region/version and this event phase remain unestablished. No complete schedule or safety guarantee."
  }
}
Inspected: all three remain conditional candidates; phase UNKNOWN; central inventory excluded from known claims
$ python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase enemy
exit 0
{
  "chapter_id": "chapter_17",
  "difficulty": "Hard",
  "mode": "Classic",
  "current_turn": 8,
  "current_phase": "enemy",
  "target_enemy_phase_turn": 9,
  "map_confidence": "CONFLICTED",
  "schedule_complete": false,
  "safe_to_claim_move_safe": false,
  "safe_to_conclude_no_reinforcements": false,
  "warning": "Known facts are source-supported, not a complete threat map. Hard beginning-enemy-phase spawns can move/attack immediately. Never rely on enemy-phasing an unknown wave."
}
Candidate inventory claims:
[Repeated inventory JSON omitted; inspected at this phase as recorded below.]
Inspected: all three remain conditional candidates; phase UNKNOWN; central inventory excluded from known claims
$ python3 tools/map_info.py --chapter 17 --difficulty hard --turn 9 --phase player
exit 0
{
  "chapter_id": "chapter_17",
  "difficulty": "Hard",
  "mode": "Classic",
  "current_turn": 9,
  "current_phase": "player",
  "target_enemy_phase_turn": 9,
  "map_confidence": "CONFLICTED",
  "schedule_complete": false,
  "safe_to_claim_move_safe": false,
  "safe_to_conclude_no_reinforcements": false,
  "warning": "Known facts are source-supported, not a complete threat map. Hard beginning-enemy-phase spawns can move/attack immediately. Never rely on enemy-phasing an unknown wave."
}
Candidate inventory claims:
[Repeated inventory JSON omitted; inspected at this phase as recorded below.]
Inspected: all three remain conditional candidates; phase UNKNOWN; central inventory excluded from known claims
$ python3 tools/map_info.py --chapter 17 --difficulty hard --turn 10 --phase player
exit 0
{
  "chapter_id": "chapter_17",
  "difficulty": "Hard",
  "mode": "Classic",
  "current_turn": 10,
  "current_phase": "player",
  "target_enemy_phase_turn": 10,
  "map_confidence": "CONFLICTED",
  "schedule_complete": false,
  "safe_to_claim_move_safe": false,
  "safe_to_conclude_no_reinforcements": false,
  "warning": "Known facts are source-supported, not a complete threat map. Hard beginning-enemy-phase spawns can move/attack immediately. Never rely on enemy-phasing an unknown wave."
}
Candidate inventory claims:
[Repeated inventory JSON omitted; inspected at this phase as recorded below.]
Inspected: all three remain conditional candidates; phase UNKNOWN; central inventory excluded from known claims
$ git diff --check
exit 0
(no output)
$ python3 docs/rounds/005-chapter17-provenance/attachments/compare-preservation.py /tmp/fea-worker005-before-private.json
exit 0
Canonical file set: 28 unchanged
Exactly 12 approved canonical field changes:
data/chapters/hard_reinforcements.json/records/hard_chapter_17_first/units/source_ids
data/chapters/hard_reinforcements.json/records/hard_chapter_17_first/units/notes
data/chapters/hard_reinforcements.json/records/hard_chapter_17_second/units/source_ids
data/chapters/hard_reinforcements.json/records/hard_chapter_17_second/units/notes
data/chapters/hard_reinforcements.json/records/hard_chapter_17_central/units/value
data/chapters/hard_reinforcements.json/records/hard_chapter_17_central/units/confidence
data/chapters/hard_reinforcements.json/records/hard_chapter_17_central/units/source_ids
data/chapters/hard_reinforcements.json/records/hard_chapter_17_central/units/notes
data/sources.json/hr_jp_17/accessed
data/sources.json/hr_jp_17/limitations
data/sources.json/hr_fandom17/limitations
data/sources.json/hr_fandom17/accessed
Other chapters/modes, mixed-mode JSON, Chapter 17 non-unit claims/conflict, Hard tactics and quarantine: unchanged
Reviewed inputs outside approved inventory/source fields: unchanged
Private run file set/content preserved: 2 files; live run exists: False
$ python3 -m unittest discover -s tests -p test_chapter17_provenance.py -v
exit 0
test_fresh_authoring_preserves_inventory_notes_and_claims (test_chapter17_provenance.Chapter17ProvenanceTests) ... ok
test_inventory_attribution_and_unresolved_central (test_chapter17_provenance.Chapter17ProvenanceTests) ... ok
test_query_does_not_promote_central_inventory (test_chapter17_provenance.Chapter17ProvenanceTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.062s

OK
$ git status --short
exit 0
(no output)
```

## Not verified

Actual central wave composition remains unobserved. Fandom's complete direct page was unavailable; only the Hard-labelled indexed subsection was accessible. No access bypass or repeat of denied access occurred. No game-derived event evidence, new footage, independent inventory corroboration, regional equivalence, Classic/Casual-specific source identification, actual spawn phase, trigger boundary, complete schedule or whole-map safety is certified. Repository tests cannot prove those facts. Blind Verifier review and Brain judgment remain separate future steps; no merge was performed.

## Changed

- `research/hard_verification/author_review.py`, `reviewed.json`: first/second inventories retain four source-reported units with only Fandom attribution and precise limits. Central inventory becomes null/CONFLICTED, preserving inherited six-unit and indexed two-unit alternatives in notes. Targeted assignments follow generic note rewriting.
- `research/hard_verification/additional_sources.json`, `data/sources.json`, `SOURCES.md`: only Chapter 17 Fandom/Pegasus access dates and relevant inventory/region limitations change; source-document introduction distinguishes original and current retrieval dates.
- `data/chapters/hard_reinforcements.json`: exactly eight unit-claim field changes, with all other wave fields and containing sources preserved. `hard_tactics.json` is unchanged.
- `tools/hard_data.py`: source-document date introduction only; claim generation behavior already preserves the reviewed amendment.
- `tests/test_chapter17_provenance.py`: attribution, central query uncertainty at all four requested phase queries, and isolated fresh authoring regression coverage. Tests do not change a live run.
- `STATUS.md`, `research/UNCERTAINTIES.md`, `docs/hard-reinforcements.md`: expose the inventory gap and field-specific attribution; correct the nearby language/date inference. Existing 44-map/29-wave confidence counters and zero complete verified schedules are unchanged; no new gameplay coverage.
- This round's report and `attachments/`: field matrix, lineage/dispositions, pre-change failures, strict preservation comparison and reproducible full-commit validation driver.
- `docs/state.md` unchanged.

## Open questions

The six-unit literal's external origin is missing. The accessible two-unit report is a competing alternative, not a selected correction to actual gameplay. First/second source-reported inventories remain single-source; no exact inventory is independently observed. Existing staircase and warning-to-arrival conflict remains unchanged.

Exactly one bounded next task: review one lawful, clearly Hard-labelled observation of the central Chapter 17 arrival with visible inventory/equipment, warning/setup, phase, region/version and Classic/Casual where available; compare both alternatives without assuming a fixed turn. That observation is unavailable in this round.

<!-- fw-report
round: 005-chapter17-provenance
role: verifier
branch: verifier/005-chapter17-provenance
head: d05818683e32cb3c497517badb28d85d42292275
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T19:54:01Z
-->
Reviewed commit: `d05818683e32cb3c497517badb28d85d42292275`.
Worker implementation/artifact commit: `4409b66f1b7a79b0715bf4b660fa87af831b853d`.
Brief base: `a97ee2d8a528d7f8fef62b06978a3c3861599e69`.
Environment: `Darwin 27.0.0`, macOS `27.0`, `Python 3.9.6`.

## Findings

None. No BLOCKER or SHOULD FIX finding, and no correction was implemented.
Actual inventory uncertainty is retained rather than resolved by source access.

## Independent source and lineage review

I inspected baseline records, authoring code, producer and original source
contexts before opening Worker results or Round 004 conclusions. Blind findings
were recorded in a private temporary note before pass two. Earlier conversation
history contains Round 004 review, so this is not a fresh agent with no prior
exposure; the Round 005 source retrieval and baseline derivation below were
performed independently, without opening that round's conclusions.

At the brief base, the three canonical `units` claims contain totals four,
four and six, all SUPPORTED and collectively attributed to
`hr_fandom17`, `p2_guide_16_2`, `hr_jp_17`. `tools/hard_data.py:main` copies
reviewed waves directly; `make rebuild` consumes `reviewed.json` without
executing the author. The author constructs the literal groups via `u()`,
credits the same sources through `w()`, then overwrites their notes in its
generic final loop. This explains the repository attribution, not its factual
basis.

Commands `git log --follow --format='%H %s' --` for both
`research/hard_verification/author_review.py` and `reviewed.json`,
`git rev-list --max-parents=0 HEAD`, and
`git show cf17834:research/hard_verification/author_review.py` reproduce the
lineage: root commit `cf17834fd6a8867d06c25faa772a5d8700f32167`, author line 92,
already supplies central `u(3,'hero','silver_sword')`,
`u(2,'war_monk','silver_axe')`, `u(1,'sniper','silver_bow')`. The root reviewed
and canonical central records contain the same inventory. No preceding commit
exists. The old `research/phase2/guide_16.json`, `guide_16_2` record, contains
boss metadata and map facts; `reviewed_additions.json` supplies no Chapter 17
inventory. No external origin for the six-unit literal was recovered, and no
transcription/mode-conflation explanation is asserted.

All original contexts below were independently retrieved on `2026-10-03`.
They establish source reports only. Classic/Casual and region/version remain
unestablished; language and publication date do not prove a regional version.

- Fandom family, `hr_fandom17`:
  `https://fireemblem.fandom.com/wiki/Inexorable_Death`.
  Direct reader returned a restricted-URL error. The bounded query
  `site:fireemblem.fandom.com/wiki/Inexorable_Death "Hard Mode" "Turn 8"`
  retrieved indexed `Reinforcements / Hard Mode` context and reported a robots
  restriction. No denied direct access was retried. Turn 8 enumerates two Heroes
  with Silver Sword, one War Monk with Silver Axe and one Sniper with Silver
  Bow; turn 9 supplies the same composition. Each entry has level 3 in the
  index, but adoption of levels is outside this amendment. Turn 10 enumerates
  one War Monk/Silver Axe and one Hero/Silver Sword. The introductory wording
  assigns enemy-turn beginning; turn 8 describes initially allied units and
  conversion. This is not observation of the scripted event. The warning
  sentence is truncated. A later Lunatic heading is visible in this retrieval,
  but later rows remain excluded. The index is one editorial source family,
  not a new corroboration or a reproduction of the current direct revision.
- Guide family, `p2_guide_16_2` / `p2_survey_16_2`:
  `https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-17-inexorable-death`.
  Direct reader; exact local heading `Strategies for all Difficulties`, final
  paragraph mentioning Say'ri. It reports warning, eastern-most stairs and
  subsequent other stairs, with no class/count/equipment inventory. Both IDs
  share one URL/publisher. Guide-wide Hard defaults cannot turn this paragraph
  into independent Hard inventory support.
- Japanese comment family, `hr_jp_17`:
  `https://www.pegasusknight.com/wiki/fe13/マップ攻略/章別攻略/17章+死の運命`.
  Direct reader; anonymous comment `2012-04-27 11:57:31`, explicitly Hard.
  My translation: approximately three turns after Say'ri announces arrivals,
  four units emerge from four left stairs, including a Sniper. This supplies
  partial total/class overlap, without complete class counts, equipment, event
  phase or explicit wave ordinal. The initial-placement section is not a
  Hard reinforcement inventory. The `2014-09-06 12:10:14` Hard comment concerns
  initial upper-group activation and possible stair blocking, not composition.
  The neighboring `2014-02-09 03:49:41` sequence is difficulty-unlabelled and
  cannot supply Hard counts. These are insufficient/contrary contexts, not
  omitted corroboration of the inherited central group.

Blind findings therefore supported narrowing first/second attribution, while
leaving central composition unknown with both historical and indexed alternatives
visible. I did not repeat a broad footage search, acquire game assets or use
unavailable material as agreement.

## Comparison and acceptance criteria

After recording the blind pass, I read the complete Worker report, inventory
matrix, regression log, comparison helper and commit-validation helper, and
inspected the exact production diff. The material source readings and
historical locators agree with the independent derivation above.

1. **Met:** recoverable lineage is explicit and historical literals are not
   presented as external proof.
2. **Met:** the field matrix scopes all three inventories by source, attribute,
   locator, retrieval date and limitations. G supplies no inventory; J supplies
   partial overlap only; index retrieval remains F's source family.
3. **Met:** first/second class/count/equipment values remain single-source
   SUPPORTED reports, credited only to F. Central `units.value` becomes null,
   `confidence` CONFLICTED; notes retain the unsupported six-unit alternative
   and indexed two-unit alternative. F is explicitly credited only for the
   latter. Neither is selected as actual gameplay. Null never means zero.
4. **Met:** targeted assignments occur after generic note rewriting, so fresh
   authoring retains them. Reviewed and canonical Chapter 17 waves compare
   equal. The producer needs no claim-generation feature change; its changed
   line describes source-document dates. Meaningful regressions catch broad
   attribution, central promotion in queries and fresh-author regression.
5. **Met:** all non-unit Chapter 17 fields, timing/location conflict, null
   fixed turns, reported turns 8/9/10, unknown phase, immediate-action caveats
   and incomplete schedule are unchanged. The consumer places central units
   in uncertain claims, outside known claims. Chapter 5 and other Hard records
   remain unchanged. No new verified gameplay coverage is claimed.
6. **Met:** two complete rebuilds reproduce identical canonical file sets and
   SHA-256 values. The strict recursive base comparison accounts for exactly
   12 field differences and no unrelated data adoption. Private preservation
   passes as described below.
7. **Met, with prior-exposure limitation stated above:** blind Round 005
   derivation precedes Worker-results inspection, followed by independent
   checks, regression failures and source-disposition comparison.
8. **Met:** five changed documents render readably; all three local links
   resolve. Exactly one bounded next task is proposed, contingent on unavailable
   observation input.

The real default-branch diff also carries inherited Round 004 Brain review
and a four-line parked Chapter 17 decision in `docs/state.md`. No sentence
was removed. Relative to the supplied brief base, standing decisions are
unchanged; the Worker's preservation statement has that scope.

## Commands and actual results

At the full reviewed commit, I ran
`python3 docs/rounds/005-chapter17-provenance/attachments/verify-commit.py`
with my private baseline argument. The complete successful run returned exit 0
and actually executed the following commands in order. Make output excerpts
are relevant output, not full logs; private full driver output was inspected.

```text
make audit
exit 0; Ran 118 tests in 2.384s; OK
make rebuild
exit 0; registered_sources: 217; source_refs_resolve: true;
source_truth_not_proven_by_tests: true
make audit
exit 0; Ran 118 tests in 1.633s; OK
make rebuild
exit 0; registered_sources: 217; source_refs_resolve: true;
source_truth_not_proven_by_tests: true
make audit
exit 0; Ran 118 tests in 0.728s; OK
Two complete rebuilds: file sets and every SHA-256 equal; 28 canonical JSON files
Canonical manifest SHA-256:
44cb0c0444d2ef40718b65659cb63ce590a5bf4950cdc31ff7b4c9ce15a11529
python3 tools/fw.py check
exit 0; 0 error(s), 0 warning(s)
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase player
exit 0; target_enemy_phase_turn: 8
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase enemy
exit 0; target_enemy_phase_turn: 9
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 9 --phase player
exit 0; target_enemy_phase_turn: 9
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 10 --phase player
exit 0; target_enemy_phase_turn: 10
git diff --check
exit 0; no output
```

All four CLI outputs contain `map_confidence: CONFLICTED`,
`schedule_complete: false`, `safe_to_claim_move_safe: false`,
`safe_to_conclude_no_reinforcements: false`, with all three conditional
candidates. Candidate first/second inventories retain four units and only
`hr_fandom17` attribution. Central candidate units are null/CONFLICTED with
both alternatives in notes, excluded from `known_verified_supported` and
included in `uncertain_partial_conflicted_unknown`. The warning remains:
`Known facts are source-supported, not a complete threat map. Hard beginning-enemy-phase spawns can move/attack immediately. Never rely on enemy-phasing an unknown wave.`
CLI fields show software behavior, not game composition or actual event phase.

`python3 docs/rounds/005-chapter17-provenance/attachments/compare-preservation.py`
with the private baseline argument returned exit 0. Its inspected recursive
comparison checks every canonical JSON against the full brief base, including
mixed-mode files, exact keys, values and file sets. Actual output:

```text
Canonical file set: 28 unchanged
Exactly 12 approved canonical field changes:
hard_chapter_17_first/units/source_ids
hard_chapter_17_first/units/notes
hard_chapter_17_second/units/source_ids
hard_chapter_17_second/units/notes
hard_chapter_17_central/units/value
hard_chapter_17_central/units/confidence
hard_chapter_17_central/units/source_ids
hard_chapter_17_central/units/notes
hr_jp_17/accessed
hr_jp_17/limitations
hr_fandom17/limitations
hr_fandom17/accessed
Other chapters/modes, mixed-mode JSON, Chapter 17 non-unit claims/conflict,
Hard tactics and quarantine: unchanged
Reviewed inputs outside approved inventory/source fields: unchanged
Private run file set/content preserved: 2 files; live run exists: False
```

The first eight locators are under
`data/chapters/hard_reinforcements.json/records`; the last four under
`data/sources.json`. Attribution narrows and notes change for all three unit
claims; only central value/confidence changes. Registry access dates and
limitations change only for the two Chapter 17 sources. Containing source
lists stay intact for other claims. Hash equality covers all 28 canonical files,
not just changed ones. Git status is clean after rebuilding.

Private baseline command was `python3 -`, using `pathlib`, `json` and
`hashlib.sha256(p.read_bytes()).hexdigest()` on canonical JSON, `CURRENT_RUN.md`
and all files recursively under `state/`. The private subset includes two
files, with no live run. Exact file-set and content equality passes after
checks; no player content or private digests are published.

My first driver invocation returned exit 1 at its final preservation comparison:
its referenced private snapshot was absent because my earlier baseline script
had stopped on the source-registry list structure. All preceding audit/rebuild
and CLI commands passed. I then captured the private snapshot and repeated the
complete required sequence successfully. Preservation evidence above applies
to this completed repeat; it is not a fabricated pre-first-run snapshot. No
production or run changes appeared after either rebuild sequence.

Regression verification:

```text
python3 -m unittest discover -s tests -p test_chapter17_provenance.py -v
exit 0; Ran 3 tests in 0.090s; OK
```

I independently assembled a temporary, minimal input fixture from the brief
base: baseline query/common tools, required data and author inputs, plus the
new test module. It is not a project checkout or a player run. Running the
same three tests there produced test exit 1:

```text
AssertionError: Lists differ:
['hr_fandom17', 'p2_guide_16_2', 'hr_jp_17'] != ['hr_fandom17']
AssertionError: [central six-unit list] is not None
Ran 3 tests in 0.124s
FAILED (failures=6)
```

Two attribution/author assertions and four query subcases fail on the old
inputs; all pass at the reviewed commit. This reproduces the Worker's material
pre-change result. Structural regressions still cannot validate the game.

Presentation commands used the installed marked renderer and headless Chrome
via Playwright on `SOURCES.md`, `STATUS.md`, `docs/hard-reinforcements.md`,
`research/UNCERTAINTIES.md` and `attachments/inventory-audit.md`. Exit 0; inspected
screenshots, including both modified source rows, the inventory matrix and new
paragraphs. Layouts fit the 1400-pixel viewport without overlap. Python
`re.findall` / `Path.exists()` local-link check returned
`Resolved local links: 3 exit 0`. Temporary renders/screenshots remain private.

## Not verified

The actual central wave composition is unobserved. No source independently
corroborates the exact first/second inventories. The current direct Fandom
revision is unavailable; source confidence refers to the scoped indexed report.
The six-unit value's external origin remains missing. Classic/Casual, regional
version equivalence, actual spawn phase, warning trigger, staircase mapping,
complete schedule and full-map safety are not established. No additional
verified gameplay coverage results from passing audits or rebuilding.
Historical Worker execution logs are compared with independently rerun checks,
not treated as independently observed past sessions.

Exactly one bounded next task: review one normally accessible or owner-provided,
clearly Hard-labelled observation of the central Chapter 17 arrival, with
visible inventory/equipment, setup/warning, phase and declared region/version
and mode where available, comparing both alternatives without assuming a fixed
turn. Suitable observation input is unavailable here. No next round was started.

## Verdict

The amendment corrects overbroad inventory attribution and prevents an unsupported
central literal from appearing as a supported known inventory. Both alternatives
and the schedule conflict remain visible, and fresh authoring/rebuilds preserve
the change without unrelated data drift. I am confident in the repository
behavior and bounded source interpretation, while actual gameplay remains
unresolved. Brain must independently re-derive and judge this exact commit
under owner approval; this report does not approve or merge it.

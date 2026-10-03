<!-- fw-report
round: 003-chapter5-research
role: verifier
branch: verifier/003-chapter5-research
head: c25da4e7b5acaed339aea04dade98d798cf93eed
os: macOS 27.0
python: 3.9.6
written: 2026-10-03T16:58:47Z
-->
Reviewed commit: `c25da4e7b5acaed339aea04dade98d798cf93eed`.
Environment: `macOS-27.0-arm64-arm-64bit`, Python `3.9.6`.

## Findings

- [SHOULD FIX, nonblocking provenance correction]
  `docs/rounds/003-chapter5-research/attachments/research.md:96` and `:127`
  describe the excluded GameFAQs candidate as `map-unscoped` and
  `chapter unscoped`. Its original opening post explicitly says `I'm on ch 11
  right now`, and post 3 describes `this chapter`. The failure is inaccurate
  evidence classification: future researchers may investigate an allegedly
  unidentified map even though its context already names a different map.
  Record it as explicitly different-map context and retain its exclusion from
  Chapter 5. The correct exclusion and unresolved conclusion are unaffected;
  this is not a blocker or a request to research Chapter 11. Related wording
  in `worker.md:145` and the retrieval log should be reconciled if amended.

No blocking factual leap or unauthorized canonical change found. I completed
my independent first pass before opening the Worker report or results
attachments: project policy, canonical Chapter 5 context, original Japanese
and guide contexts, contrary/insufficient candidates, required checks and
protected-file hashes. Western direct retrieval failed; the full indexed
context was independently obtained during pass two. I did not infer agreement
from failed retrieval. No new tests or production changes in this round.

### Acceptance assessment

1. Met with the disclosed indexed-source limitation. The exact western
   table/prose class discrepancy and Japanese Hard alternatives reproduce.
   Combined-difficulty, unlabelled-table and general-guide boundaries are
   explicitly separated. Direct current Fandom revision remains unverified.
2. Met. Independent focused searches found the Hard/Classic video and the
   firsthand Hard/Classic forum candidate; neither gave me visible arrival
   chronology. Other-difficulty and other-map hits were excluded. The Worker's
   additional candidates were inspected in pass two. No visible gameplay
   sequence was certified, and a new confirming source is not required.
3. Met subject to the provenance correction above. Matrix covers timing,
   phase, groups, areas, activation, trigger, suppression and completeness,
   linked through source-family IDs to URLs, dates and scope. Retrieved
   statements remain distinct from certified game facts; unknown phase,
   mode and version are not invented. Indexed copies remain one family.
4. Met. Evidence does not choose a Hard schedule, last wave, grace turn,
   safe route or effective blocking rule. Clarified source boundaries are
   useful research results without resolving the actual events.
5. Met. No amendment is proposed. Exactly one bounded Tier 2 Chapter 5
   controlled-observation task is recommended. Continuous early phase
   boundaries, initial/new unit distinction, matched occupancy/range trials,
   resets/cuts and map-ending censoring are specified. Its horizon cannot
   establish absence of later waves. This review does not authorize that task.
6. Met. Checks and source evidence are separated; no canonical/coverage
   increase claimed. Independent file-set/SHA-256 comparison and baseline
   diff show preservation. No live run exists.
7. Met. Original-context inspection and contrary/insufficient source search
   preceded Worker report/results. Material research claims compared below;
   access-specific details that I could not reproduce remain unverified.

### Independent source review and comparison

Retrieval date for every source/search below: `2026-10-03`. Public reader and
focused public-index search only; no challenge bypass, source-page archive,
footage download or game-file acquisition. URLs are code as required.

- `hr_jp_5` / J:
  `https://www.pegasusknight.com/wiki/fe13/マップ攻略/章別攻略/5章+聖王と暗愚王`.
  Direct reader succeeded. Original `kk` comment dated `2012-04-19 23:50:56`,
  reader line 148, explicitly says Hard. My translation: turn 3 has two
  Wyverns, Barbarian and Myrmidon from central-left; turn 5 is tentatively
  Barbarian and Myrmidon (`はず`). It distinguishes initial Wyverns moving
  turn 1 and range-triggered movement of the remaining initial group/boss.
  It does not specify arrival phase, Classic/Casual, region or software version.
  Earlier table headings at lines 110/113 specify after enemy phases 3/5,
  without a difficulty label. I agree with every J matrix row and the
  prohibition on borrowing that phase for the Hard comment. Japanese language
  and date suggest context, not proof of region/version.
- `reinforcements_early_0` / F:
  `https://fireemblem.fandom.com/wiki/The_Exalt_and_the_King`.
  Direct open returned internal error; retrieval later reported robots denial.
  No direct retry after definite denial. Focused indexed query in pass two
  returned original-page context including `Hard & Lunatic Mode`, strategy
  prose and reinforcement list. Table says T3 two Barbarians/Myrmidon,
  T4 two Wyverns, T5 Dark Mage/Myrmidon/Barbarian/two Wyverns; areas match
  the matrix. Prose instead gives T3 Dark Mage/Barbarian/Myrmidon and
  beginning-enemy-phase timing. Occupancy and turn-6 reassurance are source
  advice only. All F rows reproduce as indexed statements, with no
  independent Hard event, latest revision, phase observation or final-wave
  verification. The copy/index is not another evidence family.
- `p2_guide_04_2` / G:
  `https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/beginning-to-chapter/chapter-5-the-exalt-and-the-king`.
  Direct body lines 352–360 reads `Strategies for all Difficulties` and warns
  of fort reinforcements and movement. No numbered schedule in that body.
  This supports the local scope limitation, not a Hard timing table. It
  cannot discriminate new arrivals from initial movement or establish a
  suppression/trigger rule. I agree with its treatment in the matrix.
- `candidate_gf_hardclassic_ch5`:
  `https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/65988139`.
  Direct reader lines 117–125: DracoErus explicitly describes Hard/Classic
  replay and death resets; Kysafen reports two Hard plays. No numbered spawn
  inventory. Supports the reported applicability/reset limitation, not timing.
- `candidate_gf_hard_ch5`:
  `https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/65437343`.
  Direct reader lines 117–131: Chapter 5 Hard title, repeated resets and
  ally/Wyvern advice; no phase inventory. No arrival corroboration obtained.
- X:
  `https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/69714904`.
  Direct reader lines 117–127 explicitly identify Chapter 11 in opening
  context, then a same-chapter Hard/Classic reset account with turns and
  boss-defeat claim. Excluding this from Chapter 5 is correct; claiming
  unidentified map context is the finding above. No Chapter 11 fact adopted.
- `candidate_video_omega`:
  `https://www.youtube.com/watch?v=yM8RlvDbSkA`.
  Search metadata gives omegaevolution's Chapter 5 Hard/Classic title and
  publication `2013-02-10`. Reader open returned internal error. No gameplay
  frames, setup, phase boundary, timestamp, cut/reset, mode/region/version
  verification. I cannot independently reproduce the Worker's particular
  browser sign-in/bot challenge; the underlying lack of observed footage
  agrees. A separately found MegamanNG Hard/Casual candidate
  `https://www.youtube.com/watch?v=_zR9MZSsVZo` provides description metadata
  only in my pass; I did not treat it as observed gameplay or Classic evidence.
- `candidate_ip_playthrough`:
  `https://forums.neoseeker.com/55238/t1870378-tale-of-adventure-fails-ips-hard-mode-playthrough-summary/`.
  Reader returned internal error in my pass, not a reproduced 403. No event
  fact verified. Access-failure differences are not factual contradictions.

Independent blind searches included:
`Fire Emblem Awakening chapter 5 Hard reinforcements turn 3 turn 4`,
`Fire Emblem Awakening Hard Classic chapter 5 playthrough reinforcements`,
`site:fireemblem.fandom.com/wiki/The_Exalt_and_the_King "Turn 3" "Hard"`,
and `Awakening chapter 5 hard reinforcements barbarian dark mage turns`.
Results mixed other games/maps, Lunatic/Lunatic+ evidence, general mechanics
and relevant forum/video metadata. Those were not imported as Hard timing.
Pass-two targeted index queries included the same Fandom URL with
`"Hard & Lunatic" "Barbarians"`, `"Turn 5" "Turn 4"` and
`"Dark Mage" "forts"`; these reproduced its reported table/prose boundary.
The original indexed context is insufficient to establish a game schedule.

### Repository commands and actual results

All at the reviewed commit. No rebuild performed or authorized; no production
or research artifact edited by this Verifier. Only this report is written.

```text
make audit
exit 0; Ran 115 tests in 0.583s; OK
python3 tools/fw.py check
exit 0; 0 error(s), 0 warning(s)
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase player
exit 0; target EP3; CONFLICTED; hard_chapter_5_disputed_schedule
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase enemy
exit 0; target EP4; CONFLICTED; hard_chapter_5_disputed_schedule
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 5 --phase player
exit 0; target EP5; CONFLICTED; hard_chapter_5_disputed_schedule
git diff --check
exit 0; no output
```

All three CLI outputs retain spawn phase null/UNKNOWN, unknown schedule,
`schedule_complete: false` and `safe_to_conclude_no_reinforcements: false`.
This establishes existing query behavior, not actual arrival turns.

After reading the Worker report, independently reran:

```text
python3 docs/rounds/003-chapter5-research/attachments/verify.py /tmp/fea-v003-exact
exit 0; each of all six subprocess commands exits 0
protected_files: 30; canonical_json_files: 28
added: []; removed: []; changed: []
live_run_exists: false; state_files: [state/.gitkeep]
```

Protected snapshots before/after my checks used this Python code, exit 0:

```python
import hashlib, pathlib, json
r = pathlib.Path('.')
files = sorted(r.glob('data/**/*.json')) + [r/'CURRENT_RUN.md']
files += sorted(p for p in (r/'state').rglob('*') if p.is_file())
snapshot = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
# Compare both key sets and values to before, not only surviving files.
manifest_hash = hashlib.sha256(json.dumps(snapshot, sort_keys=True,
    separators=(',', ':')).encode()).hexdigest()
```

Actual before and after sorted-manifest SHA-256:
`4ae9655643ee1f8583f49ec87b38c2450ebeb41c236a1fc7922e205e6f3d5c10`.
File-set/hash equality is True for all 30 files. My manifest also matches the
Worker's preservation manifest exactly. No live run to test; state only contains
`.gitkeep`. Other-mode records are preserved within byte-identical JSON.
`git diff --name-only origin/main HEAD -- data CURRENT_RUN.md state STATUS.md
tools tests docs/state.md` exits 0, no output. Standing decisions unchanged.

### Presentation

Rendered both research Markdown files independently with bundled Node,
`marked.parse` and Playwright/installed Chrome to temporary screenshots outside
Git (exit 0); inspected both with the image viewer. Matrix, context, source URLs
and observation plan are readable. Local links parsed with Python Markdown
regex and resolved relative to attachment directory: `3` targets, all exist,
exit 0. Rendering validates presentation only, not source accuracy.

## Not verified

Actual Hard Chapter 5 timing/phase/counts/classes/spawn coordinates, trigger
conditions, suppression, full schedule and map safety remain unverified.
No game-derived visible sequence obtained; no footage timestamps can be
claimed. Latest direct Fandom revision unavailable. Access-specific Worker
browser challenge and Neoseeker 403 not reproduced by my reader. These access
limits do not imply agreement or absence. No exact region/software version
established for any reported arrival, nor Classic/Casual for F/J/G. No Linux,
Windows or current remote CI checks. No live run initialized or exercised.
No certified gameplay coverage, canonical amendment or accepted next round.

## Verdict

The delivered research is a credible, bounded unresolved result at the reviewed
commit: important source boundaries and conflicts reproduce, repository checks
pass, and canonical/run files remain untouched. No blocker to recording this
research found. Correct the nonblocking different-map provenance wording before
reusing that source catalog; it does not change the absence of admissible Chapter
5 suppression evidence. The single proposed observation task is reasonable,
but needs Brain's decision and separate authorization. This report is evidence
for exact-commit Brain review, not merge approval or a tactical safety guarantee.

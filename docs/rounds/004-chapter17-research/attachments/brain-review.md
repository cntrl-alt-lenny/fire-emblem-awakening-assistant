# Brain review — round 004

Decision: accept the bounded unresolved research at exact delivered commit
`79ae3374036cb7460df05a44ab669274437b1c73`, pending owner merge approval.
Worker artifact commit: `159f99496f352a42fb3f25cfa1039e7dfeb9f398`.
Verifier reviewed `bdaa9772a7cea1c01c67b4228f09cdadc2912438`;
the delivered successor adds only its report. No gameplay schedule, canonical
amendment or new certified coverage is accepted.

## Independent repository evidence

2026-10-03; macOS 27.0 arm64; Python 3.9.6. Commands below exited 0 at the
literal delivery before this review attachment was added.

```text
python3 tools/fw.py delivery --round 004-chapter17-research
origin/verifier/004-chapter17-research (79ae3374036c): delivered
verifier: report describes bdaa9772a7ce
worker: report describes 159f99496f35

git rev-parse HEAD
79ae3374036cb7460df05a44ab669274437b1c73

python3 docs/rounds/004-chapter17-research/attachments/verify.py /tmp/fea-brain004-exact-review /tmp/fea-brain004-before-private.json
make audit -> exit 0
python3 tools/fw.py check -> exit 0
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase player -> exit 0
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase enemy -> exit 0
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 9 --phase player -> exit 0
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 10 --phase player -> exit 0
git diff --check -> exit 0

Audit excerpt:
Ran 115 tests in 0.954s
OK

Framework check: 0 error(s), 0 warning(s)
Protected files: 30; canonical JSON: 28; state files: 1
added_count: 0; removed_count: 0; changed_hash_count: 0
live_run_exists: false

git diff --name-only 867b664..HEAD
Only five round-004 attachments, worker.md and verifier.md

gh run view 37146098977 --json headSha,conclusion,jobs,url
headSha: 79ae3374036cb7460df05a44ab669274437b1c73
conclusion: success
Audit (macos-latest, Python 3.13): success
Audit (ubuntu-latest, Python 3.13): success
Audit (ubuntu-latest, Python 3.9): success
```

Brain inspected the standard-library evidence runner before running it. Brain
independently created the private baseline using `python3 -`, `hashlib` and
`pathlib`, reconstructed the protected file set with `git ls-tree -r
--name-only 867b664`, and compared SHA-256 values with each corresponding
`git show 867b664:<path>` blob. All 30 files matched before the runner and
remained unchanged afterwards; other difficulty data is included. Actual
digests and raw state remain private. No live run exists or was initialized.

The four CLI queries retain conditional candidates and conflict/unknowns;
enemy phase 8 targets enemy phase 9. This proves current software behavior,
not actual gameplay. No production tools/tests, canonical data, rebuild code,
source registry, coverage or standing decisions changed after the brief base.
The default-branch diff also includes Brain's previously supplied brief,
Chapter 5 parking decision and review; those are not Worker changes.
No rebuild was required or performed.

## Independent source assessment

Retrieval date: 2026-10-03. Brain used direct public readers for J/G and the
scoped forum/Reddit contexts, and an indexed original-page context for F/C6.
Index copies remain in the originating source family. No restricted access
was retried, no gameplay media downloaded and no whole guide archived.

- J: [Japanese chapter/comments](https://www.pegasusknight.com/wiki/fe13/%E3%83%9E%E3%83%83%E3%83%97%E6%94%BB%E7%95%A5/%E7%AB%A0%E5%88%A5%E6%94%BB%E7%95%A5/17%E7%AB%A0%2B%E6%AD%BB%E3%81%AE%E9%81%8B%E5%91%BD),
  `hr_jp_17`. Brain independently translates the Hard-labelled 2012-04-27
  11:57:31 comment as four units from four left stairs, including a Sniper,
  approximately three turns after the announcement. It does not expressly
  identify the first wave or specify event phase. J2/J3 are difficulty
  unlabelled; their timing/trigger wording cannot borrow J1's setting. The
  2014-09-06 Hard comment concerns movement of existing enemies in the upper
  six rows and offers occupancy advice; it does not demonstrate a spawn trigger
  or suppression experiment. The table is initial placement. These boundaries
  reproduce the matrix and keep translation separate from game verification.
- G: [Chapter 17 guide](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-17-inexorable-death),
  `p2_guide_16_2` / `p2_survey_16_2`. The local heading explicitly covers all
  difficulties. Its relative interval is between initial and subsequent
  arrivals, not warning-to-first. The paragraph gives no exact class/count
  inventory. Duplicate registry IDs provide one publisher family.
- F: [Western wiki](https://fireemblem.fandom.com/wiki/Inexorable_Death),
  `hr_fandom17`. Focused public search reproduced a Hard heading, incomplete
  warning sentence, eastern T8 four-unit inventory and allegiance conversion,
  followed by nearby T9/T10 rows. T10 lists two units, not the canonical six.
  A later Lunatic boundary is visible, but no later waves were adopted. Direct
  access was reported robots-denied; current direct revision is unverified.
  This corroborates reported wording, not a universal schedule or phase.
- C1/C5: direct [stairs thread](https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/66653306)
  opening and Tables post 5, and [warning thread](https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/77319034)
  sad-boi post 4 reproduce the catalog's Chapter 17 scope. Neither establishes
  Hard setup or the required warning/phase interval. C5 was readable to Brain,
  unlike the Worker's failed retrieval; this supplies no missing game sequence.
- C2/C3: direct original Reddit openings reproduce chapter scope and narrative
  limitations. Coridoras's central-Sniper account lacks a warning/numbered-phase
  anchor; Isilel's separate Hard/Casual setting cannot be transferred. RAlexa21th
  describes consolidation and preparation, without first-stair timing.
- C6: indexed original [misnumbered thread](https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/70523749)
  reproduces the complaint, Chapter 16 correction and acknowledgment in posts
  4/6/7. Exclusion from Chapter 17 is justified; direct revision is unverified.

Brain obtained no gameplay frames or continuous Hard arrival sequence. The
specific historical 402 response and video-browser gate were not independently
reproduced. The Verifier's UNPROVEN CLAIM finding is valid as an access-log
limitation. Treat those exact outcomes as reported session observations, not
Brain-verified results. No game conclusion depends on them; no blocker follows.

## Finding disposition and acceptance

All seven research acceptance criteria were checked against the actual diff,
source boundaries, claim matrix, bounded retrieval record, observation plan and
required checks. No blocking finding remains. No canonical amendment is
proposed, so accepting the research cannot adopt an unproven arrival claim.

Brain independently confirms the inherited provenance questions: the stored
first-wave unit field cites three sources but the retrieved exact inventory
is supplied by F alone, with partial J attributes and no G inventory. The
central six-unit record is not reproduced by the indexed two-unit T10 row.
These are gaps to resolve in a separately reviewed Tier 2 provenance/data
round, not evidence that either gameplay inventory has been disproved.

Accept the unresolved source record and the conditional observation protocol.
Do not upgrade confidence, certify first-side ordering, assign a fixed turn,
claim a safe staircase or silently amend the inherited data from this review.
The proposed footage task requires suitable accessible inputs. A continuous
run can establish its sequence; causal triggers need matched comparisons.
Missing recordings must not be invented or treated as already available.

## Merge card

Changed: research catalog, claim matrix, retrieval log and seat reports; inherited
Brain brief/review and parking decision also accompany the default-branch diff.
Verified: independent source-boundary checks, all 115 tests, framework hygiene,
Linux/macOS CI, three local links and preservation of 30 protected files.
Not verified: actual first staircase, warning/arrival phase or trigger, universal
timing, exact inventory, suppression, complete schedule or route safety.
Risk: gameplay uncertainty remains, with inherited attribution/inventory gaps
explicitly exposed; this merge records research rather than adopting mechanics.

Brain inspected the rendered GitHub research prose, claim matrix, findings and
search-log table. Local-link resolution with Python `re.findall` and
`Path.exists()` returned `3 local links resolved; exit 0`.
No merge performed. Owner approval is required by `AGENTS.md`.

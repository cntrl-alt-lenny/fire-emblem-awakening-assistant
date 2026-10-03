# Brain review — round 003

Decision: accept the bounded research record at delivered commit
`e933b3c2c8aadde3a49bca14c653e132dbb437a4`, pending owner merge approval.
Worker evidence describes `74a6a3d1ea22f30c0f3e2115aa4ee5984e97fe77`;
Verifier reviewed `c25da4e7b5acaed339aea04dade98d798cf93eed`.
The final delivery adds the Verifier report only. No canonical amendment or
new certified gameplay coverage is accepted. The actual arrival conflict
remains unresolved.

## Independent checks at the exact delivery

2026-10-03; macOS 27.0 arm64, Python 3.9.6. All commands below exited 0.

```text
python3 tools/fw.py delivery --round 003-chapter5-research
origin/verifier/003-chapter5-research (e933b3c2c8aa): delivered
verifier: report describes c25da4e7b5ac
worker: report describes 74a6a3d1ea22

python3 docs/rounds/003-chapter5-research/attachments/verify.py /tmp/fea-brain003-exact-review
make audit -> exit 0
python3 tools/fw.py check -> exit 0
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase player -> exit 0
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase enemy -> exit 0
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 5 --phase player -> exit 0
git diff --check -> exit 0
protected_files: 30; canonical_json_files: 28
added: []; removed: []; changed: []
live_run_exists: false; state_files: [state/.gitkeep]

Captured make audit result from that run:
Ran 115 tests in 0.625s
OK

git diff --name-only 91193ff..HEAD -- . ':(exclude)docs/rounds/003-chapter5-research'
(no output)

git status --short
(no output)

gh run view 37138830818 --json conclusion,headSha,url
headSha: e933b3c2c8aadde3a49bca14c653e132dbb437a4
conclusion: success

gh run view 37138830818 --json jobs --jq '.jobs[] | {name,conclusion}'
Audit (macos-latest, Python 3.13): success
Audit (ubuntu-latest, Python 3.9): success
Audit (ubuntu-latest, Python 3.13): success
```

The evidence runner was inspected before use and writes only to the supplied
temporary output directory. Brain separately reconstructed the protected
file set and SHA-256 values with `hashlib`/`pathlib`: all 30 current entries
match the before manifest exactly. No live run exists. Independent Markdown
link resolution found three local targets, all existing. No production, data,
standing-decision or coverage-counter changes were delivered. No rebuild
was required or performed.

## Independent source re-derivation

Brain reread or retrieved scoped indexed contexts on 2026-10-03, comparing the
claim matrix with the source boundaries. Public index copies remain evidence
from the originating source, not independent corroboration. Direct access
restrictions were respected; no retry after definite robots denial, footage
download, game-file acquisition or source-page archive.

- J, `hr_jp_5`:
  `https://www.pegasusknight.com/wiki/fe13/マップ攻略/章別攻略/5章+聖王と暗愚王`
  Direct reader succeeded. The dated Hard comment by kk describes two initial
  Wyverns moving on turn 1 and a different turn-3 arrival mixture from the
  western table, with a tentative turn-5 account. It does not state arrival
  phase. The earlier table's after-enemy-phase headings are unlabelled by
  difficulty. Brain's translation agrees with the bounded matrix; borrowing
  that table's phase for the Hard comment would be unsupported. Region,
  software version and Classic/Casual are not established by that comment.
- F, `reinforcements_early_0`:
  `https://fireemblem.fandom.com/wiki/The_Exalt_and_the_King`
  Public indexed original-page context exposes the combined Hard/Lunatic
  heading. The turn-3 table and strategy prose name different class mixtures;
  later-turn groups and source-relative areas match the research matrix.
  Prose includes fort occupancy and final-wave reassurance, but none is a
  controlled Hard observation. Direct page access is robots-denied; current
  revision and Hard-only event behavior remain unverified. This reconstructs
  a reported conflict, not a selected game schedule.
- G, `p2_guide_04_2`:
  `https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/beginning-to-chapter/chapter-5-the-exalt-and-the-king`
  Direct reader exposes the local all-difficulties strategy heading. Its
  warning about arrivals/movement is not a numbered Hard-only phase inventory.
  The local scope limitation is independently reproduced.
- The two scoped GameFAQs candidates were recovered in indexed public context.
  Their Chapter 5 Hard / Hard-Classic scope and reset context agree with the
  catalog; retrieved material supplies no observed phase sequence. Brain's
  access was indirect, unlike the seats' reported direct retrieval. No stronger
  evidentiary weight is inferred from either account.
- X:
  `https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/69714904`
  Public indexed original-thread context explicitly identifies Chapter 11
  in the opening post, with the responding account referring to that chapter.
  The Verifier's provenance finding is correct. No event claim from that
  thread is admissible for Chapter 5.

Brain did not independently reproduce the exact video-browser challenge or
Neoseeker HTTP result. Neither seat claims visible footage observations;
those candidates remain unavailable evidence, not confirmation or absence.
No independently observable gameplay sequence was obtained by this review.

## Provenance erratum and finding disposition

Nonblocking correction for any reuse of this catalog: research.md's
`map-unscoped` / `chapter unscoped` labels for candidate X are inaccurate.
Classify it as explicitly different-map context (Chapter 11), retaining its
exclusion from Chapter 5. The related Worker summary and retrieval-log wording
must be read with this correction. The Verifier report already records the
correction in the delivered commit. This Brain review is an explicit erratum,
not a silent edit of the stamped Worker artifacts or a new Chapter 11 claim.

No blocker remains to recording the unresolved research. All seven criteria
were assessed against the actual diff, sources, bounded retrieval attempts,
claim matrix, follow-up protocol and required checks. The limited indexed
retrieval and unavailable gameplay are disclosed rather than converted to
certainty. No canonical amendment is proposed. The proposed observation
horizon distinguishes the named early-turn alternatives but cannot prove
the last wave or whole-map safety. No factual adoption is authorized.

## Next direction

Resolving this conflict now requires observable Hard gameplay rather than
another comparison of the same textual accounts. The proposed continuous
Hard/Classic observation protocol is a reasonable bounded next evidence task,
but requires a usable recording or controlled observations with known setup.
Neither matched trials nor their missing inputs can be invented from a video
title. Do not brief execution as though that evidence is already available.
If such evidence cannot be supplied or accessed normally, retain Chapter 5's
conflict and move to the standing Chapter 17 research priority while awaiting it.

## Merge card

Changed: source-context research, claim matrix, access log and independent
review only; canonical data and gameplay behavior unchanged.
Verified: scoped source boundaries/conflicts, the different-map exclusion,
115 tests, hygiene, Linux/macOS CI and 30 protected files preserved.
Not verified: actual Chapter 5 arrivals, phases, triggers, suppression,
complete schedules or map safety; no footage sequence observed.
Risk: a useful unresolved result, not new tactical certainty; use the explicit
provenance erratum rather than the original candidate-X label.

No merge performed. Owner approval is required under AGENTS.md.

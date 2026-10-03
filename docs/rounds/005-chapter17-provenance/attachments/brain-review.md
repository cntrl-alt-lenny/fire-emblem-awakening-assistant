# Brain review — round 005

Decision: **accept** the delivered amendment at
`6c87334bd6b5ccbc7b0a6f0e2a3ac24af99d4e3b`, pending owner approval to merge.
No blocking finding. This is a provenance/uncertainty correction, not proof of
the actual central inventory or arrival schedule.

## Exact delivery and scope

`python3 tools/fw.py delivery --round 005-chapter17-provenance` returned exit 0:
`origin/verifier/005-chapter17-provenance (6c87334bd6b5): delivered`.
Worker implementation/artifacts: `4409b66f1b7a79b0715bf4b660fa87af831b853d`;
Worker report and Verifier-reviewed commit:
`d05818683e32cb3c497517badb28d85d42292275`.
The only difference from that reviewed commit to the accepted delivery is the
Verifier report. Brain reran the required checks at the final delivery itself.
Brief base: `a97ee2d8a528d7f8fef62b06978a3c3861599e69`.

First/second inventories retain their four-unit source reports with Fandom-only
unit attribution and precise limits. Central units become null/CONFLICTED;
notes preserve the unsupported six-unit literal and indexed two-unit account.
No actual composition is selected. Other Chapter 17 fields, aggregate source
lists and timing/staircase conflict remain unchanged. Source metadata changes
are confined to the two relevant entries. Authoring assignments follow generic
note rewriting, and the existing offline producer preserves reviewed claims.

The default-branch diff also carries the previously reviewed round 004 Brain
record and parked Chapter 17 decision from the supplied brief. Neither is a
new Worker implementation. No new verified gameplay coverage is claimed;
existing map/wave counters and zero complete schedules remain valid.

## Independent re-derivation

On 2026-10-03 Brain independently inspected the existing source contexts:

- [Fandom](https://fireemblem.fandom.com/wiki/Inexorable_Death): bounded public
  index lookup for the central entry reproduced the Hard reinforcement heading
  and reported turn-8/9 inventories of two Heroes/Silver Sword, one War
  Monk/Silver Axe and one Sniper/Silver Bow each. Turn 10 reports one War
  Monk/Silver Axe and one Hero/Silver Sword. The direct revision remains
  unavailable; a robots denial was respected. Later rows were not adopted.
- [Gamer Guides](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-17-inexorable-death):
  the local all-difficulties strategy paragraph describes stairs and warning,
  without enumerating reinforcement classes/counts/equipment. It cannot support
  the entire stored unit claim.
- [Pegasus Knight](https://www.pegasusknight.com/wiki/fe13/%E3%83%9E%E3%83%83%E3%83%97%E6%94%BB%E7%95%A5/%E7%AB%A0%E5%88%A5%E6%94%BB%E7%95%A5/17%E7%AB%A0%2B%E6%AD%BB%E3%81%AE%E9%81%8B%E5%91%BD):
  Hard-labelled 2012-04-27 11:57:31 comment supplies four arrivals with a
  Sniper, not the complete inventory/equipment or explicit ordinal. The initial
  enemy table and difficulty-unlabelled 2014-02-09 sequence cannot fill that
  gap. The 2014-09-06 Hard comment concerns initial activation/stair blocking.

Language/date alone do not establish region/version or Classic/Casual. These
are source reports, not controlled gameplay observations. Narrowing attribution
is justified. Keeping actual central composition unresolved is justified;
access availability cannot choose the correct gameplay count.

`git log --follow --format='%H %s' -- research/hard_verification/author_review.py`
returned the amendment and root commit only, exit 0. `git rev-list
--max-parents=0 HEAD` returned `cf17834fd6a8867d06c25faa772a5d8700f32167`,
exit 0. Independent inspection of its author line 92 reproduced the central
3-Hero/2-War-Monk/1-Sniper literal. History provides no earlier provenance.

Verifier reports no findings. Brain checked each material acceptance claim,
including source dispositions, exact field scope, regeneration, regressions,
CLI categorization, preservation and CI. The Verifier disclosed prior round
004 conversation exposure; its round 005 original-source/baseline pass preceded
opening Worker results. This limits complete informational blindness but does
not invalidate its independently reproduced evidence. Brain's own source and
behavior checks also agree. No unavailable source is being treated as proof.

## Actual checks at the accepted delivery

Environment: `uname -s -r` → `Darwin 27.0.0`; `sw_vers -productVersion` →
`27.0`; `python3 --version` → `Python 3.9.6`. Each command returned exit 0.

The committed validation driver was inspected before execution. Brain captured
a private pre-check file-set/hash baseline with `pathlib`/`hashlib` outside Git,
then invoked the driver via `python3 -`, passing that baseline using
`Path(tempfile.gettempdir()) / 'fea-brain005-private-before.json'`.
Complete driver exit: 0. Actual child results:

```text
git rev-parse HEAD
exit 0; 6c87334bd6b5ccbc7b0a6f0e2a3ac24af99d4e3b
make audit
exit 0; Ran 118 tests in 0.699s; OK
make rebuild
exit 0; registered_sources: 217; source_refs_resolve: true
make audit
exit 0; Ran 118 tests in 0.696s; OK
make rebuild
exit 0; registered_sources: 217; source_refs_resolve: true
make audit
exit 0; Ran 118 tests in 0.687s; OK
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
compare-preservation.py with private pre-check baseline
exit 0; exactly 12 approved canonical field changes
Other chapters/modes, mixed-mode JSON, Chapter 17 non-unit claims/conflict,
Hard tactics and quarantine: unchanged
Reviewed inputs outside approved inventory/source fields: unchanged
Private run file set/content preserved: 2 files; live run exists: False
python3 -m unittest discover -s tests -p test_chapter17_provenance.py -v
exit 0; Ran 3 tests in 0.083s; OK
git status --short
exit 0; no output
```

The twelve canonical differences are the eight Chapter 17 `units` fields
listed by the inspected recursive comparison, plus accessed/limitations on
`hr_fandom17` and `hr_jp_17`. No other JSON field differs from the brief base.
All four queries retain three conditional candidates, unknown phase, incomplete
schedule and false safety/absence guarantees. Central units are excluded from
known claims and remain visible among uncertain claims with both alternatives.

An earlier driver invocation used an incorrect temporary-directory argument:
its audits/rebuilds/queries passed, but the final comparison returned exit 1
because that path did not exist. The original pre-check baseline was retained;
using its actual location passed preservation. The complete sequence above
was then rerun successfully. No run data changed or baseline was fabricated.

Brain independently constructed a temporary minimal fixture from the brief
base using `git show BASE:PATH`, adding the new regression module. Running
`python3 -m unittest discover -s tests -p test_chapter17_provenance.py -v`
there returned exit 1: `Ran 3 tests in 0.062s; FAILED (failures=6)`.
Failures reproduced broad source attribution and promoted six-unit central
inventory, including all four phase-query subcases. These tests can detect
the old behavior; they cannot establish game composition.

`gh run view 37149566325 --json headSha,conclusion,jobs,url` returned exit 0:
accepted delivery SHA, overall success and successful Linux Python 3.9/3.13
and macOS Python 3.13 jobs.
[Exact-delivery CI](https://github.com/cntrl-alt-lenny/fire-emblem-awakening-assistant/actions/runs/37149566325).

Brain resolved all three local Markdown links in the seven changed documents,
exit 0, and inspected GitHub-rendered inventory matrix, STATUS addition,
uncertainty addition, reinforcement scope/conflicts and source table. Layout
and links were readable. Appearance is separate from source truth.

## Remaining uncertainty and next direction

Actual central inventory, first staircase, warning trigger/interval and spawn
phase remain unobserved. Exact first/second inventories lack independent
corroboration. No region/mode equivalence or complete schedule is certified.
The agents' proposed central-arrival observation is useful only when suitable
observable Hard evidence is available; that input remains unavailable.

After owner-approved merge, recommend a bounded research round on Chapter 20's
disputed victory condition. Keep Chapter 5/17 unresolved pending observable
evidence instead of repeating the same textual comparison. This recommendation
does not start a new round or change canonical data.

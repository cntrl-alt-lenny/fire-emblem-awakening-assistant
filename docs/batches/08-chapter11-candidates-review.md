# 08-chapter11-candidates — independent Verifier

Reviewed: `718bb7620605665a7db68c0c8e67094bc7deba55`.
Starting main: `d3b646975a5f0686a798aaf12c0e541ed396da08`.
Plan: `b67b91203c02bc7353f497bdfb5473bbbee40ed9`.
Remote Worker matched the literal reviewed commit after fetch. Review used a
separate detached linked checkout; primary and Worker checkouts were untouched.

## Blind ordering and source pass

Before reading production changes, new tests, changed assessment or Worker
summary, privately recorded original canonical timing, player/enemy queries,
and bounded registered source context. Baseline player 3/enemy 2 retained forts;
player 4/enemy 3 retained only northwest; player 5/enemy 4 dropped both.
Then inspected production diff, tests, summary and evidence in that order.

Public web reader, 2026-10-09: [Chapter 11](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/beginning-to-chapter/chapter-11-mad-king-gangrel),
strategy paragraph at reader line 363, supports the positioning warning and fort
suppression; line 365 separately reports northwest turn 4 on Hard.
[Reading This Guide](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/information/reading-this-guide),
line 341, establishes Hard default. One publisher family; Classic/Casual,
region/revision and full schedule remain unspecified. An initially mistaken
scope URL returned Internal Error; corrected to the registered URL without bypass.

## Findings and verdict

**NOTE — `data/chapters/hard_reinforcements.json:387`:** turn 3 is an interpreted
candidate boundary, not a directly established first-spawn script. The source
contains no recurrence/end schedule. PARTIAL timing, null turns/repeat, explanatory
notes and preserved unknowns expose this limit; no unsupported recurrence found.

**NOTE — `research/hard_verification/chapter11-candidates.md:14`:** same-publisher
scope is not independent gameplay corroboration. Tests cannot resolve the
acknowledged difficulty-phase/version gaps or certify whole-map safety.

**PASS for the bounded acceptance criteria; no BLOCKER or SHOULD FIX finding.**
Fort candidates persist from the interpreted start; northwest remains fixed.
Chapters 7/16 and event controls retain their prior behavior. Authoring reproduces
canonical timing; rebuilds preserve it. Only that timing changed against baseline:
27 other canonical files, 28 unrelated waves, all Hard tactics, quarantine and
other modes are identical. Pre-check private hash snapshots prove regular-file
sets/content and CURRENT_RUN unchanged in primary and review checkouts.
Event-family accounting changes classification only; complete schedules remain zero.
Brain re-derivation and owner merge approval remain required.

## Independent command evidence

Commands ran at the reviewed commit unless identified as the private baseline.

| Command | Actual relevant output | Exit |
|---|---|---:|
| `python3 tools/fw.py status` (primary, first) | Project checks pass; machine clean | 0 |
| `git fetch origin`; `git rev-parse 718bb76 origin/worker/08-chapter11-candidates` | Both resolved to reviewed commit | 0 |
| `python3 -m unittest discover -s /tmp/fea08-independent/baseline/tests -p test_hard.py -k chapter11 -v` (archived main; delivery tests only) | Ran 2 tests; FAILED (failures=6) | 1 |
| `make rebuild` twice | Each: Hard audit passed=true; 44 maps, 29 records, 217 sources | 0/0 |
| Sorted relative-path SHA-256 manifests of `data/**/*.json` after each rebuild | 28 hashes identical; manifest SHA-256 `d51ff1242dfba2f7155c8447d4cfeb9c610b1f31f7a26e38fffd2be488ccacd4` | 0 |
| `make audit` | Validation/phase2/Hard passed; Ran 122 tests in 2.285s; OK | 0 |
| `python3 tools/fw.py check` | 0 error(s), 0 warning(s) | 0 |
| `git diff --check d3b646975a5f0686a798aaf12c0e541ed396da08..HEAD` | No output | 0 |
| `python3 /tmp/fea08-independent/verify.py "$PWD"` | Preservation assertions pass; bounded authoring timing matches; zero complete schedules | 0 |
| Node marked/installed Chrome render; local-link resolver | Five changed Markdown documents rendered and visually inspected; no horizontal overflow; 8 local links resolve | 0 |

| Independently asserted phase controls | Result |
|---|---|
| Chapter 11 player/enemy turns 1,2,3,4,5,6,99 | Fort iff target >=3; northwest iff target=4; completeness/absence certainty false |
| Chapters 7/16, target phases 1–9, both current phases | Fixed arrivals only at 5 / 4,5,6 |
| Chapter 19, Paralogues 10/14, Endgame; turns 1,3,99, both phases | Unknown/event/repeat families retained |

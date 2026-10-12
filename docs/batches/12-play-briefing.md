# Batch 12-play-briefing — Worker

## Done

Added an offline, read-only Hard/Classic briefing around `map_info.query`.
Chapter7's baseline output falls from 333 JSON lines to 27 physical text
lines (363 words); wrapped terminals may show more lines. All returned values
and confidence remain visible; only exact repeated notes are abridged.
Unique dangers and conflicted notes have no length cap. Provenance restores
full notes/source IDs; details retain the complete spoiler-filtered query.

Explicit state supplies context only. Known chapter/turn/difficulty mismatches
are refused after alias normalization; phase remains mandatory. Deliberate
spoiler overrides are supported. No spoilers withholds every tactical claim
and provenance label. Tactical replies abridge other-map references while
retaining current-map caveats; explicit Full information keeps originals.
No deployment advice, stat conversion, run initialization or mutation added.

## Checked

Baseline: `e78fa7bcc245071556a408f725105ac63ce7a8e9`.
Approved plan: `ea5eb003d232f1e45a1c31e5ac2bb7412949b56e`.
Code commit: `77baae3db23078b6315b9a01e55eafaceeec4ec2`.
The delivery adds evidence and repairs/extends only the QA renderer.
Real outputs/exits are in [evidence](attachments/12-play-briefing/acceptance.log),
[audit](attachments/12-play-briefing/audit.log),
[framework](attachments/12-play-briefing/framework.log),
[focused tests](attachments/12-play-briefing/focused.log),
[diff](attachments/12-play-briefing/diff.log) and
[render](attachments/12-play-briefing/render.log).

| Command / check at code commit | Actual result | Exit |
|---|---|---:|
| `make audit` | Three validators/audits passed; 146 tests OK | 0 |
| `python3 tools/fw.py check` | 0 errors, 0 warnings | 0 |
| `python3 -m unittest discover -s tests -p test_play_briefing.py -v` | 15 tests OK | 0 |
| `python3 docs/batches/attachments/12-play-briefing/acceptance.py --baseline /tmp/awakening-12-preservation.json` | 108 CLI/raw-query comparisons; phase/fixed/event/family/conflict/absence controls; No-spoiler views; context refusals; synthetic bytes/file set preserved | 0 |
| `git diff --check e78fa7bcc245071556a408f725105ac63ce7a8e9 HEAD` | No output | 0 |
| Render reference; resolve links; inspect screenshot | Six local links resolve; no horizontal overflow; visually inspected | 0 |

Canonical 28-file set, 131 research files and both two-file private sets/content
are unchanged against a private pre-work snapshot. No private paths, hashes or
run values were published. Query results are copied before filtering.

## Not checked

No new external facts, observational gameplay, real-session usability, source
independence or complete schedule/safety certification. No rebuild was needed:
canonical data and build code are unchanged. Coverage counters remain unchanged.
Other difficulties, Casual and native Windows remain outside this reference.
Fresh blind Verifier, Brain re-derivation and owner merge approval remain due.

## Failed or blocked

An initial test-file read used a nonexistent filename; inventory corrected it.
One focused run failed because shortening an objective note violated the
conflict-preservation assertion; all conflicted notes now remain verbatim.
Initial visual QA hit Playwright's CommonJS export shape; the portable
evidence renderer now handles that export. [Attempts](attachments/12-play-briefing/attempts.md)
retain commands, relevant failures and exits. No Worker blocker remains.

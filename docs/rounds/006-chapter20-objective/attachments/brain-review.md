# Round 006 Brain review

Review date: 2026-10-05. Decision: reject this research delivery pending a
bounded evidence correction in round 007. No merge is authorized or performed.

## Exact delivery

Worker research commit: `16ab2465f402cee0b93be4772bd5f5ff5525235c`.
Worker report commit reviewed by the fresh Verifier:
`c32b3a00dbd6c33b111aca46275deade5a984f77`.
Complete delivered branch: `origin/verifier/006-chapter20-objective-2` at
`d001895f2c474581359161f8c5134329aed2a0b5`.
The earlier Verifier branch reviews older Worker work and is not the delivery.

`python3 tools/fw.py delivery --round 006-chapter20-objective` exited 0 and
selected the complete branch above. Brain inspected the actual attachment,
reports, full change scope and standing-decision diff. Production records,
tools and tests are unchanged. The state edits retain parked Chapter 5/17
uncertainty; they do not introduce gameplay verification.

## Independent re-derivation

Bounded source reads and indexed queries on 2026-10-05 reproduced:

- [Gamer Guides Chapter 20](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-20-the-sword-or-the-knee),
  Note: Chapter 20, Condition, reader line 332: `Defeat every Boss`.
  The boss table and all-difficulties strategy heading are separate contexts.
  This establishes source attribution, not the game's completion condition.
- [Fire Emblem Wiki chapter list](https://fireemblemwiki.org/wiki/List_of_chapters_in_Fire_Emblem_Awakening),
  Main story, Chapter 20, Objectives column, reader line 41: `Defeat Walhart`.
  No visible Hard/Classic objective or completion transition accompanies it.
- [MKaykitkats GameFAQs FAQ](https://gamefaqs.gamespot.com/3ds/643003-fire-emblem-awakening/faqs/64260),
  indexed Chapter 20 `[WM20]` metadata and the footnote following Excellus:
  `Mode: Normal/Hard/Lunatic`, `Condition: Defeat Boss`, and
  `Walhart is the "commander", defeating him ends the level.`
  The sentence is recoverable in indexed retrieval. No direct restricted-page
  retry was made. Search output also contains other chapters; those contexts
  do not acquire Chapter 20 scope. Index access is not game observation.
- [Gamer Guides Reading This Guide](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/information/reading-this-guide),
  Hard-default note at reader line 341, compared with MK's indexed introductory
  Hard-default note. Their wording overlaps substantially. This supports a
  possible dependency lead; it establishes neither copying nor independence.
  Different sites, named authors or differing wording do not resolve lineage.
- [Vandal Chapter 20](https://vandal.elespanol.com/guias/fire-emblem-awakening/capitulo-20-lucha-o-sumision),
  Victoria field at reader line 82, supports the Worker's commander translation.
  It does not supply visible Hard/Classic setup or discriminate surviving bosses.

The first-person GameFAQs board URL returned an internal retrieval error;
one bounded indexed lookup did not recover that specific thread. Brain does
not independently certify its text or setup. The Verifier's recovered report
is evidence of that review, not Brain's direct observation. No suitable
continuous game capture was inspected. Searches stopped here; inaccessible
sources were not bypassed and no footage/game assets were downloaded.

## Findings judged

1. **MK completion quotation:** the Verifier's inability to reproduce it was
   accurate for that review. Brain now reproduced it through the index, so it
   need not be removed as false. Its retrieval route and exact local scope
   still need to be stated; neither the quotation nor metadata verifies play.
2. **Source independence:** unresolved. The Worker attachment repeatedly calls
   MK independent and counts distinct families without resolving the recorded
   overlap concern. Its main assessment therefore overstates corroboration.
   A correction can honestly mark independence unknown; it need not prove
   copying or exhaust an unavailable source. This is why round 006 is rejected
   under the exact-commit acceptance rule despite the conservative gameplay
   conclusion and the Verifier's absence of a demonstrated production blocker.
3. **Observation plan:** both remaining bosses and continuous completion are
   correctly required. Hard/Classic settings must be visibly tied to the same
   save. The plan cannot assume a preparation screen exposes those settings.
4. **Evidence gaps:** independent rendering and unchanged tracked scope do not
   reconstruct the Worker's missing pre-work `CURRENT_RUN.md` comparison or
   rendering record. Preserve that historical limitation; do not invent it.

## Checks at complete delivery

Brain ran these inside the existing clean Verifier checkout at full commit
`d001895f2c474581359161f8c5134329aed2a0b5`, before writing this review:

| Command | Relevant actual output | Exit |
|---|---|---:|
| Python environment query | macOS-27.0.1-arm64-arm-64bit; Python 3.9.6 | 0 |
| `make audit` | All three audits pass; `Ran 118 tests in 0.795s`, `OK` | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard` | Hard/Classic; objective and map CONFLICTED; incomplete schedule; no move-safety guarantee | 0 |
| Same command with `--turn 6 --phase player` | Target enemy phase 6; conflict/incomplete coverage retained | 0 |
| Same command with `--turn 6 --phase enemy` | Target enemy phase 7; conflict/incomplete coverage retained | 0 |
| `git diff --check` | Empty output | 0 |
| Python sorted path/SHA-256 before/after comparisons | Canonical JSON set/content equal, 28 files; private set/content equal, 2 files; live run absent | 0 |
| `git ls-tree` / `git show origin/main:<path>` canonical comparison | Canonical JSON file sets and all contents equal to origin/main | 0 |
| `git status --porcelain` | Empty output after checks | 0 |

Private comparison included `CURRENT_RUN.md` and every regular file in
`state/`; no private contents or digests were published. Equality proves this
Brain check preserved that checkout. It does not reconstruct another seat's
historical private snapshot. Other-mode data is included in whole-file equality.
No rebuild was run. Tests establish repository invariants, not source truth.

`gh run list --branch verifier/006-chapter20-objective-2` exited 0. Successful
CI exists for both exact report and complete-delivery commits:
[Worker report checks](https://github.com/cntrl-alt-lenny/fire-emblem-awakening-assistant/actions/runs/37283937657)
and [complete delivery checks](https://github.com/cntrl-alt-lenny/fire-emblem-awakening-assistant/actions/runs/37284545133).
Passing CI does not resolve the provenance finding or authorize a merge.

Presentation check: bundled Node/marked and Playwright using installed Chrome
rendered the delivered evidence, this review and the new brief; exit 0,
heading counts 5/6/7, table counts 2/1/0, horizontal overflow false for each.
Brain inspected all three full-page screenshots: text/tables readable with
no clipping or overlap. A Python local-link scan of the two new documents
resolved their one local link; exit 0. Render files remained outside Git.

## Next action

Round 007 corrects the research artifact's evidence strength, retrieval
accounting and settings observation prerequisite, then receives a fresh blind
Verifier pass. It preserves canonical conflict and all gameplay gaps. A real
Hard/Classic capture remains unavailable and is a later observation task;
it is not required to deliver this correction honestly.

# Chapter 20 objective evidence

Research date: 2026-10-05. Corrected 2026-10-05 by
[round 007](../../007-chapter20-evidence/brief.md), superseding the evidence
assessment in round 006. Scope: Chapter 20 objective/completion disagreement
only. No game or save state was opened or changed. Original stamped reports
remain historical evidence and are not rewritten.

## Source trace

All fresh retrievals below occurred on 2026-10-05. Durable headings/fields are
the primary locators; reader lines are supplementary. Editorial text establishes
what a source asserts, not what the game displays or does.

| Source family / exact URL | Route and local locator | Recovered assertion | Scope and gaps |
|---|---|---|---|
| Fire Emblem Wiki: [chapter list](https://fireemblemwiki.org/wiki/List_of_chapters_in_Fire_Emblem_Awakening), registry `chapter_catalog` | Direct reader, Main story table, Chapter 20 row, Objectives column, line 41. Local `research/chapter_catalog.json`, Main story row Chapter 20; `tools/build_data.py` transfers the objective column. | `Defeat Walhart` | Catalog attribution recovered. Difficulty, mode, region and game version unspecified; no game objective display inspected. Line 40 is Chapter 19 and is not used as Chapter 20 evidence. |
| Gamer Guides: [Chapter 20](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-20-the-sword-or-the-knee), registry `p2_guide_20_1` | Direct reader, Note: Chapter 20 → Condition, line 332. Local `research/phase2/guide_20.json`, `guide_20_1`, Note: Chapter 20. Boss table follows, lines 335–341; Strategies for all Difficulties follows at line 342. | `Defeat every Boss` | Actual condition-field wording, not a boss-table inference or extraction error. No local difficulty label beside Condition. Guide-wide Hard default is separate; Classic, region and game version unknown. |
| Gamer Guides: [Reading This Guide](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/information/reading-this-guide), registry `p2_guide_scope` | Direct reader, Hard-default paragraph after example chapter fields, line 341; following general-strategy paragraph at line 343. | Guide declares Hard as its default and describes applicability to Normal. | Same family as Chapter 20. This declaration cannot override local headings or certify observed Hard/Classic behavior. |
| MKaykitkats contribution hosted by GameFAQs: [FAQ 64260](https://gamefaqs.gamespot.com/3ds/643003-fire-emblem-awakening/faqs/64260) | Indexed retrieval only: exact-URL site query with Walhart/commander terms. Chapter 20 `[WM20]`, metadata and starred footnote immediately after Excellus's skills, before the map. | `Mode: Normal/Hard/Lunatic`; `Condition: Defeat Boss`; `Walhart is the "commander", defeating him ends the level.` | Exact completion sentence freshly recovered with Chapter 20 context. Direct access was historically denied and was not retried. Index is partial and also includes other chapters, which are excluded. Editorial multi-difficulty assertion; Classic, region and game version unknown. Source independence unestablished. |
| Vandal: [Capítulo 20: Lucha o sumisión](https://vandal.elespanol.com/guias/fire-emblem-awakening/capitulo-20-lucha-o-sumision) | Direct reader, Chapter 20 → Victoria field, line 82; boss-order paragraph at line 85. | `Victoria: Derrota al comandante.` Translation: Victory: Defeat the commander. Strategy describes Cervantes and Excellus before Walhart. | Spanish editorial assertion, not a transcription of a visible game objective. Difficulty, mode, region/version unspecified. Boss order does not distinguish completion with surviving bosses. Independent derivation unknown. |
| CarefreeDude contribution hosted by GameFAQs: [board topic 65613896](https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/65613896) | Inherited unreproduced report: round 006 Verifier, blind-pass table, title and posts 1, 3, 7 (historical reader lines 119–138), retrieved 2026-10-05. One fresh exact-thread indexed lookup did not recover this thread. No direct retry. | Earlier Verifier reports that the player described completion with Cervantes and Excellus alive. No exact quotation is claimed recovered in round 007. | Reported observation mediated by the historical review; difficulty, mode, region/version, continuity and visible boss state unknown. Separate contribution on the same host as MK; independence and account accuracy unestablished. |

## Dependency assessment

MK indexed introductory context (`Starting a New Game [W000]`, Hard-default
note) and Gamer Guides' Reading This Guide Hard-default paragraph both use
`assumes you do Hard mode` and describe Normal as an easier version. The example
chapter-field structure and following general-strategy discussion also overlap.
These bounded observations support a dependency lead. They prove neither
copying, direction of reuse nor independent derivation. No recoverable lineage
statement was established in the inspected contexts; independence remains unknown.

Publisher, language, registry ID and named author distinguish retrieval origins,
not independent evidence. The catalog, Vandal and forum contribution also have
unestablished derivation. Gamer Guides pages, repeated extracts and index results
remain one family; MK index results remain MK evidence, not a new family. The
player contribution is a reported account, not independent verification of MK.
No count of independent corroborating sources is warranted.

## Claim matrix

| Question | Evidence category and assessment | Alternatives / gaps |
|---|---|---|
| Original objective attribution | Recovered catalog column says Walhart; recovered Gamer Guides Condition says every boss. The stored disagreement is traceable to source fields. | Source truth and game-displayed objective remain separate. |
| Game-displayed Hard/Classic objective | Unobserved. Catalog and Vandal offer editorial commander wording; Gamer Guides offers contrary condition wording. | No visible objective tied to Hard/Classic setup or known region/version. |
| Walhart-alone completion | MK explicitly asserts completion on Walhart's defeat in its multi-difficulty Chapter 20 section. Historical Verifier reports a player's surviving-boss account. | Editorial assertion plus unreproduced reported observation; dependency/setup unknown. Neither metadata nor Walhart's first boss entry establishes completion. |
| All bosses required | Gamer Guides explicitly asserts every boss in Condition. MK's completion assertion disagrees at the textual level. | No continuous game transition discriminates the requirements. Vandal's boss-order strategy does not do so. |

## Assessment and stopping point

Source attribution is resolved within the recoverable contexts. MK's sentence
is recovered in this round; an earlier Verifier's failure to retrieve it is
preserved as that review's limitation, not a finding that the sentence is false.
The available wording and historical player report suggest a Walhart-alone
interpretation, but cannot be counted as independent corroboration or verified
Hard/Classic completion. The actual displayed objective and completion condition
remain unresolved. Canonical conflict, confidence, incomplete schedules,
quarantine and coverage are unchanged; zero new verified gameplay coverage.

Stopped after the four bounded direct contexts (catalog, Gamer Guides chapter
and scope, Vandal), two indexed MK queries (completion and introductory scope),
and one exact-thread indexed lookup. Unrelated forum hits and other-chapter
snippets were excluded. No denied direct GameFAQs URL was retried; no broad
source hunt, footage download, game-file acquisition or access bypass occurred.
More guide agreement cannot replace missing observation.

## Single next observation task

Obtain and review one owner-supplied continuous Chapter 20 capture. First show a
settings/status or save-selection display that actually exposes both Hard and
Classic, visibly tied to the same save subsequently loaded for this chapter.
Establish that linkage continuously; a preparation screen alone is insufficient
unless it demonstrably shows both settings. Show the game's displayed objective,
then keep Cervantes and Excellus demonstrably alive through Walhart's defeat and
the uninterrupted chapter-completion transition. Record region/game version if
available; otherwise keep them unknown and do not assume regional equivalence.
Cuts, resets, hidden boss state, or either other boss dying before transition
prevent the required inference. This suitable capture remains unavailable;
no capture or game/save operation is authorized by this correction round.

Worker model family: GPT-6 per session instructions. Specific variant, reasoning
effort and speed settings are not inspectable; no owner-reported settings supplied.

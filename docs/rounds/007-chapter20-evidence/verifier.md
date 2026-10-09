<!-- fw-report
round: 007-chapter20-evidence
role: verifier
branch: verifier/007-chapter20-evidence
head: 07357188ae2b841a704e0e5e0e7fb4866cc3bded
os: macOS 27.0.1
python: 3.9.6
written: 2026-10-05T10:52:21Z
-->
Reviewed commit: `07357188ae2b841a704e0e5e0e7fb4866cc3bded`.
Review date: 2026-10-05. Environment: `macOS-27.0.1-arm64-arm-64bit`, Python `3.9.6`.
Model family: GPT-6 per session instructions. Specific variant, reasoning effort
and speed settings are not independently inspectable; no owner-reported settings
were supplied. This Verifier writes only this report and does not accept or merge.

## Findings

None. No demonstrated BLOCKER, SHOULD FIX or retained unproven claim presented
as recovered fact in the corrected assessment. Explicit unknowns are legitimate
research results rather than failures to resolve gameplay.

### Blind ordering and independent source work

Created the requested detached linked worktree inside the project, then ran
`python3 tools/fw.py start --role verifier --round 007-chapter20-evidence`
(exit 0). Output: `seat ok: verifier, round 007-chapter20-evidence, branch
verifier/007-chapter20-evidence at 07357188ae2b`; review pinned to the full commit
above. Read project rules, framework, role, tactical policy, standing decisions,
round 007 brief and round 006 brief. Inspected canonical baseline and relevant
coverage/source context before reading the changed evidence attachment, round
007 Worker report or round 006 reports/Brain review. Privately recorded the
source/baseline pass before comparison. A premature private note incorrectly
called the catalog inaccessible; its completed direct reader output had actually
recovered the Chapter 20 row during the blind pass. Corrected that note explicitly;
no public finding or conclusion relies on the mistaken access characterization.

Before checks, privately snapshotted sorted canonical JSON paths and separately
CURRENT_RUN.md plus every regular state file. The blind conclusion was recoverable
editorial disagreement, unknown independence, no observed Hard/Classic display or
completion, and preservation of the conflict. Only then opened and compared
artifacts and historical reviews. Inspected the full origin/main diff and the
round-specific diff from `1675abf9f657cec6c5c70be9479d9a5b05c0404e`.
Standing-decision changes versus main predate this Worker delivery; round 007
changes exactly the corrected attachment, correction record and Worker report.

Bounded retrievals on 2026-10-05, with inert URLs and durable local locators:

| Source, route and locator | Independently recovered result and limits |
|---|---|
| `https://fireemblemwiki.org/wiki/List_of_chapters_in_Fire_Emblem_Awakening`, direct reader, Main story Chapter 20 row, Objectives column, line 41 | `Defeat Walhart`. Chapter 19 is a separate row. Local `research/chapter_catalog.json:194-196` matches; `tools/build_data.py:160-163` transfers objective column 2. No difficulty/mode/region/version or game display proof. |
| `https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-20-the-sword-or-the-knee`, initially indexed in blind pass, later direct reader, Note: Chapter 20, Condition line 332 | `Defeat every Boss`. The Boss table and Strategies for all Difficulties are separate following contexts. Local `research/phase2/guide_20.json`, `guide_20_1`, preserves that condition; author_review.py constructs the historical conflict from it. Wording attribution reproduced; actual completion not established. |
| `https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/information/reading-this-guide`, direct reader, Hard-default paragraph after example chapter fields, lines 341/343 | Hard default and Normal applicability recovered. Local scope does not become an observed Hard/Classic sequence. Template and general-strategy paragraph compared with MK introductory contexts. |
| `https://gamefaqs.gamespot.com/3ds/643003-fire-emblem-awakening/faqs/64260`, original-URL indexed retrieval, Chapter 20 `[WM20]`, starred footnote after Excellus skills and before map | `Walhart is the "commander", defeating him ends the level.` Recovered with local multi-difficulty metadata and boss-star linkage during blind pass, before Worker comparison. Adjacent Chapter 19 quick-finish wording and later paralogue text excluded. MK editorial assertion, not game observation; Classic/region/game version unknown. |
| Same MK URL, indexed introductory contexts, Starting a New Game `[W000]`, Hard-default note; template and Tips discussion | Phrase `assumes you do Hard mode` and Normal applicability overlap Gamer Guides. Template structure and general-strategy discussion also recovered, the latter during comparison. This is a dependency lead; neither copying direction nor independent derivation established. Different publishers, languages or named authors do not establish lineage. |
| `https://vandal.elespanol.com/guias/fire-emblem-awakening/capitulo-20-lucha-o-sumision`, direct reader during comparison, Chapter 20, Victoria line 82 and boss-order paragraph line 85 | `Victoria: Derrota al comandante.` Translation reproduced as Victory: Defeat the commander. Strategy describes the other bosses before Walhart, which cannot distinguish completion with them alive. Difficulty/mode/region/version and independent derivation unknown. |
| `https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/65613896`, bounded exact-thread indexed lookup during comparison | Specific topic not recovered. Historical round 006 Verifier does record CarefreeDude posts 1/3/7 and the surviving-boss account. This verifies the correction's historical attribution only; no fresh forum quotation or observed setup claimed. |

Original GameFAQs search results included a robots-denial notice. No denied direct
URL was retried, alternate-host mirror opened or restriction bypassed. Indexed
results retain MK provenance. Search results surfaced unrelated chapters/sites;
only original scoped contexts above were used. Stopped after original catalog,
Gamer Guides chapter/scope, bounded MK completion/introduction/template queries,
Vandal and the exact-thread lookup. No broad new-source hunt, capture, download,
game/save operation or rebuild occurred.

### Comparison and acceptance criteria

1. Met. Retained assertions have exact URLs, durable headings/fields, route/date,
   family and explicit scope limits. Recovered quotes versus inherited forum
   observation are distinguished. Original extraction attribution independently
   reproduced; no other-chapter snippet supplies Chapter 20 scope.
2. Met. Independence claims removed throughout trace, matrix, assessment and
   stopping narrative. Introductory overlap is reproduced as an unresolved lead;
   catalog, Vandal and player derivation receive the same conservative standard.
3. Met. MK completion sentence recovered neutrally at its local footnote, rather
   than inferred from boss order/metadata. Player account remains inherited and
   unknown-difficulty; earlier retrieval limitation is preserved as historical.
4. Met. Editorial attribution, displayed objective and actual completion are
   separated. Canonical confidence/conflict and zero gameplay coverage gain remain.
5. Met. One next task requires an actually settings-bearing display continuously
   tied to the same save, objective, both other bosses alive through Walhart defeat
   and completion; cuts/resets/hidden state and unknown region/version explicit.
   It does not assume preparation exposes settings or authorize game operations.
6. Met. Correction record maps every material historical finding. Original brief,
   stamped reports and Brain review byte-identical to the round starting commit.
   New comparisons cannot reconstruct another seat's missing old private evidence.
7. Met for this exact delivery. Checks/preservation and rendering below reproduced.
8. Met. Fresh blind source/baseline pass recorded before comparison, followed by
   exact-commit claim review and independent checks. Only this report is written.

Worker comparison: required repository outcomes and correction claims agree with
my independent observations. Worker audits were explicitly at its full evidence
commit before a report-only commit; my checks are at the complete Worker delivery.
Worker private snapshots and original render session cannot be retrospectively
inspected; my independent worktree checks reproduce the delivered invariants,
not another seat's historical actions. There are no new tests in this docs round.

### Exact-commit checks and preservation

Commands below ran at the reviewed full commit before writing this report:

| Command | Relevant actual output | Exit |
|---|---|---:|
| Python platform/version query | `macOS-27.0.1-arm64-arm-64bit`, `3.9.6` | 0 |
| `make audit` | Three audits `passed: true`; Hard audit `campaign_maps: 44`, `reinforcement_records: 29`, `registered_sources: 217`, `source_refs_resolve: true`, `source_truth_not_proven_by_tests: true`; `Ran 118 tests in 0.936s`, `OK`. Verified safe schedules: 0. | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard` | Hard/Classic; map/objective CONFLICTED; catalog/guide conflict retained; `schedule_complete: false`, `safe_to_claim_move_safe: false`, target enemy phase null. | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase player` | `target_enemy_phase_turn: 6`; same conflict, incomplete schedule and no safety guarantee. | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase enemy` | `target_enemy_phase_turn: 7`; same conflict, incomplete schedule and no safety guarantee. | 0 |
| `git diff --check` | Empty output. | 0 |
| Python sorted-path/SHA-256 before/after comparison | Data count 28 equal True; private count 2 equal True; live run absent. | 0 |
| `git ls-tree -r --name-only <ref> data`, `git show <ref>:<path>` via Python | Canonical JSON file sets/content match both round starting commit and origin/main, 28 files. Includes all other-mode records. | 0 |
| `git diff --exit-code <starting-commit> HEAD -- <historical-artifacts>` | Empty output; original round 006 brief, Worker/Verifier reports and Brain review preserved. | 0 |
| Python Markdown local-link scan of changed attachments | `local links 2 all resolve` | 0 |
| Bundled Node `--input-type=module` render heredoc: marked + Playwright Chromium using installed Chrome | `evidence { headings: 6, tables: 2, overflow: false }`; `correction { headings: 1, tables: 1, overflow: false }` | 0 |
| `git status --short` before report | Empty output. | 0 |

Rendered both attachments from the committed source bytes into private temporary
HTML/PNG files outside Git; visually inspected both complete screenshots. Tables,
prose, code and links are readable without clipping or overlap. No software installed.

Preservation method executed privately before checks and recomputed afterward:

```python
from pathlib import Path
import hashlib, subprocess

def snapshot(paths):
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths) if p.is_file()}
data = snapshot(Path('data').rglob('*.json'))
private = snapshot([Path('CURRENT_RUN.md'), *Path('state').rglob('*')])
# Serialize privately before checks, recompute and assert dictionary equality after.
for ref in ('1675abf9f657cec6c5c70be9479d9a5b05c0404e', 'origin/main'):
    paths = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', ref, 'data'], text=True).splitlines()
    old = {p: hashlib.sha256(subprocess.check_output(
        ['git', 'show', ref + ':' + p])).hexdigest()
        for p in paths if p.endswith('.json')}
    assert old == data
```

No private contents, hashes or personal filesystem paths published. Equality is
for this linked Verifier worktree only; main-checkout ignored state was not inspected.

## Not verified

No game-displayed Hard/Classic objective or continuous surviving-boss completion
was observed. Suitable owner-supplied capture remains unavailable. Region/game
version equivalence, source accuracy and independent derivation remain unknown.
Forum text was not freshly recovered; only its historical review attribution
checked. New preservation/rendering cannot recreate old missing private snapshots
or historical render evidence. Structural checks do not certify game mechanics,
complete schedules or whole-map safety.

## Verdict

No demonstrated blocker in the bounded evidence correction. High confidence that
retained source wording, unknown independence and historical limitations are
represented conservatively, production records are unchanged, and the CLI still
exposes Chapter 20 conflict and incomplete coverage. Actual Hard/Classic completion
remains unresolved. This informs Brain's exact-commit review and does not accept
or merge. Exactly one next observation task remains: review one owner-supplied
continuous Chapter 20 capture establishing settings tied to the same save, displayed
objective, both Cervantes and Excellus alive through Walhart defeat and immediate
completion, with region/version and cuts/resets/hidden state handled explicitly.

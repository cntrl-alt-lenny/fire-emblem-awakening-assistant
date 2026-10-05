<!-- fw-report
round: 006-chapter20-objective
role: verifier
branch: verifier/006-chapter20-objective-2
head: c32b3a00dbd6c33b111aca46275deade5a984f77
os: macOS 27.0.1
python: 3.9.6
written: 2026-10-05T08:35:07Z
-->
Reviewed commit: `c32b3a00dbd6c33b111aca46275deade5a984f77`.
Review date: 2026-10-05. Environment: `macOS-27.0.1-arm64-arm-64bit`, Python `3.9.6`, Clang `21.0.0`. Model family: GPT-6 per session instructions; specific model variant, reasoning effort and speed settings are not inspectable. No owner-reported settings were supplied.

## Findings

- [UNPROVEN CLAIM] `docs/rounds/006-chapter20-objective/attachments/objective-evidence.md:17` — `independently authored GameFAQs walkthrough` and `Walhart is the ‘commander’, defeating him ends the level`. Direct retrieval of the cited MKaykitkats FAQ returned `Failed to fetch restricted URL`. A bounded indexed lookup recovered the local Chapter 20 `[WM20]` header, `Mode: Normal/Hard/Lunatic`, `Condition: Defeat Boss`, and Walhart's first boss entry, but did not recover the quoted completion sentence. No direct retry or bypass followed the restriction. The exact completion quote is therefore not independently reproduced in this review. Neither a boss list nor this metadata proves Walhart-alone completion.
- [SHOULD FIX] `docs/rounds/006-chapter20-objective/attachments/objective-evidence.md:20` — source-family accounting does not investigate the brief's explicit possible MK/Gamer Guides overlap. Indexed MK introduction wording closely matches Gamer Guides' Hard-default introduction; this is a dependency lead, not proof of copying or authorship. Different hosting sites cannot establish independent derivation. Qualify MK independence as unestablished until lineage is checked; otherwise the claimed independent multi-difficulty support at lines 26–28 is overstated. The separate player's first-person report remains a separate contribution with unknown setup. This does not justify removing the canonical conflict.
- [NOTE] `docs/rounds/006-chapter20-objective/attachments/objective-evidence.md:32` — the observation plan appropriately requires both other bosses alive when Walhart dies, continuous completion, displayed objective and visible Hard/Classic setup. Hard/Classic evidence must come from a settings/status display tied to the same save; a chapter preparation screen alone may not expose those settings. This is an observation prerequisite, not a gameplay resolution.

### Blind first pass and source re-derivation

Started with the requested detached worktree and `python3 tools/fw.py start --role verifier --round 006-chapter20-objective` (exit 0). Output pinned the review to the full commit above on `verifier/006-chapter20-objective-2`. Read the project rules, full tactical policy, standing decisions and brief, then inspected baseline records, extraction/code and original source contexts. Did not open `worker.md` or `attachments/objective-evidence.md` until completing and recording the independent first pass in a temporary private note. The first-pass conclusion was: attribution recoverable; Hard/Classic display and completion unobserved; preserve the conflict. Then read the Worker artifacts and compared their material claims.

Source retrievals below were on 2026-10-05. URLs and excerpts are inert code, not live links. Reader line numbers supplement durable local headings.

| Source / locator | Independently recovered evidence | Scope / limitation |
|---|---|---|
| `https://fireemblemwiki.org/wiki/List_of_chapters_in_Fire_Emblem_Awakening`, Main story, Chapter 20 row, Objectives column, reader line 41 | `Defeat Walhart`; local extract `research/chapter_catalog.json:194-196` matches. `tools/build_data.py:160-163` transfers row column 2 into the canonical objective. | Fan catalog family; no difficulty/mode/region/version or observed objective screen. |
| `https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-20-the-sword-or-the-knee`, Note: Chapter 20, Condition, lines 326–342 | `Condition: Defeat every Boss`; three names appear in a separate Boss table; `Strategies for all Difficulties` is a separate following heading. Local `research/phase2/guide_20.json`, `guide_20_1`, preserves the condition. `research/hard_verification/author_review.py:108-109` creates the historical hazard/conflict. | Gamer Guides family; condition itself has no difficulty label. Actual source attribution is resolved; actual game behavior is not. No translation or boss-list inference needed. |
| `https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/information/reading-this-guide`, line 341 | Source explicitly assumes Hard mode. | Independently read the source declaration, rather than relying only on registry metadata. Local all-difficulties strategy heading is preserved; neither establishes region/version/Classic or a captured objective. |
| `https://gamefaqs.gamespot.com/3ds/643003-fire-emblem-awakening/faqs/66466?page=1`, arvilino, Chapter 20, lines 391–395 | `Cervantes and Excellus are also Bosses but you don't need to fight them.` | Additional blind-pass contrary guide lead: Table of Contents scopes this walkthrough to Lunatic (lines 130–134). Do not promote it to Hard evidence. Different named author is not proof of complete source independence. |
| `https://gamefaqs.gamespot.com/boards/643003-fire-emblem-awakening/65613896`, title and CarefreeDude posts 1, 3, 7, lines 119–138 | Title reports Chapter 20 cleared leaving both other bosses alive; post 3 describes Cervantes trapped and Excellus pursuing a chest opener; post 7 reports ordinary subsequent story. | First-person reported observation, not visible footage. Difficulty, mode, region/version and uninterrupted state cannot be determined. Supports a reported counterexample, not verified Hard completion. |
| `https://vandal.elespanol.com/guias/fire-emblem-awakening/capitulo-20-lucha-o-sumision`, Chapter 20, lines 82–85 | `Victoria: Derrota al comandante.` Translation: Victory: Defeat the commander. Text describes defeating the other bosses before Walhart. | Spanish editorial guide; difficulty/mode/version unknown. No objective screenshot inspected. Does not discriminate whether the other bosses can survive completion. Worker translation and caveat reproduced. |
| `https://gamefaqs.gamespot.com/3ds/643003-fire-emblem-awakening/faqs/64260`, indexed `[WM20]` metadata | Chapter 20, Normal/Hard/Lunatic, Defeat Boss and Walhart entry recovered. Direct page unavailable. | Same MK source family whether indexed or direct. Exact completion quote and independence remain unproven as noted above. No denied-source retry. |

Stopped after original catalog/guide/scope, one bounded independent-lead query, arvilino and the player's report, then the Worker's Vandal/MK contexts. No footage was downloaded, game opened, source restrictions bypassed or run initialized. More copied summaries would not establish a visible Hard/Classic completion transition.

### Exact-commit checks and preservation

Commands executed at the reviewed commit before writing this report:

| Command | Relevant real output | Exit |
|---|---|---:|
| `make audit` | Data validation `passed: true`; phase-two `passed: true`; Hard audit `passed: true`, `campaign_maps: 44`, `reinforcement_records: 29`, `registered_sources: 217`, `source_truth_not_proven_by_tests: true`; `Ran 118 tests in 1.218s`, `OK`. Complete tactical schedules remain unverified. | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard` | Hard/Classic, map and objective `CONFLICTED`, objective value `Defeat Walhart`, target enemy phase null, `schedule_complete: false`, `safe_to_claim_move_safe: false`. | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase player` | Target enemy phase 6; same objective/conflict/incomplete schedule. | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase enemy` | Target enemy phase 7; same objective/conflict/incomplete schedule. | 0 |
| `git diff --check` | Empty output. | 0 |
| `git diff --name-only 6ab0e77..HEAD` | Only round 006 `attachments/objective-evidence.md` and `worker.md`. | 0 |
| `git show 6ab0e77 -- docs/state.md` | Standing-decision edits belong to the preceding Brain brief commit, not Worker implementation. They retain parked gameplay uncertainty and add central inventory uncertainty; no decision removed by Worker. | 0 |

Before audit/source work, a Python SHA-256 snapshot recorded sorted `data/**/*.json`, separately `CURRENT_RUN.md` and every regular file under `state/`. Digests stayed outside public artifacts. The same snapshot code ran after checks: `canonical JSON set/content SHA-256 equality True count 28`; `private set/content SHA-256 equality True count 2 live run False` (exit 0). Whole-file equality includes every other-mode record. Also compared the canonical JSON set with `git ls-tree -r --name-only origin/main data`, and each file's bytes with `git show origin/main:<file>`: file sets equal and all contents equal (exit 0). No rebuild was run. Preservation is for this Verifier worktree; the main checkout's ignored state was not inspected or operated on.

Reproducible snapshot expression used within `python3 - <<'PY'`:

```python
from pathlib import Path
import hashlib
root = Path('.')
def snapshot(paths):
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths if p.is_file()}
canonical = snapshot(sorted(root.glob('data/**/*.json')))
private = snapshot([root / 'CURRENT_RUN.md'] + sorted((root / 'state').rglob('*')))
# Save privately before work; recompute after work and compare dictionaries.
# Print counts/equality/live-run presence only, never private hashes or contents.
```

Rendered the research attachment using bundled `marked` and Playwright with installed Chrome, via a temporary script outside the repository. Successful command: `node /tmp/fea006-render.cjs` using the bundled runtime (exit 0): `rendered headings=5 tables=2`. Inspected the full-page screenshot: both tables, prose, code spans and links render without clipping or overlap. Initial launch using Playwright's default browser failed because that browser executable was absent (exit 1); using installed Chrome resolved it without installing software. A Python Markdown-link scan checked the brief's one local link and the attachment's zero local links: all resolve (exit 0). Nothing except this report was written in the repository.

An initial local catalog inspection incorrectly assumed a dictionary rather than its list structure (exit 1, `AttributeError`); subsequent direct line inspection recovered the correct Chapter 20 row. No production change or source conclusion depended on that failed helper.

### Acceptance-criterion assessment

1. Met for original source attribution, exact URLs, locators/date and local extraction context. Hard-default declaration was additionally re-read; metadata versus strategy scope is preserved.
2. Matrix present and conservatively distinguishes editorial objective and reported completion from game observation. Independence accounting needs the qualification above.
3. Met as bounded research with explicit insufficient observation: the first-person player report is relevant but lacks difficulty; suitable footage is not required to exist. The added Lunatic guide was kept separate.
4. Met: unresolved gameplay result plus a discriminating observation plan, no proposed canonical adoption.
5. Met by independent equality checks and CLI behavior; no coverage gain or canonical mutation.
6. Met: fresh session, blind first pass, exact-commit comparison, required checks and preservation rerun.
7. Rendering and local links independently checked; exactly one bounded next task and honest settings limitations retained.

## Not verified

The game's displayed Hard/Classic objective and Walhart-alone map completion were not observed. No continuous capture ties Hard/Classic setup, both other bosses alive and the victory transition together. Region/version equivalence is unknown. Editorial agreement cannot establish those facts. MK's precise quoted completion sentence and its independence from Gamer Guides could not be reproduced; restricted access was respected. The Worker does not record a rendering command/result or a separate `CURRENT_RUN.md` preservation comparison; independent rendering and tracked unchanged scope reduce these documentation gaps but do not reconstruct its private pre-work snapshot. Tests certify repository behavior, not external source truth or complete map safety.

## Verdict

No demonstrated blocker in the research-only delivery. High confidence that original attribution is resolved, canonical records remain unchanged and the CLI still exposes the conflict. Moderate confidence that the available reports favor Walhart alone; low confidence in any claim of verified Hard/Classic completion, which the Worker correctly withholds. Brain should qualify the unproven MK quotation/independence before relying on its multi-difficulty corroboration. This review neither accepts nor merges. Recommend exactly one next task: obtain and review one owner-supplied continuous Chapter 20 capture showing Hard/Classic settings tied to that save, the displayed objective, both Cervantes and Excellus alive through Walhart's defeat, and the immediate completion transition, recording region/version when available. That capture is the unavailable input; do not initialize or alter a player run to manufacture it.

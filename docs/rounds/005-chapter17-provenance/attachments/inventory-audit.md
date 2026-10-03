# Chapter 17 Hard inventory provenance — 2026-10-03

This audit changes inventory attribution and uncertainty, not the actual arrival schedule. No new game observation or independently verified gameplay coverage is claimed.

## Recoverable lineage

Base: `a97ee2d8a528d7f8fef62b06978a3c3861599e69`.

`data/chapters/hard_reinforcements.json` → `records[id=hard_chapter_17_first|second|central].units` is copied by `tools/hard_data.py:main` from `research/hard_verification/reviewed.json` → `maps[id=chapter_17].waves[id=...].units`. `hard_tactics.json` contains wave references and aggregate sources, not a second inventory. `make rebuild` consumes reviewed inputs; it does not run the author.

`research/hard_verification/author_review.py` constructs these waves in its Chapter 17 loop. Its `u()` literals supplied class/count/equipment; `w()` credited three sources collectively and defaulted nonempty units to SUPPORTED. The later generic loop replaced inventory notes. This obscured differences between sources without adding evidence.

`git log --follow` for both author and reviewed input reaches only root commit `cf17834fd6a8867d06c25faa772a5d8700f32167` (2026-10-03), “Publish Awakening tactical reference and offline tools.” In that commit, author line 92 and reviewed `maps[17].waves[2].units.value` already contain the central six-unit literal: three Heroes/Silver Sword, two War Monks/Silver Axe, one Sniper/Silver Bow. The same root commit's canonical central record contains it. There is no parent commit, captured source row or author explanation establishing its external origin. Historical presence is not factual support. The first/second four-unit literals also enter there.

The older `research/phase2/guide_16.json`, record `guide_16_2`, retains a boss table and map metadata, not a reinforcement composition. `reviewed_additions.json` has no Chapter 17 inventory. Neither supplies the missing six-unit origin. No cause such as transcription error or mode conflation is asserted without evidence.

## Independently inspected contexts

All three existing family contexts were revisited on **2026-10-03**, with round 004 used only as secondary comparison material. Retrieval is bounded to those pages and the specific indexed subsection. No denied access retry, bulk archive, footage search or assets.

- **F:** [Fandom Inexorable Death](https://fireemblem.fandom.com/wiki/Inexorable_Death), `Reinforcements / Hard Mode`, indexed rows labelled turns 8, 9, 10. Public index only; direct access remains unavailable. Family `fandom_editors`. Explicit Hard heading; Classic/Casual and region/version unspecified. Indexed enemy-turn wording is a source report, not observation of this event. Later rows remain excluded; the original excerpt lost their mode boundary.
- **G:** [Gamer Guides Chapter 17](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/chapter-14-to-endgame/chapter-17-inexorable-death), `Strategies for all Difficulties`, final paragraph; direct public reader. Guide dated 2013-06-05, updated 2020-12-29. `p2_guide_16_2` and `p2_survey_16_2` share this URL and publisher family (`gamerguides_vincent_lau`); they are not two corroborations. Local all-difficulties scope overrides the guide-wide default. It describes warning and stairs, without an inventory or phase/version/mode identification.
- **J:** [Pegasus Knight Chapter 17](https://www.pegasusknight.com/wiki/fe13/%E3%83%9E%E3%83%83%E3%83%97%E6%94%BB%E7%95%A5/%E7%AB%A0%E5%88%A5%E6%94%BB%E7%95%A5/17%E7%AB%A0%2B%E6%AD%BB%E3%81%AE%E9%81%8B%E5%91%BD), direct public reader, `コメント`, anonymous **2012-04-27 11:57:31**, explicitly Hard. Family `pegasus_original_player_comments`. Own translation: roughly three turns after Say’ri's warning, four arrivals emerge from four left stairs, including a Sniper. No full class counts, equipment, phase or wave ordinal. Language/date do not establish region/version; Classic/Casual unspecified. The `初期配置` enemy list is initial placement, not a reinforcement inventory. The Hard-labelled 2014-09-06 comment concerns activation/possible stair blocking, not composition. Nearby unlabelled comments, including 2014-02-09, cannot be assigned to Hard.

## Field-level comparison and disposition

F rows below supply source-reported attributes only. Levels visible in that index are not newly adopted; existing null levels remain unknown. G supplies none of these inventory attributes. J supplies only the partial overlap described above, with no unambiguous mapping to a stored wave.

| Stored inventory | Class | Count | Equipment | Exact supporting locator | Decision / remaining gap |
|---|---|---:|---|---|---|
| first | Hero | 2 | Silver Sword | F Hard turn-8 row, two Hero entries | Retain as single-source SUPPORTED report |
| first | War Monk | 1 | Silver Axe | F Hard turn-8 row | Same |
| first | Sniper | 1 | Silver Bow | F Hard turn-8 row | Same; J mentions a Sniper but not this count/equipment |
| second | Hero | 2 | Silver Sword | F Hard turn-9 row, two Hero entries | Retain as single-source SUPPORTED report |
| second | Sniper | 1 | Silver Bow | F Hard turn-9 row | Same |
| second | War Monk | 1 | Silver Axe | F Hard turn-9 row | Same |
| central, inherited | Hero | 3 | Silver Sword | Root author/reviewed/canonical literal only | Unsupported historical alternative |
| central, inherited | War Monk | 2 | Silver Axe | Same | Same |
| central, inherited | Sniper | 1 | Silver Bow | Same | Same |
| central, indexed alternative | War Monk | 1 | Silver Axe | F Hard turn-10 row | Competing source report; actual inventory unresolved |
| central, indexed alternative | Hero | 1 | Silver Sword | F Hard turn-10 row | Same |

First and second unit claims now credit **only `hr_fandom17`**. G's stairs description and J's four-arrival/Sniper overlap cannot corroborate every class/count/equipment attribute. They remain credited on timing/location and containing records because those fields were outside this amendment.

Central `units.value` is null with confidence CONFLICTED; both alternatives are preserved in notes. Its source ID identifies the indexed alternative only, not external proof of six. Neither a failed reproduction nor access availability chooses the actual count. Null means unknown, never zero. The parent wave remains PARTIAL because its other claims are unchanged; the map and first staircase conflict remain CONFLICTED. The current-map consumer places the central inventory among uncertain claims, with both alternatives visible.

## Regeneration and scope

Targeted final inventory assignments follow the author's generic note rewriting so fresh authoring cannot erase their limits. The offline producer already preserves those claims, so no claim-producing or tactical-tool feature change is needed. The producer source-document introduction alone now distinguishes original access dates from the Chapter 17 reinspection. Source registry amendments are limited to F's inventory discrepancy/access date and J's inventory/region limitations/access date. No other source entry changes.

The 44-map/29-wave counters and zero complete verified schedules stay unchanged. This is a downgrade of one unit claim, not new tactical coverage. All Chapter 17 timing, location, phase, immediate action, suppression, coordinates, skills and conflict remain identical as JSON fields; unrelated maps/modes and quarantine are checked separately. Regressions test attribution, central query uncertainty across four phase queries, and isolated fresh-author output, not external source truth.

## One bounded next task

Obtain and review one lawful, clearly Hard-labelled observation of the central Chapter 17 arrival, with visible units/equipment, warning/setup, phase and region/version (and Classic/Casual where available). Compare its composition with both retained alternatives without assuming a fixed turn. **That observation is unavailable in this round.** Repeated guide comparison cannot resolve actual composition or complete-map safety.

## Documentation inspection

Rendered all five changed Markdown documents with the installed marked renderer and inspected them in the hidden local browser: inventory matrix, STATUS addition, uncertainty addition, reinforcement limits/conflicts and source registry. Table columns and paragraphs were readable without overlap. All three relative links in changed documents resolved to the inventory audit. Rendering and link checks validate presentation only, not source facts.

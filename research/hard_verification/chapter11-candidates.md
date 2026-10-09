# Chapter 11 fort candidate assessment — 2026-10-09

## Source wording and scope

Read through the public web reader on 2026-10-09, without authentication,
mirrors or access bypass:

| Registry ID | Route and locator | Bounded finding |
|---|---|---|
| `p2_guide_12_0` | [Chapter 11](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/beginning-to-chapter/chapter-11-mad-king-gangrel), strategy paragraph after chest/thief advice and before Gangrel’s movement paragraph (reader line 363) | Warns about enemy-turn arrivals and turn-3 positioning; occupying forts blocks arrivals, with southern forts reachable by turn 3. |
| `p2_guide_12_0` | Following paragraph (reader line 365) | Separately reports three northwest arrivals on turn 4, explicitly labelled Hard. |
| `p2_guide_scope` | [Reading This Guide](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/information/reading-this-guide), paragraph after the chapter-field example (reader line 341) | Declares Hard as the walkthrough default. Its suggestion about Normal is not adopted as Normal timing evidence. |

Both pages belong to one publisher/author family, not independent corroboration.
Classic/Casual, game region and game revision are unspecified. Guide metadata
lists publication 2013-06-05 and update 2020-12-29; these are not game versions.
No recurrence, final turn, complete fort inventory or complete schedule is given
in the bounded text. No gameplay footage, save or game script was examined.

## Interpretation and representation

The inherited note says arrivals are expected from turn 3 but its fixed `[3]`
encoding hides the fort family at later target phases. That encodes an unsupported
closed schedule. The source itself gives a turn-3 warning rather than an explicit
statement that every later turn has a spawn.

Preserve `hard_chapter_11_t3_forts` as an unresolved `conditional_report`, with
`reported_start_turn: 3`, `turns: null` and `repeat: null`. The start is an
interpretation of the warning. Timing confidence is PARTIAL rather than SUPPORTED
for the former exact-turn representation; the supported location claim is retained.
Queries keep this family from target enemy phase 3 onward. Its presence means
possible unresolved arrivals, not a spawn prediction; a late query does not
establish that any wave remains. Before that boundary, the general incomplete
schedule warning still prevents an absence conclusion.

The northwest report remains separately fixed at turn 4. No inference is made
about overlap between that report and the fort family. Unknown counts, classes,
equipment, coordinates and skills remain unknown. Fort suppression and ordinary
Hard immediate-action claims retain their existing limits.

## Observed gameplay and coverage

No gameplay was observed. Regression results establish query behavior only.
There remain zero certified complete schedules, no newly verified gameplay
coverage, and no whole-map safety guarantee. Other difficulties and quarantined
records are unchanged. See [reinforcement policy](../../docs/hard-reinforcements.md)
and [coverage counters](coverage_counts.json).

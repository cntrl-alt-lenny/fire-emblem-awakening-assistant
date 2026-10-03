# Awakening Hard / Classic reinforcement evidence

**Ordinary Hard reinforcements can move and attack immediately when they appear at the beginning of enemy phase. They can kill on that same phase.** The Hard-specific [Gamer Guides rules explanation](https://www.gamerguides.com/fire-emblem-awakening/guide/intro-and-gameplay/gameplay/starting-a-new-game) (`hr_gg_spawn`) and an independent [Hard player report](https://gbatemp.net/threads/fire-emblem-awakening-reinforcements.435653/) (`hr_hard_spawn_observation`, public indexed excerpt) corroborate this Awakening-specific rule. General-rule confidence: VERIFIED. The community thread is corroboration, not a controlled event-script test; direct access was restricted and was not bypassed.

Classic makes a resulting death permanent unless the player explicitly resets. Casual does not change a Hard enemy into a Normal enemy or establish different reinforcement timing.

This rule does **not** establish the exact phase of every scripted arrival. Phase-unconfirmed map events remain UNKNOWN. Every ordinary-arrival immediate-action claim is a **conditional application** of the general rule, not an observation of that individual wave. No map has a complete audit excluding all scripted exceptions. Conservatively treat an unconfirmed arrival as potentially able to attack immediately; that is a safety policy, not a newly verified mechanic.

## Turn conventions

A reported “turn 5” can mean player phase 5, beginning of enemy phase 5, or an end-of-phase arrival. Preserve the actual source wording; never shift a table by one turn to make sources agree. Unlabelled Japanese end-of-enemy-phase tables are not imported as Hard merely because they share a map name. Difficulty-specific headings can be lost by indexed excerpts.

`map_info.py --chapter 7 --difficulty hard --turn 5 --phase player` targets the next enemy phase **5**. If currently in enemy phase 5, `--phase enemy` targets enemy phase **6**. Phase is mandatory when a turn is supplied. The older `tactical_query.py` explicitly targets the following numbered turn N+1; it is retained for compatibility and is not the preferred Hard reference.

Fixed-turn supported records are filtered to that phase number. Conditional, relative-warning, repeated or unknown-timing events remain candidates on every query. A returned candidate is not a prediction that its condition is satisfied. A wave not returned by the fixed-turn filter does not establish an empty map schedule.

## Evidence and independence

VERIFIED requires strong game-derived evidence or independent credible corroboration. SUPPORTED preserves a specific good single source. PARTIAL means important details missing; CONFLICTED retains alternatives; UNKNOWN uses null rather than invented values. Parent confidence applies to supplied attributes only: a null equipment, count, class, location or skill remains unknown. Map completeness is scored separately from individual facts.

Gamer Guides' [scope declaration](https://www.gamerguides.com/fire-emblem-awakening/guide/story-walkthrough/information/reading-this-guide) establishes Hard as its default. Explicit Lunatic sections are excluded. All mirrors and repeated registry entries are one family; similarities to MK's guide are not independent verification. Guide objective errors have been caught, so vague victory descriptions never override a contradicted chapter catalog without investigation. Pegasus Knight explicitly Hard-labelled original comments are dated Japanese-release observations; unlabelled enemy data are not Hard evidence. No regional equivalence is silently presumed for a conflicting schedule. No footage was used as observational proof without establishing difficulty/state.

## Resolutions and outstanding conflicts

- **Chapter 15 import error:** old Hard turn-4/5/6 rows match Chapter 16's separately headed Lunatic mixture. They and the associated activation assertion are quarantined. Chapter 16's explicit Hard subsection instead supports eight/four/four arrivals. Chapter 15 absence has separate single-source Hard-labelled Japanese support. This is an extraction error, not evidence of two valid Hard schedules.
- **Chapter 5:** western Hard excerpt's turns/classes differ from a dated Hard-labelled Japanese report; table/prose also differ. Full alternatives remain CONFLICTED. Do not guard just one turn or just ground approaches.
- **Chapter 17:** guide/index describe eastern first stairs; Hard-labelled Japanese observation reports left stairs first, about three turns after warning. Retain both sides and unknown warning trigger; indexed turns 8/9/10 are conditional reports, not guaranteed fixed turns. Later excerpt rows with a lost mode boundary are excluded.
- **Chapter 7:** the earlier Hard-versus-Lunatic level discrepancy does not invalidate a separately scoped Hard claim. Hard level 7 is supported; do not import Lunatic level 9, random skills or stats.
- **Objectives:** conflicting boss/rout/defend descriptions for Prologue, Chapters 1, 2, 6, 9 and 20 remain exposed. Chapter 15 rout is preferred against the guide's boss shorthand using the catalog and Japanese chapter reference. Check the game's displayed objective before recommending a boss rush. Paralogue 3's all-villagers-dead failure versus reward consequence is UNKNOWN.

## Spawn blocking and important events

Supported blocking claims exist for Chapter 11 forts, Chapter 19 forts, Chapter 23 stairs and Paralogue 10 stairs. Exact tiles and universal applicability are not certified: occupying a likely tile does not remove every other threat. Event claims include Severa talking to Holland, village visits, faction choices, warning-relative southern arrivals, Tiki targeting and changing walls. No nonexistent coordinate system has been imposed on descriptive map locations.

Absence itself is SUPPORTED on Chapters 15 and 22. It is not game-script VERIFIED; the query reports it as reasonably supported but never sets its stronger certainty flag from a single source. Reinforcement status on other maps with no positive evidence is UNKNOWN, not “none.”

Ordinary campaign coverage counts 44 fixed maps. Premonition is a separate tutorial; procedural world-map skirmishes have no fixed enemy schedule here and require actual map/enemy observations. SpotPass bonus paralogues, DLC and multiplayer content are separate. The query refuses those rather than substituting a story map.

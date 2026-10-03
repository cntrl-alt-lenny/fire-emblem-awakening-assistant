# EXP and progression support

`tools/experience.py` requires actual internal level, difficulty, enemy displayed level/class/promotion, explicit unit category and boss flag, engagement count and battle result. It does not infer any of these from a map template. Sources: `calculations`, `p2_exp_empirical`, `p2_exp_staff_empirical`. The forum observations are the origin of the Serenes calculations, not independent confirmation.

Let LD = enemy displayed level +20 if promoted − player internal level. Taguel/Manakete/Dancer and other special classes do not gain the promoted offset solely from their level cap. Child units use their actual class/level and known seal history; no special guessed child EXP modifier is inserted.

| LD | Damage component | Kill component |
|---|---|---|
| ≥0 | floor((31+LD)/3) | 20+3LD+character bonus |
| −1 | 10 | 20+character bonus |
| ≤−2 | max(floor((33+LD)/3),1) | max(26+3LD+character bonus,7) |

A lead kill receives both components; chip receives damage component; no damage receives0. Boss bonus adds20 to character bonus. Class bonuses: Thief/Assassin/Trickster/Conqueror20, Revenant/Entombed80, Troubadour/Cleric/Priest−10, other classes0. Deadlord/Einherjar unit bonus20 and Harvest Scramble ordinary enemy bonus0 constrain the combined unit/class bonus to no greater than the unit bonus; ordinary enemies use class bonus directly. Category/boss flags must be supplied, not inferred. Awards clamp to100 and applicable positive minimums.

Support EXP uses its own damage component, multiplied by1 for its final blow and½ otherwise. Fractional support and Veteran/Paragon rounding order remains unverified; the default refuses those cases rather than silently choosing. Veteran needs actual active Pair Up; Paragon doubles EXP. Explicit interpretation flags expose the adopted rounding and never make it a verified game fact.

Lunatic/Lunatic+ repeated engagement count includes this battle against the same enemy. The published signed term conflicts with the explanatory reduction after the third engagement. For T≥4 default calculation refuses. `allow_interpreted_lunatic_penalty` explicitly selects max(T−3,0), deducted from chip EXP down to0; this is documented interpretation. Do not report it as confirmed exact EXP.

Staff/Dance: floor(base − max(internal level−5,0)/3 + ordinary-unpromoted bonus + exception), clamped1..100. Ordinary-unpromoted bonuses are Normal8, Hard3, Lunatic/Lunatic+0. Dancer receives no such bonus and base17. Exceptions are−1 at internal levels8/11 and+1 at30. Subtracting ceil(max(level−5,0)/3) produces the same final-expression truncation for integer base/bonuses. This placement matches the reported Rescue sequence at levels26..33: 33,32,32,32,32,31,31,30 without the ordinary-unpromoted bonus. A term-by-term floored subtraction would overstate some values. Sources label formula reconstruction empirical; multiplier rounding still remains separate uncertainty.

Staff base EXP is stored in the item record. Do not add difficulty bonuses twice. `ordinary_unpromoted` describes the current class, not whether an internal level happens to be below20. Starting at a high internal level does not mean a unit is unable to gain displayed levels.

Internal level and Second Seal accumulation remain in `average_stats.py`: displayed level + promoted20 + cumulative level; Second Seal adds floor((old displayed level+old promoted20−1)/2) subject to Normal20/Hard30/Lunatic(+)50 cumulative caps. Master Seal preserves cumulative level. The existing Donnel worked example is regression tested. Growth projections use actual level-up counts and class path; EXP scaling does not change per-level growth percentages. Unknown cumulative history stays unknown.

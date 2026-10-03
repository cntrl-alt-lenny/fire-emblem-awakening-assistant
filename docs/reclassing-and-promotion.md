# Seals, classes and experience

Sources: `class_details_2`, `class_sets`, `class_sets_1`, `calculations`, `nintendo_manual`.

Master Seals promote eligible base classes at level10+. Second Seals permit base-class changes at nonpromoted level10+ or any promoted level; advanced-class targets require promoted level10 or special-class level30. Special classes cap at30; ordinary base/promoted classes cap at20. Same-class reset eligibility and DLC item transitions must be checked individually. Class sets and gender restrictions determine available targets.

Class changes reset displayed level to1. Permanent stats change by new class bases minus old class bases; Luck class bases are zero. Caps can hide accumulated personal stats that reappear on changing class. Weapon experience is retained even when the current class cannot use its weapon type. Learned skills persist; equipped slots are limited to five. Promotion links are reciprocal in `classes.json`. Changing classes does not mean every temporarily active/equipped bonus is permanent.

Internal level = displayed level +20 if promoted + cumulative level. A Second Seal adds floor((displayed level + promoted20 −1)/2) to cumulative level, capped Normal20/Hard30/Lunatic50/Lunatic+50. Master Seals preserve cumulative level. This affects EXP scaling, not the growth rate per level-up. `average_stats.py` exposes both internal-level functions but does not claim a full EXP-to-future-level prediction.

Average projections require actual class path, number of level-ups, raw baseline, known caps, gender for Taguel and resolved Robin/child growths. They propagate cap-aware per-stat distributions and class-base changes. Empty-level rerolls/correlations and seal availability are not modeled. `starting_level` is required for actual-unit comparisons; the result must end at the same class and displayed level. Stat boosters must be included consistently in both comparison baselines.

Battle EXP source ambiguity remains unresolved: a published Lunatic repeated-combat term has a sign inconsistent with its explanatory note. `experience.py` now implements supported ordinary combat/staff/Dance cases; repeated Lunatic engagements refuse by default, with an explicit interpretation opt-in. See [experience.md](experience.md) for rounding, categories and tested examples. Weapon-rank tables may use zero-based versus initial-one experience conventions (31/71/121/181 versus30/70/120/180); do not increment actual ranks from unverified thresholds.

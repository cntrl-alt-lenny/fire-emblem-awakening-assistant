# Using the local assistant during play

Report difficulty/mode, current map and turn first, then the actual relevant units: class/level/current HP, all eight stats, whether raw or effective, weapon ranks, inventory durability/forges, equipped skills, supports and Pair Up/adjacent allies. Report terrain/rallies/tonics and enemy stats/skills from the screen. The assistant should record changes before advising.

A doubling question needs effective Speed for both sides (difference5). A combat question also needs weapon/range, Defense or Resistance, Skill/Luck, ranks, terrain and supported effects. Paired stat forecasts are available; full dual-combat survival distributions are not. For two enemy attacks, supply their actual order/ranges; `enemy_phase.py` propagates HP across supported duels without predicting enemy AI.

Use actual roster roles and stat thresholds for promotion, boosters and weapon choices. Average-stat deviation can inform discussion but does not measure a unit's usefulness or guarantee future gains. Promotion gains follow class-base differences; later growth depends on the new class and attainable EXP. Exact future EXP is not yet implemented.

Reference items contain seals, stat boosters, tonics, keys, special/DLC items and staves. Weapons contain ranks, stats, durability, Worth, effects and many obtainability entries. Worth is retained as the source's term; buy/sell price under discounts/durability is not guessed. Forge quotes use full-use Worth and verified player interval limits. Enemy forged values can exceed those limits.

Shop/merchant stock and renown rewards are normalized with source IDs. Birthdays/barracks, event boosts and world-map encounter tables retain partly unreviewed rows. Do not use their blank continuation cells as “nothing sold.” Complete movement-cost/terrain maps, enemy pathfinding, shops per difficulty, status effects, rescue/healing formulas and exhaustive legacy bonus teams are unfinished. Historical DLC/SpotPass descriptions do not establish present-day network service availability.

For reinforcements, inspect the matching mode's record and its verification flags. No record currently meets complete tactical-safety verification. A null schedule means unknown. During a real run, researching and confirming the current map takes priority over generic future content, with spoiler mode enforced.

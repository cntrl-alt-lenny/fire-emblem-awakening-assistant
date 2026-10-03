# Combat calculations

Primary numerical source: `calculations` (Serenes Forest). Probability cross-check: `true_hit` (Fire Emblem Wiki; table credits Serenes Forest). `data/mechanics/formulas.json` stores equations. Most formulas are reviewed single-source facts, not independently verified game code.

Use effective stats including active bonuses exactly once. Discard fractions at the stated floor operations. Clamp displayed hit/crit to 0–100.

| Quantity | Rule |
|---|---|
| Attack | Strength or Magic + weapon Might + rank attack bonus |
| Damage | max(0, Attack + triangle attack − appropriate Defense/Resistance − terrain defense bonus) |
| Hit | weapon Hit + floor((3×Skill+Luck)/2) + rank hit + triangle hit + hit bonuses − defender Avoid |
| Avoid | floor((3×Speed+Luck)/2) + avoid bonuses + terrain Avoid |
| Critical | weapon Crit + floor(Skill/2) + crit bonuses − defender Luck − crit-avoid bonuses |
| Critical damage | 3 × normal damage |
| Follow-up | effective Speed at least 5 greater than opponent |
| Effective weapon | triple weapon Might; rank/stat attack is not tripled |

No weapon-weight Speed penalty. Magical weapons target Resistance; ordinary weapons target Defense. Brave weapons strike twice per attack opportunity, potentially four strikes with a follow-up. Counters require matching range. Combat ends on death; planned strikes are not guaranteed to occur.

Weapon triangle: swords beat axes, axes beat lances, lances beat swords. The advantageous unit's rank governs both sides: E/D ±5 hit; C ±10 hit; B ±10 hit and ±1 attack; A ±15 hit and ±1 attack. The disadvantaged side loses its weapon-rank bonuses.

| Rank | Sword attack/hit | Lance, bow, tome attack/hit | Axe attack/hit | Staff recovery |
|---|---|---|---|---|
| C | 1/0 | 1/0 | 0/5 | 1 |
| B | 2/0 | 1/5 | 0/10 | 2 |
| A | 3/0 | 2/5 | 1/10 | 3 |

Hit uses 2RN: floor(mean of two uniform integers 0–99) below displayed hit. Critical activation uses a separate modeled probability. The tool enumerates HP outcomes across hit/crit branches; those are exact under the independent uniform model, not knowledge of the game's current RNG stream.

`combat_calculator.py` supports ordinary/magical/effective/Brave weapons, range, ranks, triangle, supplied terrain and combat bonuses, selected passives, Aggressor and weakness removal. Stat skills/faires/weapon bonuses must already be in effective input stats. Restricted weapon eligibility is separate; dark-tome restrictions are not resolved from plain text. Stones distinguish Beaststone/Pavise from Dragonstone/Aegis.

Supported isolated events: Luna (Skill%), Ignis (Skill%), Vengeance (2×Skill%), Sol (Skill%, overkill refused), Pavise/Aegis (Skill%), Miracle (Luck%, only above1HP and against a lethal hit), Vantage/Wrath (at most halfHP), Rightful King/God (add10/30percentage points), and enemy Hawkeye/Luna+/Vantage+/Pavise+/Aegis+. Rates cap at100%. Offensive effects precede criticals; defensive halving follows them. Fractions discard at implemented steps. Proc priority is sourced; multiple probabilistic offensive proc combinations are refused until shared/separate RNG checks are independently established. Multiple defensive procs, Luna with defense terrain, and Sol overkill are also refused.

Nominal `attacker`/`defender` forecasts exclude proc damage. Use `outcome` for HP states/probabilities, minimum/maximum possible HP, death probability and deterministic classification. Vantage changes initial attack order; Brave strikes stop on death. HP-dependent Wrath/Vengeance/Miracle are checked against the current branch state. Expected HP is not a guarantee. These are exact distributions within the supported independent uniform model and supplied inputs, not the actual RNG stream or unknown enemy skill rolls.

Aether/Astra/Lethality/Counter/Dragonskin/drain weapons, post-kill healing, breakage and full dual combat remain unsupported. Pair bonuses, Dual Support and rates remain in `pair_up.py`; `paired_forecast.py` applies bonuses once from explicitly unpaired leader stats and raw partner thresholds, but leaves outcome UNKNOWN. Never strip an unsupported skill/weapon effect to obtain a result. `enemy_phase.py` requires explicit attacker order and enough total player weapon durability; it does not predict AI/pathfinding or missing reinforcements.

`healing.py` uses independently sourced Mend15+floor(Magic/2), Physic8+floor(Magic/2), Recover to full HP, plus staff rank/Healtouch and target HP caps. Sources: `p2_mend`, `p2_physic`, `calculations`, `skills_extra`, `weapons_b_2`. Physic maximum range is floor(Magic/2); low-Magic edge cases beyond the table are not inferred. Other healing staff coefficients remain unsupported. No automatic terrain table is implemented. Pegasus Knight's explicitly uncorrected/copy-conflicted sections remain excluded.

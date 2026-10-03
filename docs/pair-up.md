# Pair Up and Dual Support

Sources: `pair_support`, `pair_support_1`, `calculations`, `fe_wiki_pair`; do not import Fates' shield mechanics.

Pair Up gives the lead unit class-based bonuses from the support unit's **current class** plus bonuses from the support unit's **raw** stats. Class tables are in `classes.json`. For each non-HP stat, raw 10–19 adds1, 20–29 adds2, ≥30 adds3. Equipped stat skills, tonics and equipment are excluded from these raw thresholds. C/B support adds1 and A/S adds2 to each nonzero class bonus; these support increments do not apply to Movement. Personal thresholds do not add Movement or HP. The support unit does not receive reciprocal lead bonuses.

Dual Support also works with adjacent allies and gives combat hit/avoid/crit/crit-avoid bonuses. Individual contribution none/C/B/A/S =1/2/3/4/5; contributions sum, maximum12. Dual Support+ adds4 once. `pair_up.py` contains the full level1–12 table. These combat bonuses are separate from stat changes.

Dual Strike = floor((lead effective Skill + chosen support effective Skill)/4) +20/30/40/50/60 for none/C/B/A/S. Dual Strike+ adds10 once if present on either participating unit. Dual Guard uses effective Defense for physical attacks or Resistance for magical attacks: floor(sum/4) +0/2/5/7/10; Dual Guard+ adds10 once. Clamp to100.

Which adjacent ally participates, their usable weapon/range, activation ordering, Brave interactions and skill restrictions matter. The rates tool does not simulate those interactions. A displayed high hit or Dual Guard rate never guarantees survival. Nintendo's manual (`nintendo_manual`) confirms only the lead is targeted in Pair Up and switching lead ends movement; tactical movement/pathfinding is not implemented.

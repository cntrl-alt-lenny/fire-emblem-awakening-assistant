# Discrepancies, limits and unresolved questions

Last audit: 2026-10-02. No disagreement was silently averaged or hidden.

| Issue | Investigation / decision | Gameplay consequence |
|---|---|---|
| Chapter7 Lunatic reinforcement levels | EmblemWiki numerical table lists level9, Fandom Hard/Lunatic combined excerpt level7. Mode aggregation likely matters, but not resolved. Timing turn5 west is cross-referenced; exact squares/conditions unknown. | Partial record is not tactically certified; inspect spawned stats, never use Hard values for Lunatic. |
| Map search pollution | Search for one chapter returned a different chapter's schedule. Unreviewed excerpts retained as candidates with no safe flag. Irrelevant numerical search results were removed. | Do not use candidate lines as facts for the queried chapter. |
| Lunatic repeated-battle EXP | Serenes formula uses a minimum/sign that contradicts its note about reducing later EXP. No reliable independent resolution yet. | Supported battle/staff/Dance EXP now available; repeated Lunatic T>=4 refuses by default. Multiplier/fractional support rounding also remains opt-in interpretation. |
| Japanese triangle/rank/terrain conflicts | Pegasus Knight page labels early sections uncorrected and includes older-game copied values. | Excluded from implemented triangle/rank and no automatic terrain table. |
| WEXP thresholds | Serenes31/71/121/181 includes initial1; another table30/70/120/180 appears zero-based. Convention needs game check. | Store observed ranks/extra WEXP; no automatic rank advancement. |
| Yarne/Nah source ranks | Main-story bases page shows bow icon in stone-wielding rows; class weapon access contradicts it. Corrected to unranked stone. | Never infer bow access from erroneous icon. |
| Chrom movement | Recruitment source lists movement6; Lord class table movement5. Class table preferred. Movement is stored on classes. | Use effective observed movement plus current class/bonuses. |
| Morgan support table | Male/female Morgan edge contradicts explicit support restriction. Removed and logged in support_conflicts.json. | No impossible Morgan marriage suggestion. |
| Renown Tiki's Tears naming | Renown table plural versus item table singular Tiki's Tear. Canonical reward ID maps to singular; source display text preserved. | One item identity, no duplicate reward inventory. |
| Robin / child recruitment values | Robin requires asset/flaw. Child absolute bases are formula inputs; parents and autolevel treatment matter. | Baselines/growths/caps are not universal recruited stats. |
| Lunatic+ player recruitment templates | No independently established equivalence for every character. | Raw recruitment template is null; actual reported stats required. |
| Caps and level-up distributions | Ordinary capped marginal growth model implemented; empty-level rerolls/correlations not researched enough. | Means/standard deviations are model estimates; not exact joint game distributions. |
| Services/availability | Sources describe historical DLC/SpotPass, not current service availability. | Do not promise online acquisition today. |
| Full skill/weapon simulation | An isolated proc subset is supported. Full duals, Aether/Astra/Lethality/Counter/Dragonskin/drain weapons, combined procs/RNG dependence, terrain-Luna, Sol-overkill and breakage remain unsupported. | Refuse exact forecast or clearly mark partial, never strip effects. |

The machine source registry lists extract IDs, not independent publishers; see SOURCES.md for the current count. Serenes Forest supplies most numerical tables, and some fan tables credit it. Cross-check depth is incomplete. Source accessibility failures were respected rather than circumvented.

## Tactical correctness phase findings

- Chapter5: grouped Hard/Lunatic source turns3/4/5 versus separate Lunatic numerical turns3/5/6. Mode conflation remains possible; no certified schedule.
- Chapter22: grave/road wave text was repeated under another map. Quarantined rather than copied into either schedule. Gamer Guides reports no reinforcements on Hard, still single-source and uncertified.
- All starting coordinates, activation geometry and exact wave tile coordinates remain UNKNOWN. Source surveys cover51 maps; complete tactical audits do not.
- Enemy `+`/`++` forges and random skills remain unresolved; do not use ordinary weapon values after stripping suffixes. Missing starting/reinforcement headings remain an explicit unknown phase.
- Celica's Gale/Waste Brave flags, Mjölnir Skill bonus, Luck aliases and combined Defense/Resistance bonuses were parsing mistakes corrected in the offline build.
- Vantage/Wrath inclusive halfHP boundaries were checked against game-localization descriptions. Pavise includes blighted claws/talons and excludes Dual Strikes; General learning level15 independently checked.
- Staff EXP final-expression truncation matches reported Rescue examples; term-wise truncation overstated several values. Empirical reconstruction is not game-code verification.
- Plain-text tome extraction loses the red color used for dark-only eligibility. Dark Mage/Sorcerer/Shadowgift rule is known; exhaustive individual tome classification is not yet recovered. Do not certify other-class eligibility from a generic tome label.
- Independent numerical field audit checked15 fields in Iron Sword/Mend/Physic. Full character/class/gender/Robin/child/DLC/SpotPass audits remain partial. Existing availability tags are maintained, not exhaustively recertified.

`research/phase2/reviewed_additions.json`, `normalization_audit.json`, `access_inventory.json`, `final_audit.json` and `docs/map-coverage.md` retain specific evidence, attempts, conflicts and coverage. Zero fully verified map reinforcement schedules remain.

## Chapter 17 inventory provenance — 2026-10-03

The first and second Hard inventories retain four units as single-source Fandom reports; their class/count/equipment claims no longer credit Gamer Guides or Pegasus Knight. The central inherited six-unit literal has no recoverable external origin, while the accessible indexed Hard row reports two units. Neither is selected as actual gameplay: the central inventory is CONFLICTED with a null value and both alternatives in notes. Null is unknown, not zero. Staircase/timing conflict, unknown phase and incomplete schedule remain unchanged. See the [field-level audit](../docs/rounds/005-chapter17-provenance/attachments/inventory-audit.md).

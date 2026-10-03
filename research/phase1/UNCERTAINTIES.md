# Discrepancies, limits and unresolved questions

Last audit: 2026-10-02. No disagreement was silently averaged or hidden.

| Issue | Investigation / decision | Gameplay consequence |
|---|---|---|
| Chapter7 Lunatic reinforcement levels | EmblemWiki numerical table lists level9, Fandom Hard/Lunatic combined excerpt level7. Mode aggregation likely matters, but not resolved. Timing turn5 west is cross-referenced; exact squares/conditions unknown. | Partial record is not tactically certified; inspect spawned stats, never use Hard values for Lunatic. |
| Map search pollution | Search for one chapter returned a different chapter's schedule. Unreviewed excerpts retained as candidates with no safe flag. Irrelevant numerical search results were removed. | Do not use candidate lines as facts for the queried chapter. |
| Lunatic repeated-battle EXP | Serenes formula uses a minimum/sign that contradicts its note about reducing later EXP. No reliable independent resolution yet. | Full battle EXP calculator omitted. |
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
| Full skill/weapon simulation | Proc damage/healing, priorities, dual interactions and breakage unsupported. | Refuse exact forecast or clearly mark partial, never strip effects. |

The source registry has 66 source/extract IDs, not 66 independent publishers. Serenes Forest supplies most numerical tables, and some fan tables credit it. Cross-check depth is incomplete. Source accessibility failures were respected rather than circumvented.

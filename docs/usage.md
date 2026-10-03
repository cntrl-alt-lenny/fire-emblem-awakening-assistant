# Usage and tools

Local factual reference and playthrough tools, built on 2026-10-02. Python 3.9+; standard library only. No account, service, installation or API key required. All files live here. Start with [STATUS.md](../STATUS.md) for coverage and limitations and [AGENTS.md](../AGENTS.md) for tactical/spoiler policy.

The catalog contains 49 story/child/SpotPass story characters, 55 class variants including enemy/NPC entries, 138 damaging weapons, 59 staves/items, 103 skills, 76 map catalog entries and 316 support-threshold edges. Most numerical facts are single-source transcriptions. Detailed maps are a major unfinished area: 1,104 representative Lunatic enemy rows across36 maps, partial Hard metadata across45 maps and74 partial wave records, with no fully verified safe reinforcement schedules. Tracking and supported observed-input calculations are available. The current Hard forensic layer supports uncertainty-aware assisted play; it cannot provide complete map safety guarantees. See [current coverage](../STATUS.md). No run was started.

## Start a run

From the repository root:

```sh
python3 tools/roster_tracker.py init --difficulty Hard --mode Classic
python3 tools/roster_tracker.py upsert examples/chrom.json
python3 tools/roster_tracker.py set chapter chapter_7
python3 tools/roster_tracker.py set turn 1
python3 tools/roster_tracker.py show
```

The example is Chrom's **recruitment** state; replace it with your actual stats before importing. No run is initialized automatically. Run JSON is authoritative; [CURRENT_RUN.md](../CURRENT_RUN.md) explains the pointer. Use `--state state/another_run.json` before the subcommand to maintain a separate run. Atomic writes, process locking and an embedded before/after event ledger preserve updates. Do not manually erase history.

```sh
python3 tools/level_tracker.py Chrom hp=1 str=1 skl=1 spd=1
python3 tools/roster_tracker.py death Stahl
python3 tools/roster_tracker.py consume Chrom vulnerary_1 --uses 1
python3 tools/roster_tracker.py support Chrom Sumia C
python3 tools/roster_tracker.py class-change Chrom great_lord_m examples/promotion_stats.json --kind promotion
python3 tools/roster_tracker.py complete-map
```

Commands require the relevant actual unit(s) to exist. Promotion example stats are illustrative, not predicted for your run; promotion requires displayed level 10+. `class-change` records actual stats and history; record the consumed seal separately. `complete-map` explicitly restores Casual availability. Read each tool's `--help`.

## Reference and calculations

```sh
python3 tools/knowledge.py weapons "Iron Sword"
python3 tools/knowledge.py classes knight --search
python3 tools/combat_calculator.py examples/battle.json
python3 tools/pair_up.py examples/pair_up.json
python3 tools/enemy_phase.py examples/enemy_phase.json
python3 tools/average_stats.py examples/average_chrom.json
python3 tools/unit_compare.py Chrom examples/average_chrom.json
python3 tools/inheritance.py avatar spd lck
python3 tools/inheritance.py child examples/child_growths.json
python3 tools/forge.py "Steel Sword" 2 3 1
python3 tools/tactical_query.py chapter_7 --difficulty Hard --turn 4
python3 tools/experience.py examples/experience.json
python3 tools/healing.py examples/healing.json
python3 tools/paired_forecast.py examples/paired_forecast.json
```

Combat inputs contain effective stats, current HP, equipped skills, rank, exact weapon, range and active combat bonuses. Raw stats belong in growth and Pair Up threshold tools. Full paired battle outcome, many proc interactions and weapon breakage remain unsupported. A verified isolated-proc subset now reports HP distributions and worst possible HP; refused effects must never be silently ignored. See [combat-formulas.md](combat-formulas.md). Enemy-phase analysis requires a supplied sequence and does not predict AI behavior. CLI reference output can contain spoilers.

## Layout and reproducibility

- `data/`: canonical JSON facts, formulas, separate difficulty records and source registry.
- `research/`: factual-table staging extracts, schemas, inventory, discrepancies and generated audit; unreviewed facts remain visibly labeled.
- `docs/`: mechanics explanations and coverage boundaries.
- `tools/`: offline normalization, lookup, calculation and tracking programs.
- `state/`: player runs; initially empty.
- `tests/`, `examples/`: independent regression fixtures and input examples.

`make audit` validates references/values/difficulty separation and runs the regression suite. `make rebuild` deterministically regenerates core entities from retained factual tables and reviewed enrichment, then audits. It never fetches websites or modifies run state. Formula/system JSON and docs are maintained separately. [SOURCES.md](../SOURCES.md) lists sources, dates, scope and limitations; [research/UNCERTAINTIES.md](../research/UNCERTAINTIES.md) records unresolved issues. No whole webpages were archived.

## Hard / Classic forensic reference

No run has been initialized. The current evidence-aware Hard layer is described in [STATUS.md](../STATUS.md) and [map coverage](map-coverage.md). It has 44 ordinary campaign reviews, useful supported tactical claims and explicit gaps; it is not a fully certified route guide.

```sh
python3 tools/map_info.py --chapter 7 --difficulty hard --turn 5 --phase player
python3 tools/tactical_combat.py observed_battle.json
make audit
make rebuild
```

The map command targets enemy phase5 from player phase5; phase is required with a turn. It separates known from uncertain events and retains unknown timing. The strict combat gate requires confirmed observed inputs and explicit support state; unsupported interactions return UNKNOWN. Read `docs/hard-reinforcements.md` before interpreting arrival claims. Other modes, procedural skirmishes and bonus content remain separate.

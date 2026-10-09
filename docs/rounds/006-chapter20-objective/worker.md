<!-- fw-report
round: 006-chapter20-objective
role: worker
branch: worker/006-chapter20-objective
head: 16ab2465f402cee0b93be4772bd5f5ff5525235c
os: macOS 27.0.1
python: 3.9.6
written: 2026-10-05T08:05:45Z
-->
## Verified
- Startup and branch — `python3 tools/fw.py start --role worker --round 006-chapter20-objective` → exit 0
  Output: `seat ok: worker, round 006-chapter20-objective, branch worker/006-chapter20-objective at 6ab0e7786c74`; brief resolved to `docs/rounds/006-chapter20-objective/brief.md`.
- Environment at evidence commit `16ab246` — `platform.platform()` / `sys.version` → exit 0
  Output: `macOS-27.0.1-arm64-arm-64bit`; `3.9.6 (default, Aug 25 2026, 21:26:21) [Clang 21.0.0 (clang-2100.3.34.2)]`.
- Required audits at `16ab246` — `make audit` → exit 0
  Output: data validation passed; phase-two audit passed; Hard audit passed with `campaign_maps: 44`, `reinforcement_records: 29`, `registered_sources: 217`, `source_refs_resolve: true`; unittest summary: `Ran 118 tests ... OK`. Audit warnings retain incomplete schedules and source-truth limits.
- Framework hygiene at `16ab246` — `python3 tools/fw.py check` → exit 0
  Output: `0 error(s), 0 warning(s)`.
- Chapter 20 map query at `16ab246` — `python3 tools/map_info.py --chapter 20 --difficulty hard` → exit 0
  Output: `chapter_id=chapter_20 difficulty=Hard mode=Classic map_confidence=CONFLICTED`; objective is `Defeat Walhart`, `objective_confidence=CONFLICTED`, `schedule_complete=False`.
- Player-phase query at `16ab246` — `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase player` → exit 0
  Output: `target_enemy_phase_turn=6`; map remains `CONFLICTED`, objective confidence remains `CONFLICTED`, schedule remains incomplete.
- Enemy-phase query at `16ab246` — `python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase enemy` → exit 0
  Output: `target_enemy_phase_turn=7`; map remains `CONFLICTED`, objective confidence remains `CONFLICTED`, schedule remains incomplete.
- Whitespace check at `16ab246` — `git diff --check` → exit 0
  Output: no whitespace errors.
- Preservation at baseline commit before research through `16ab246` — Python SHA-256 snapshot of sorted `data/**/*.json` and `state/**/*` file sets/content → exit 0
  Output: canonical data JSON count `28` before and after; file set equal and SHA-256 equal; state file count `1` before and after; file set equal and SHA-256 equal; `state/current_run.json` present: `false`. Other-mode canonical data was preserved. Private state digests remain outside this public report.
- Source trace and comparison — direct page contexts checked 2026-10-05 against registry extracts accessed 2026-10-02; details, exact URLs and claim matrix are in `attachments/objective-evidence.md`.
  Output: `p2_guide_20_1` contains `Condition: Defeat every Boss` in the actual Chapter 20 note field; the three-boss roster is a separate table. A separate GameFAQs guide scopes Chapter 20 to Normal/Hard/Lunatic, identifies Walhart as commander, and says defeating him ends the level. A player post reports the chapter completed with Cervantes and Excellus alive, but states no difficulty and supplies no visible capture. This source evidence favors Walhart alone, while direct Hard/Classic display and transition remain unobserved.

## Not verified
No in-game objective screen or continuous Hard/Classic gameplay sequence was available. The player report does not establish difficulty, region/version, hidden boss status or an uninterrupted completion transition. No canonical source/data assertion was amended. Model, reasoning-effort and speed settings are not exposed to this Worker.

## Changed
- `docs/rounds/006-chapter20-objective/attachments/objective-evidence.md` — source trace, claim matrix, assessment, and the discriminating Hard/Classic observation plan. No canonical data, source registry, tools, tests, coverage counters, standing decisions or run state changed.

## Open questions
Whether the game's displayed Hard/Classic objective says to defeat Walhart and whether defeating Walhart immediately ends the map while Cervantes and Excellus remain alive still need visible game evidence. Recommended next task: obtain one continuous owner-supplied Chapter 20 capture showing Hard/Classic setup, both other bosses alive, Walhart's defeat and the immediate completion transition; record region/version if available. A sequence with a cut, reset, hidden/dead other boss, or either other boss defeated first is not discriminating.

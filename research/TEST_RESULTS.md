# Validation record — 2026-10-02, tactical correctness phase

- `make audit`: structural/reference/value/difficulty checks and semantic audit passed, zero errors; **60 regression tests passed**.
- The EXP test includes35 observed Champions of Yore values and eight Rescue examples as subcases; they are not counted as separate test methods.
- `python3 -m py_compile tools/*.py`: passed.
- Two successive offline rebuilds: all25 canonical JSON files identical by SHA-256. No network used by rebuilds.
- Combat, enemy-phase, paired-preview, current-map query, EXP and healing CLI smoke checks passed. Paired outcome remains explicitly UNKNOWN; query cannot certify no reinforcements.
- Canonical nested source references and static calculator source IDs resolve in the registry.
- `state/` remains empty; no playthrough initialized. Existing CURRENT_RUN.md remains unchanged.

See `audit.json`, `phase2/final_audit.json`, `phase2/rebuild_determinism.json`, `phase2/offline_rebuild.log` and `phase2/validation_and_tests.log`. Tests verify supported calculations and guardrails, not missing map evidence. No schedule is certified; the Hard/Classic readiness judgment is false.

# Owner-requested bootstrap evidence — 2026-10-03

Setup was completed before this first product audit was briefed. The owner
explicitly requested moving and publishing the project and applying the
framework. This record is setup evidence, not a Worker or Verifier report.

Reviewed setup commit: `69a73ac6bee68e15f86a70cc6f9f13b7645a97ba`.

## Verified

- `make audit` at the setup commit: exit 0.

  ```text
  Ran 102 tests in 0.310s
  OK
  ```

- `python3 tools/fw.py check`: exit 0.

  ```text
  0 error(s), 0 warning(s)
  ```

- Python SHA-256 comparison: all 198 original data, tool, test, research,
  example and current-run-pointer files were byte-identical to the pre-move
  snapshot. The original `AGENTS.md` is preserved byte-identically in
  `docs/agents/local/tactical-policy.md`.
- Python SHA-256 comparison against `docs/agents/framework.json`: every
  framework-owned copy matches the exact upstream `v3.1.0` release.
- `gh pr checks 1`: exit 0 once all six push/PR jobs passed (Linux Python
  3.9/3.13 and macOS Python 3.13 for each event). Setup pull request merged.
- Published README rendered in GitHub: banner/layout inspected; local links
  in the landing page and usage guide resolved. Visible word estimate: 372.

## Not verified

No independent game-source certification or live playtest was performed by
this setup. No full reinforcement schedule was newly certified. A project-wide
license and branch-protection policy were not selected. Native Windows CI
failed before tests on default text encoding; run tracking additionally uses
`fcntl`. The full toolkit is documented for Linux/macOS, with WSL suggested
for Windows. No production portability fix was made.

## Preserved scope

The original gameplay data, calculators, trackers, tests and research were
preserved. Player runs stay local/ignored, no run was initialized, and the
upstream framework MIT notice is retained separately. No separate agent was
started or messaged as part of this bootstrap.

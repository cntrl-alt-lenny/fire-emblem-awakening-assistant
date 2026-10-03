# Contributing

Read [AGENTS.md](AGENTS.md) before changing anything. Preserve source provenance,
difficulty separation, explicit uncertainty and the live-run event history.
Never initialize or edit a player run while testing.

## Checks

From the repository root, run `make audit`. Without make:

```sh
python3 tools/validate_data.py
python3 tools/audit_phase2.py
python3 tools/audit_hard.py
python3 -m unittest discover -s tests -v
```

Python 3.9+ and its standard library are sufficient. On Windows, replace
`python3` with `py -3`. Audit warnings describe real coverage gaps; green
checks do not certify all mechanics or a complete tactical route.

`make rebuild` regenerates canonical records from retained factual extracts
and reviewed enrichment. Review the diff and rerun `make audit` afterwards.
Never fetch sources as part of a build. Do not store whole guide prose, game
assets, credentials or personal playthrough files in this public repository.

## Changes and evidence

Use focused branches and pull requests. Explain the problem, the resulting
behavior, the exact checks and their output, and what remains unverified.
Canonical data and external factual claims require independent source review.
The owner chooses licensing and repository access policy.

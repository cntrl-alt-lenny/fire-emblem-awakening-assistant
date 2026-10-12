# Earlier attempts

All work used the isolated Worker checkout. No private run was used as a test.

| Command / attempt | Relevant actual result | Exit |
|---|---|---:|
| Read `tests/test_hard_tactics.py` after inspecting Makefile | `sed: tests/test_hard_tactics.py: No such file or directory`; inventory located actual `tests/test_hard.py` and subsequent read succeeded | 1 |
| First `python3 -m unittest discover -s tests -p test_play_briefing.py -v` | `Ran 15 tests in 2.310s`, `OK` before standard-note shortening | 0 |
| Focused tests after shortening repeated notes | `Ran 15 tests in 2.202s`, `FAILED (failures=1)`; conflict test expected the exact objective note for Chapter20; default renderer had abbreviated that generic note | 1 |
| Focused tests after preserving every conflicted note verbatim | `Ran 15 tests in 2.192s`, `OK` | 0 |
| Pre-commit CLI acceptance | 108 raw-query CLI comparisons passed; 333/27 before/after lines; canonical/research/local/private preservation passed | 0 |

The failed conflict assertion produced:

```text
FAIL: test_conflicts_and_terrain_dangers_not_truncated
AssertionError: 'Campaign objective catalog compared against Hard-default guide; verify displayed objective before declaring completion.' not found
Ran 15 tests in 2.202s
FAILED (failures=1)
```

The renderer now leaves all conflicted notes unabridged. No test was weakened
to resolve that failure. No blocker remains from these attempts.

# 09-combat-context — independent Verifier review

Reviewed delivery: `51d99b75d829ef3fa82c7785552352887016181f`.
Starting main: `d3b646975a5f0686a798aaf12c0e541ed396da08`.
Plan: `4c18202f428c736a10643865e7ba2ef7c9244515`.

## Blind ordering and judgment

Started with framework status and project/verifier/tactical rules, fetched origin,
resolved `51d99b7` and asserted the remote Worker tip equalled that literal commit.
Used an independent detached linked checkout. Before reading changed gate,
new tests/reference or Worker conclusions, exported starting main and privately
probed the existing `test_hard.battle()` fixture on both sides. Then read the real
diff before the summary. Baseline observations were retained privately.

All criteria **met**. Both fighter skills require exact booleans; all three turn
skills require exact positive integers on either side. Missing/null, numbers,
booleans, strings and containers produce UNKNOWN/null with useful side/field
messages when invalid for that field. No coercion or skill removal occurs.
Optional omissions still work. Both sides, indoor/outdoor conditions, turns
1/2/7/8/9 and active/inactive parity preserve complete assessment objects exactly;
I separately rederived displayed-hit arithmetic. Inputs remain unchanged.
Unequipped-defender context and paired/adjacent/Counter/Dragonskin/Astra/drain
refusals remain enforced. All 16 changed files are within ownership; canonical,
rebuild, general calculator, proc engine and shared tests are unchanged.

## Independent evidence

All delivery checks below ran at the reviewed literal commit. `$P` denotes the
private temporary probe directory; `$BASE` its exported starting-main tree.
Private scripts/logs were kept outside the public repository and use synthetic
fixtures only. The regression harness independently challenges malformed context
with subtests; the broader probe includes missing fields and supported controls.

| Actual command/check | Relevant real output | Exit |
|---|---|---|
| `python3 "$P/probe.py" "$BASE" "$P/baseline-probe.json"` | `malformed cases 116 numerical 70 UNKNOWN 46 valid cases 39 input unchanged` | 0 |
| `python3 "$P/independent_regression.py" "$BASE"` | `Ran 1 test`; `FAILED (failures=62)` | 1 expected |
| `python3 "$P/independent_regression.py" .` | `Ran 1 test`; `OK` | 0 |
| `python3 "$P/probe.py" . "$P/review-probe.json"`; independent JSON comparison/assertions | `All 39 supported full-result outputs equal baseline`; all 116 UNKNOWN/null/diagnostic; inputs unchanged | 0 |
| Independent `python3` public-CLI harness invoking `python3 tools/tactical_combat.py` with temporary synthetic JSON | `Independent public CLI: 20 cases: exit 0; valid hits rederived; JSON/refusals/files unchanged` | 0 |
| `make audit` | Three audits `"passed": true`, `"errors": []`; `Ran 127 tests in 2.417s`; `OK` | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `git diff --check d3b646975a5f0686a798aaf12c0e541ed396da08...HEAD` | No output | 0 |
| `python3 -m unittest discover -s tests -p test_combat_context.py -v` | `Ran 9 tests in 0.916s`; `OK` | 0 |
| Private SHA256 file-set/content comparison: canonical JSON, CURRENT_RUN.md, every regular state file | `primary 30/30, review 30/30` preserved | 0 |
| Python Markdown tables/fenced-code + headless Chrome, 1440×3000; local-link assertions | Reference 3 links, summary 1 link resolve; both screenshots visually inspected, readable and unclipped | 0 |

## Findings and verdict

No BLOCKER, SHOULD FIX, NOTE or UNPROVEN CLAIM finding. **PASS for Brain review**;
this is not merge approval. Expected baseline failures are preserved evidence.
Existing framework patch/EADME housekeeping is outside this batch.

No rebuild was required by scope. No run was initialized, used as test input or
modified. Checks establish this input contract and numerical preservation;
source truth, exhaustive mechanics, real gameplay and whole-map safety remain
unverified. No gameplay coverage increase is claimed.

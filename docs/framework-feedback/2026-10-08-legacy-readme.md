# Framework feedback: legacy README misclassified as a batch

Project: Fire Emblem Awakening Assistant.
Observed at integration commit `8bf3a05`, framework 4.0.1 installed (only the
release-record patch was uncommitted). Framework source tag: `v4.0.1`.

## What happened

`python3 tools/fw.py status` labels legacy Worker/Verifier branches as
`batch EADME: Worker summary in`, though these branches contain 3.x reports,
not a batch summary. This can suggest the wrong next seat.

## Reproduction

```sh
python3 tools/fw.py status
python3 - <<'PY'
import importlib.util
s = importlib.util.spec_from_file_location('fw', 'tools/fw.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
print(m.batch_papers({'docs/rounds/README.md'}))
PY
```

Both exit 0. The isolated call prints `(['EADME'], [])`. `batches_lines`
combines changed batch and legacy-round paths; `batch_papers` slices every
path using the batch-directory length without first checking that prefix.

Expected: legacy README never becomes a Worker summary; legacy report branches
receive the existing legacy-round description. Actual: an invented batch EADME.

No installed framework code was edited. Brain inspects literal branch ancestry,
diffs and reports to reconcile this delivery; misleading status remains explicit.

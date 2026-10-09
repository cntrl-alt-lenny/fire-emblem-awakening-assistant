"""Reproduce numerical preservation against a pinned baseline gate; synthetic data."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import types

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
from test_hard import battle
from tactical_combat import assess

baseline_commit = sys.argv[1]
source = subprocess.check_output(
    ['git', 'show', baseline_commit + ':tools/tactical_combat.py'], cwd=ROOT, text=True)
baseline = types.ModuleType('baseline_tactical_combat')
exec(compile(source, 'baseline_tactical_combat.py', 'exec'), baseline.__dict__)
controls = []
for side in ('attacker', 'defender'):
    for skill, field, values in (
        ('outdoor_fighter', 'outdoors', (True, False)),
        ('indoor_fighter', 'outdoors', (True, False)),
        ('lucky_seven', 'turn', (1, 2, 7, 8)),
        ('even_rhythm', 'turn', (1, 2, 7, 8)),
        ('odd_rhythm', 'turn', (1, 2, 7, 8)),
    ):
        for value in values:
            payload = battle()
            payload[side]['skills'] = [skill]
            payload['context'][field] = value
            controls.append(payload)
controls.append(battle())
both = battle()
both['attacker']['skills'] = ['indoor_fighter', 'lucky_seven']
both['defender']['skills'] = ['outdoor_fighter', 'even_rhythm']
both['context'].update(outdoors=False, turn=8)
controls.append(both)
results = []
for index, payload in enumerate(controls):
    before = copy.deepcopy(payload)
    expected = baseline.assess(payload)
    actual = assess(payload)
    assert actual == expected, index
    assert payload == before, index
    results.append(actual)
print('Baseline gate:', baseline_commit)
print('All', len(controls), 'complete supported assessment objects match baseline exactly; inputs unchanged.')
print('SHA256 of ordered results:', hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest())
print('General calculator and proc engine must remain unchanged; verify with git diff before using this check.')

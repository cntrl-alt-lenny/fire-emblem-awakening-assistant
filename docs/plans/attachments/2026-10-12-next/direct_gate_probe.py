"""Brain's read-only synthetic direct-gate probe; no actual run inputs."""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
from tactical_combat import assess

payload = json.loads((ROOT / 'examples/battle.json').read_text())
before = copy.deepcopy(payload)
for field, value in (('alive', '?'), ('alive', 'false'), ('forge', {}),
                     ('status_effects', ['unknown'])):
    modified = copy.deepcopy(payload)
    modified['attacker'][field] = value
    unchanged = copy.deepcopy(modified)
    result = assess(modified)
    assert modified == unchanged
    print(json.dumps({'field': field, 'observation': value,
                      'status': result['status'], 'numeric_outcome': result['outcome'] is not None}))
assert payload == before
print('Synthetic checked-in fixture unchanged; no run read or initialized. Exit0')

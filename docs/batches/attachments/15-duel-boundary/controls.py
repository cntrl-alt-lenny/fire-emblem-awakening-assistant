"""Replay compatibility without production mutations or live run access."""
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'tests')]
import tactical_combat as gate
import tactical_enemy_phase as sequence
from test_observed_input import transcript
from test_tactical_enemy_phase import sequence as sequence_input
from test_duel_boundary import controls
BASE = 'ec3bceca1d70a4da240a490601602e97c2466de2'
source = subprocess.check_output(['git', 'show', BASE+':tools/tactical_combat.py'], cwd=ROOT, text=True)
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp)/'baseline.py'; path.write_text(source)
    spec = importlib.util.spec_from_file_location('baseline_duel', path)
    baseline = importlib.util.module_from_spec(spec); spec.loader.exec_module(baseline)
    for name, payload in controls():
        before = copy.deepcopy(payload)
        assert gate.assess(payload) == baseline.assess(payload)
        assert payload == before
        print('Full output equals baseline:', name)
    payload = sequence_input(); before = copy.deepcopy(payload)
    actual = sequence.evaluate(payload)
    with patch.object(sequence, 'assess', baseline.assess), patch.object(sequence, 'known_weapon', baseline.known_weapon):
        expected = sequence.evaluate(payload)
    assert actual == expected and actual['outcome'] is not None and payload == before
    print('Full sequence output equals baseline; input unchanged')
    for weapon in ('custom', 'catalog iron_sword'):
        # Existing synthetic collector helper exercises exactly its public API.
        from test_observed_input import collect as collector_fixture
        payload, _ = collector_fixture(transcript(weapon=weapon))
        assert gate.assess(payload) == baseline.assess(payload)
        assert gate.assess(payload)['outcome'] is not None
        print('Collector supported output equals baseline:', weapon)
print('Compatibility and immutable inputs; exit 0')

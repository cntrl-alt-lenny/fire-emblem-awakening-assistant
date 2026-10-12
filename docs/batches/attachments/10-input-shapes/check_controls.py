"""Reproduce baseline leaks and compare full supported results; synthetic only."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
from tactical_combat import assess
from test_hard import battle

BASELINE = 'e78fa7bcc245071556a408f725105ac63ce7a8e9'
source = subprocess.check_output(['git', 'show', BASELINE + ':tools/tactical_combat.py'], cwd=ROOT, text=True)
baseline = types.ModuleType('baseline_gate')
exec(compile(source, 'baseline_gate.py', 'exec'), baseline.__dict__)
print('Baseline:', BASELINE)
print('Current commit:', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())
print('Baseline direct/CLI numeric leaks -> hardened UNKNOWN/null; original inputs unchanged:')
with tempfile.TemporaryDirectory(prefix='input-shape-controls-') as temp:
    path = Path(temp) / 'synthetic.json'
    script = Path(temp) / 'baseline_gate.py'
    # Public baseline CLI with the unchanged calculator and canonical data.
    script.write_text('import sys\nsys.path.insert(0, ' + repr(str(ROOT / 'tools')) + ')\n' + source, encoding='utf-8')
    for side in ('attacker', 'defender'):
        for field, values in (('skills', ('', {})), ('weaknesses', ('', {})), ('current_hp', (True, 1.0, 1.5))):
            for value in values:
                payload = battle()
                payload[side][field] = value
                before = copy.deepcopy(payload)
                old = baseline.assess(payload)
                assert old['outcome'] is not None
                actual = assess(payload)
                assert actual['status'] == 'UNKNOWN' and actual['outcome'] is None
                assert side + ':' + field in actual['reason']
                encoded = json.dumps(payload)
                path.write_text(encoded, encoding='utf-8')
                results = []
                for command in (script, ROOT / 'tools/tactical_combat.py'):
                    process = subprocess.run([sys.executable, str(command), str(path)], cwd=ROOT, capture_output=True, text=True)
                    assert process.returncode == 0, process.stderr
                    results.append(json.loads(process.stdout))
                assert results == [old, actual]
                assert payload == before and path.read_text(encoding='utf-8') == encoded
                print(side + ':' + field, repr(value), 'direct=' + old['status'], 'CLI=' + old['status'], '-> UNKNOWN/null; CLI exit 0')

    controls = [battle()]
    for side in ('attacker', 'defender'):
        for hp in (1, 20, 40):
            for skills in ([], ['veteran'], ['hit_rate_plus_10'], ['hawkeye'], ['luna'], ['vantage'], ['miracle']):
                for weaknesses in ([], ['beast'], ['dragon'], ['armour'], ['flying'], ['beast', 'dragon', 'armour', 'flying']):
                    payload = battle()
                    payload[side].update(current_hp=hp, skills=skills, weaknesses=weaknesses)
                    payload[side]['stats']['skl'] = 10
                    payload[side]['stats']['lck'] = 10
                    controls.append(payload)
        for skill, field, values in (('indoor_fighter', 'outdoors', (True, False)), ('outdoor_fighter', 'outdoors', (True, False)),
                                    ('lucky_seven', 'turn', (1, 7, 8)), ('even_rhythm', 'turn', (1, 2)), ('odd_rhythm', 'turn', (1, 2))):
            for value in values:
                payload = battle()
                payload[side]['skills'] = [skill]
                payload['context'][field] = value
                controls.append(payload)
        for crit, speed in ((0, 14), (1, 15), (10, 20)):
            payload = battle()
            payload[side]['weapon']['crit'] = crit
            payload[side]['stats']['spd'] = speed
            controls.append(payload)
        payload = battle()
        payload[side]['weapon'] = 'iron_sword'
        payload[side]['weapon_rank'] = 'D'
        controls.append(payload)
        payload = battle()
        payload[side]['weapon'].update(brave=True, effect='2 consecutive attacks')
        controls.append(payload)
        payload = battle()
        other = 'defender' if side == 'attacker' else 'attacker'
        payload[side]['weapon']['effectiveness'] = ['flying']
        payload[other]['weaknesses'] = ['flying']
        controls.append(payload)
    payload = battle()
    payload['defender'].update(weapon=None, weapon_state='unequipped', remaining_uses=0)
    controls.append(payload)
    for index, payload in enumerate(controls):
        before = copy.deepcopy(payload)
        expected = baseline.assess(payload)
        actual = assess(payload)
        assert expected['outcome'] is not None, index
        assert actual == expected, index
        assert payload == before, index
    # Compare the full public CLI JSON too, selecting distinct supported outcomes.
    for payload in controls[::30] + controls[-7:]:
        encoded = json.dumps(payload)
        path.write_text(encoded, encoding='utf-8')
        process = subprocess.run([sys.executable, str(ROOT / 'tools/tactical_combat.py'), str(path)], cwd=ROOT, capture_output=True, text=True)
        assert process.returncode == 0, process.stderr
        assert json.loads(process.stdout) == baseline.assess(payload)
        assert path.read_text(encoding='utf-8') == encoded
    print(len(controls), 'complete supported assessment objects equal baseline; all inputs unchanged.')
    print(len(controls[::30] + controls[-7:]), 'supported full CLI outputs equal baseline; CLI exit 0; files unchanged.')
print('No canonical/private run input used; this comparison certifies no new gameplay fact.')

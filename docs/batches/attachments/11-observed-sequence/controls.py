"""Replay synthetic direct and CLI controls; no real run paths or writes."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tests')]
from enemy_phase import evaluate as reference
from tactical_enemy_phase import evaluate
from test_tactical_enemy_phase import sequence, unit


def show(label, result):
    print(label)
    print(json.dumps(result, indent=2, sort_keys=True))


def main():
    print('CODE COMMIT:', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())
    print('BASELINE: e78fa7bcc245071556a408f725105ac63ce7a8e9')
    print('PLAN: ea5eb003d232f1e45a1c31e5ac2bb7412949b56e')
    old = json.loads((ROOT / 'examples/enemy_phase.json').read_text())
    old['player'].pop('current_hp', None)
    old['player'].pop('remaining_uses', None)
    before = copy.deepcopy(old)
    result = reference(old)
    show('DIRECT reference example missing player current HP/durability', result)
    assert old == before and result['death_probability'] == 0 and result['minimum_possible_hp'] == 10
    example = json.loads((ROOT / 'examples/observed_enemy_sequence.json').read_text())
    cases = [('complete_example', example), ('independent_composition', sequence())]
    for field in ('current_hp', 'remaining_uses'):
        p = copy.deepcopy(example); del p['player'][field]
        cases.append(('missing_player_' + field, p))
    p = sequence()
    for entry in p['enemies']:
        entry['unit']['weapon'].update(might=10, hit=100)
    cases.append(('death_absorption', copy.deepcopy(p)))
    p['enemies'][1]['unit']['skills'] = ['counter']
    cases.append(('unsupported_tail_after_certain_death', copy.deepcopy(p)))
    p['enemies'][1]['unit']['skills'] = 'counter'
    cases.append(('malformed_tail_after_certain_death', p))
    p = sequence(); p['player'] = unit(hp=20, damage=10, hit=100)
    p['player'].update(current_hp=12, skills=['vantage'], remaining_uses=2)
    for entry in p['enemies']:
        entry['unit'] = unit(hp=10, damage=3, hit=100)
    cases.append(('newly_active_vantage_early_kill', copy.deepcopy(p)))
    p['player']['remaining_uses'] = 1
    cases.append(('cumulative_durability_refusal', p))
    p = sequence(); p['enemies'][1]['id'] = p['enemies'][0]['id']
    cases.append(('repeated_entity', p))
    for field, values in (('turn', (1, 2)), ('outdoors', (False, True))):
        p = sequence()
        for entry, value in zip(p['enemies'], values):
            entry['context'][field] = value
        cases.append(('conflicting_context_' + field, p))
    p = sequence()
    for entry in p['enemies']:
        entry['unit']['weapon']['hit'] = 100
    p['player']['stats']['lck'] = 100
    p['enemies'][0]['unit']['skills'] = ['hawkeye']
    p['enemies'][1]['unit'].update(skills=['sol', 'hawkeye'])
    p['enemies'][1]['unit']['stats']['skl'] = 100
    cases.append(('dynamic_sol_overkill_refusal', p))
    with tempfile.TemporaryDirectory(prefix='sequence-controls-', dir='.') as tmp:
        for label, payload in cases:
            original = copy.deepcopy(payload)
            direct = evaluate(payload)
            show('DIRECT evaluate: ' + label, direct)
            assert payload == original
            path = Path(tmp) / (label + '.json')
            path.write_text(json.dumps(payload))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            cmd = ['python3', 'tools/tactical_enemy_phase.py', str(path)]
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
            print('COMMAND:', ' '.join(cmd))
            print(r.stdout, end=''); print('STDERR:', r.stderr.strip()); print('EXIT:', r.returncode)
            assert r.returncode == 0 and json.loads(r.stdout) == direct
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
            if 'refusal' in label or label.startswith(('missing_', 'unsupported_', 'malformed_', 'repeated_', 'conflicting_')):
                assert direct['status'] == 'UNKNOWN' and direct['outcome'] is None
        path = Path(tmp) / 'invalid.json'; path.write_text('{')
        cmd = ['python3', 'tools/tactical_enemy_phase.py', str(path)]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        print('COMMAND:', ' '.join(cmd)); print('STDOUT:', r.stdout.strip())
        print('STDERR:', r.stderr.strip()); print('EXIT:', r.returncode)
        assert r.returncode == 2 and path.read_text() == '{'
    print('All synthetic payloads and temporary input files preserved; controls exit 0.')


if __name__ == '__main__':
    main()

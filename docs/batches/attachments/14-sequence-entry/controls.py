"""Replay synthetic CLI workflows without exposing paths or opening a real run."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
from tactical_enemy_phase import evaluate, WEAPON_FIELDS
from tactical_combat import known_weapon

expected = json.loads((ROOT / 'examples/observed_enemy_sequence.json').read_text())
base = []
for entry in expected['enemies']:
    duel = {key: copy.deepcopy(expected[key]) for key in
            ('difficulty', 'mode', 'stats_basis', 'support_state', 'partners', 'observed_inputs_complete')}
    duel.update(attacker=copy.deepcopy(entry['unit']), defender=copy.deepcopy(expected['player']),
                context=copy.deepcopy(entry['context']))
    base.append(duel)
confirmed = ['--confirm-order', '--confirm-unchanged', '--confirm-no-events']


def trial(name, mutate=None, flags=confirmed, guided=False, cancellation=False,
          expected_exit=0, expected_status=None, output=None):
    with tempfile.TemporaryDirectory() as tmp:
        sources = copy.deepcopy(base)
        if mutate:
            mutate(sources)
        args = ['--player-id', expected['player_id']]
        answers = [expected['player_id']]
        originals = []
        for index, (entry, source) in enumerate(zip(expected['enemies'], sources)):
            path = Path(tmp) / ('duel-' + str(index) + '.json')
            path.write_text(json.dumps(source))
            path.chmod(0o400)
            originals.append((path, path.read_bytes()))
            args += ['--enemy', entry['id'], str(path)]
            answers += [str(path), entry['id']]
        answers += ['', 'yes', 'yes', 'yes']
        if guided:
            args = []
        else:
            args += flags
        if output:
            args += ['--output', output]
        stdin = '\n'.join(answers[:-1] if cancellation else answers) + '\n' if guided else ''
        process = subprocess.run([sys.executable, str(ROOT / 'tools/sequence_input.py')] + args,
                                 input=stdin, capture_output=True, text=True, cwd=ROOT)
        assert process.returncode == expected_exit, (name, process.stderr)
        for path, original in originals:
            assert path.read_bytes() == original, name
        payload = json.loads(process.stdout) if process.stdout else None
        if expected_exit == 0:
            assert payload['player'] == sources[0]['defender']
            for assembled, source in zip(payload['enemies'], sources):
                assert assembled['unit'] == source['attacker']
                assert assembled['context'] == source['context']
            status = evaluate(payload)['status']
            if expected_status:
                assert status == expected_status, (name, status)
            if name in ('complete explicit', 'complete guided'):
                assert payload == expected
                assert evaluate(payload) == evaluate(expected)
        else:
            assert payload is None, name
            status = 'refused; no stdout'
        print(name + ': exit ' + str(process.returncode) + '; ' + status + '; source bytes unchanged')
        if name == 'complete guided':
            print('Guided answers: player ID; file 1; enemy ID 1; file 2; enemy ID 2; blank; yes; yes; yes')
            print('Nine answers; zero manually edited JSON; zero retyped observation values.')
            print('Exact existing payload and evaluate result equality: PASS')
        if payload is not None and expected_status == 'UNKNOWN':
            assert evaluate(payload)['outcome'] is None
            print('No numerical outcome; supplied units/context/effects retained verbatim.')
        return payload


print('CODE COMMIT: ' + subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip())
print('COMMAND: python3 docs/batches/attachments/14-sequence-entry/controls.py')
trial('complete explicit')
trial('complete guided', guided=True)
for field in confirmed:
    trial('missing ' + field, flags=[x for x in confirmed if x != field], expected_status='UNKNOWN')
trial('source completeness false', lambda d: d[1].update(observed_inputs_complete=False), expected_status='UNKNOWN')
trial('stale player HP', lambda d: d[1]['defender'].update(current_hp=1), expected_exit=2)
trial('unknown effect tail', lambda d: d[1]['attacker'].update(unknown_effect=['Counter']), expected_status='UNKNOWN')
trial('unsupported Counter tail', lambda d: d[1]['attacker'].update(skills=['counter']), expected_status='UNKNOWN')
trial('fixed context conflict', lambda d: (d[0]['context'].update(turn=1), d[1]['context'].update(turn=2)), expected_status='UNKNOWN')
trial('paired observations', lambda d: [x.update(support_state='paired', partners=[{'id': 'support'}]) for x in d], expected_status='UNKNOWN')
trial('explicitly unarmed player', lambda d: [x['defender'].update(weapon=None, weapon_state='unequipped', remaining_uses=0) for x in d])


def forge(sources):
    unit = sources[1]['attacker']
    unit['weapon'] = {key: value for key, value in known_weapon(unit, 'attacker').items()
                      if key in WEAPON_FIELDS}
    unit['weapon']['might'] += 1


payload = trial('exact forged might', forge)
assert payload['enemies'][1]['unit']['weapon']['might'] == known_weapon(base[1]['attacker'], 'attacker')['might'] + 1
assert evaluate(payload)['outcome'] is not None
trial('EOF before final confirmation', guided=True, cancellation=True, expected_exit=2)
trial('forbidden run destination', output='state/current_run.json', expected_exit=2)
print('EXIT: 0')

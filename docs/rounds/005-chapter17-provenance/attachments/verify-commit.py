"""Reproduce required commit checks from repository root; optionally check private baseline."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout + result.stderr
    print('$ ' + ' '.join(command))
    print('exit', result.returncode)
    if command[0] == 'make':
        lines = output.splitlines()
        print('\n'.join(lines[:4] + ['[relevant output excerpt]'] + lines[-5:]))
    elif command[1:2] == ['tools/map_info.py']:
        q = json.loads(result.stdout)
        fields = ('chapter_id', 'difficulty', 'mode', 'current_turn', 'current_phase',
                  'target_enemy_phase_turn', 'map_confidence', 'schedule_complete',
                  'safe_to_claim_move_safe', 'safe_to_conclude_no_reinforcements', 'warning')
        print(json.dumps({k: q[k] for k in fields}, ensure_ascii=False, indent=2))
        print('Candidate inventory claims:')
        print(json.dumps({w['id']: w['units'] for w in q['candidate_reinforcements']},
                         ensure_ascii=False, indent=2))
        assert len(q['candidate_reinforcements']) == 3
        assert all(w['spawn_phase']['value'] is None and w['timing']['value']['turns'] is None
                   for w in q['candidate_reinforcements'])
        assert not any(c['label'] == 'hard_chapter_17_central:units'
                       for c in q['known_verified_supported'])
        assert any(c['label'] == 'hard_chapter_17_central:units' and c['confidence'] == 'CONFLICTED'
                   for c in q['uncertain_partial_conflicted_unknown'])
        print('Inspected: all three remain conditional candidates; phase UNKNOWN; central inventory excluded from known claims')
    else:
        print(output.strip() or '(no output)')
    if result.returncode:
        raise SystemExit(result.returncode)
    return output


def hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path('data').rglob('*.json'))}


run(['git', 'rev-parse', 'HEAD'])
run(['uname', '-s', '-r'])
run(['sw_vers', '-productVersion'])
run(['python3', '--version'])
run(['make', 'audit'])
run(['make', 'rebuild'])
first = hashes()
run(['make', 'audit'])
run(['make', 'rebuild'])
second = hashes()
run(['make', 'audit'])
assert first.keys() == second.keys() and first == second
print('Two complete rebuilds: file sets and every SHA-256 equal;', len(first), 'canonical JSON files')
print('Canonical manifest SHA-256:', hashlib.sha256(json.dumps(first, sort_keys=True).encode()).hexdigest())
run(['python3', 'tools/fw.py', 'check'])
for turn, phase in ((8, 'player'), (8, 'enemy'), (9, 'player'), (10, 'player')):
    run(['python3', 'tools/map_info.py', '--chapter', '17', '--difficulty', 'hard',
         '--turn', str(turn), '--phase', phase])
run(['git', 'diff', '--check'])
run(['python3', 'docs/rounds/005-chapter17-provenance/attachments/compare-preservation.py'] + sys.argv[1:])
run(['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_chapter17_provenance.py', '-v'])
run(['git', 'status', '--short'])

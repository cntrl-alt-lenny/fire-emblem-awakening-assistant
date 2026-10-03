"""Offline foundation audit; writes evidence only under this round."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

def snapshot():
    paths = sorted((ROOT / 'data').rglob('*.json')) + [ROOT / 'CURRENT_RUN.md']
    paths += sorted(p for p in (ROOT / 'state').rglob('*') if p.is_file())
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def run(name, command):
    r = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (OUT / (name + '.txt')).write_text('$ ' + ' '.join(command) + '\n' + r.stdout + '\nexit_status: ' + str(r.returncode) + '\n')
    return {'command': command, 'exit_status': r.returncode, 'output_file': name + '.txt'}

def main():
    evidence = {'reviewed_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'os': platform.system(), 'os_release': platform.release(), 'python': platform.python_version(), 'commands': []}
    before = snapshot()
    for name, cmd in [('framework', ['python3','tools/fw.py','check']), ('audit-before', ['make','audit']), ('rebuild-one', ['make','rebuild'])]:
        evidence['commands'].append(run(name, cmd))
    first = snapshot()
    evidence['commands'].append(run('rebuild-two', ['make','rebuild']))
    second = snapshot()
    for n, phase in [(7,'player'), (7,'enemy'), (15,'player'), (5,'player'), (17,'player')]:
        evidence['commands'].append(run('map-' + str(n) + '-' + phase, ['python3','tools/map_info.py','--chapter',str(n),'--difficulty','hard','--turn','5','--phase',phase]))
    evidence['commands'].append(run('audit-after', ['make','audit']))
    evidence['commands'].append(run('diff-check', ['git','diff','--check']))
    evidence['hashes'] = {'before': before, 'first': first, 'second': second,
                          'original_drift': [p for p in set(before) | set(first) if before.get(p) != first.get(p)],
                          'second_pass_drift': [p for p in set(first) | set(second) if first.get(p) != second.get(p)]}
    (OUT / 'reproduction.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({k:v for k,v in evidence.items() if k != 'hashes'}, indent=2))
    print('original drift:', evidence['hashes']['original_drift'])
    print('second-pass drift:', evidence['hashes']['second_pass_drift'])

if __name__ == '__main__':
    main()

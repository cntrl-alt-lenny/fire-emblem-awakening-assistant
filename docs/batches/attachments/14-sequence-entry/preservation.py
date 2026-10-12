"""Compare private snapshots without publishing file names or contents."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--compare', required=True, help='private before snapshot JSON')
args = parser.parse_args()
root = Path(__file__).resolve().parents[4]
roots = [root, root.parents[1]]
after = {}
for index, checkout in enumerate(roots):
    for folder in ('data', 'research', 'state'):
        for path in (checkout / folder).rglob('*'):
            if path.is_file():
                after[str(index) + ':' + str(path.relative_to(checkout))] = hashlib.sha256(path.read_bytes()).hexdigest()
    path = checkout / 'CURRENT_RUN.md'
    if path.exists():
        after[str(index) + ':CURRENT_RUN.md'] = hashlib.sha256(path.read_bytes()).hexdigest()
before = json.loads(Path(args.compare).read_text())
assert before == after, 'Private preservation mismatch; inspect privately'
changed = subprocess.check_output(['git', 'diff', '--name-only',
                                  '5c596d42adb3d2a5eeee460032ee20bdd4bb78ba..HEAD'], cwd=root, text=True).splitlines()
allowed = {'tools/sequence_input.py', 'tests/test_sequence_input.py', 'docs/sequence-entry.md',
           'docs/batches/14-sequence-entry.md'}
assert all(name in allowed or name.startswith('docs/batches/attachments/14-sequence-entry/')
           for name in changed), 'Unexpected branch file scope'
print('CODE COMMIT: ' + subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip())
print('COMMAND: python3 docs/batches/attachments/14-sequence-entry/preservation.py --compare PRIVATE_SNAPSHOT')
print(str(len(after)) + ' canonical/research/private/pointer files across primary and Worker checkout unchanged.')
print('No canonical/research/private/shared engine/coverage diff; branch scope allowed.')
print('EXIT: 0')

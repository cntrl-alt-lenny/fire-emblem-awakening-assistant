"""Compare protected bytes against baseline; print no private file content/names."""
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
BASE = 'ec3bceca1d70a4da240a490601602e97c2466de2'
tracked = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
protected = [p for p in tracked if p.startswith(('data/', 'research/', 'state/')) or p == 'CURRENT_RUN.md']
for path in protected:
    old = subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)
    assert (ROOT/path).read_bytes() == old, 'Protected tracked bytes differ'
# Ignored private files: compare before/after all checks by opaque aggregate only.
private = [p for p in (ROOT/'state').rglob('*') if p.is_file() and not p.is_symlink()]
aggregate = hashlib.sha256()
for p in sorted(private):
    aggregate.update(str(p.relative_to(ROOT)).encode()); aggregate.update(p.read_bytes())
print('Protected tracked files unchanged:', len(protected))
print('Private state aggregate:', aggregate.hexdigest(), 'files:', len(private))
print('No canonical/research/pointer edits; exit 0')

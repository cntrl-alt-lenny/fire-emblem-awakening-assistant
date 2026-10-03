# Presentation and link inspection

On 2026-10-03 rendered `research.md` and `search-log.md` using the installed
marked Markdown renderer into temporary HTML outside the repository. Served
with `python3 -m http.server 8764 --bind 127.0.0.1` and inspected the normal
in-app browser's screenshots and accessibility text. Reviewed headings,
source URL wrapping, all matrix rows and scope labels, findings, observation
protocol and search-log table. Columns were readable without overlap; long
URLs wrapped. Corrected ordinal/trigger wording was rerendered and inspected.
Tabs were closed; no source pages or game assets were archived.

A Python `re.findall`/`Path.exists()` check resolved local Markdown links
relative to the containing file: `research.md -> search-log.md`,
`research.md -> verify.py`, `search-log.md -> research.md`; all three exist,
exit 0. Preview links between research/log documents pointed to generated
HTML. The code link was checked against the repository rather than rendered.
Presentation checks do not certify gameplay or external source truth.

Protected SHA-256 baselines/results and full raw CLI stdout remain in private
temporary files, outside the repository. Only counts, comparison outcomes and
sanitized audit/parsed CLI excerpts are public in `checks.txt`. No live run
exists, but this avoids publishing any state contents or hashes regardless.

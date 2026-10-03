# Presentation inspection

2026-10-03: rendered `research.md` and `search-log.md` with the installed
Markdown renderer (marked), into temporary HTML outside the repository.
Served the preview with `python3 -m http.server 8763 --bind 127.0.0.1` and
inspected it in the normal in-app browser. Inspected headings, wrapped source
URLs, matrix header and all disputed-turn/condition rows, interpretation,
follow-up plan and retrieval-log table through screenshots and accessibility
text. Tables were legible without overlapping columns; source URLs wrapped.
No game assets or source-page archives were saved. Preview tabs were closed.

Local-link check: Python `re.findall` over Markdown link targets, resolving
relative targets against each file's parent with `Path.exists()`: 3 targets,
all exist, exit 0 (`research.md`, `search-log.md`, `verify.py`). Preview links
between the two Markdown files were mapped to their generated HTML; the code
link was checked against the repository file, not served as a rendered page.
This is presentation/hygiene evidence, not evidence of gameplay correctness.

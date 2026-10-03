.PHONY: validate test audit rebuild
validate:
	python3 tools/validate_data.py
	python3 tools/audit_phase2.py
	python3 tools/audit_hard.py
test:
	python3 -m unittest discover -s tests -v
audit: validate test
rebuild:
	python3 tools/build_data.py
	python3 tools/enrich_data.py
	python3 tools/phase2_data.py
	python3 tools/coverage_report.py
	python3 tools/hard_data.py
	python3 tools/validate_data.py
	python3 tools/audit_phase2.py
	python3 tools/audit_hard.py

PYTHON ?= python

.PHONY: help smoke test

help:
	@echo "Available targets:"
	@echo "  make smoke  - run minimal scaffold smoke validation"
	@echo "  make test   - run test suite"

smoke:
	PYTHONPATH=src $(PYTHON) -m bci_trans_eeg.cli --smoke

test:
	PYTHONPATH=src $(PYTHON) -m pytest

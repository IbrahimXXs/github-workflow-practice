PYTHON ?= python3
USER_NAME ?= IbrahimXXs

.PHONY: test help summary

test:
	$(PYTHON) -m unittest -v

help:
	$(PYTHON) repo_summary.py --help

summary:
	$(PYTHON) repo_summary.py "$(USER_NAME)"

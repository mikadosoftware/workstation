#CONSTANTS
PYTHON=python

.PHONY: wheel help

#TARGETS
help:
#@echo suppresses echo
	@echo "Simple Build script. only target is 'make wheel'"

wheel:
	rm -rf workstation.egg-info/
	rm -rf dist/
	$(PYTHON) setup.py bdist_wheel

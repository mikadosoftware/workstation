#CONSTANTS
PYTHON=python

#TARGETS
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<

##wheel: Build the wheel for distribution
.PHONY: wheel 
wheel:
	rm -rf workstation.egg-info/
	rm -rf dist/
	$(PYTHON) setup.py bdist_wheel

# useful reference for make: https://swcarpentry.github.io/make-novice/reference

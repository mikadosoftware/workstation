#CONSTANTS
PYTHON=python

#TARGETS
.PHONY : help clear wheel installlocal

help : Makefile
	@sed -n 's/^##//p' $<

##clear: clean setup build stuff
clear :
	rm -rf *.egg-info/
	rm -rf dist/ build/ 

##wheel: Build the wheel for distribution
wheel :
	clear
	$(PYTHON) setup.py bdist_wheel

##installlocal: install locally for testing
installlocal :
	clear
	$(PYTHON) setup.py install


# useful reference for make: https://swcarpentry.github.io/make-novice/reference

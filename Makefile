PYTHON:=python3
PYLINT:=pylint
VERBOSE:=0

SOURCES=$(wildcard src/piston/*.py)

VERBOSE_FLAG=$(if $(shell test $(VERBOSE) -gt 0 && echo 1),--verbose)

check: check-docstring lint

check-docstring: $(patsubst %.py,%.status,$(SOURCES))

lint: $(patsubst %.py,%.lint,$(SOURCES))

%.status: %.py $(SOURCES)
	$(PYTHON) -m doctest $(VERBOSE_FLAG) $< && echo "$$?" > $@

%.lint: %.py
	$(PYLINT) --rcfile lint.rc $(VERBOSE_FLAG) $< && echo "$$?" > $@

PYTHON:=python3
PYLINT:=pylint
VERBOSE:=0

SOURCES=$(wildcard src/piston/*.py)
TESTS=$(wildcard tests/*.py)

VERBOSE_FLAG=$(if $(shell test $(VERBOSE) -gt 0 && echo 1),--verbose)

check: check-docstring check-unit lint

check-docstring: $(patsubst %.py,%.status,$(SOURCES)) README.status

check-unit: $(patsubst %.py,%.status,$(TESTS))

lint: $(patsubst %.py,%.lint,$(SOURCES))

tests/%.status: tests/%.py $(SOURCES)
	PYTHONPATH=src $(PYTHON) -m unittest $< && echo "$$?" > $@

%.status: %.py $(SOURCES)
	$(PYTHON) -m doctest $(VERBOSE_FLAG) $< && echo "$$?" > $@

README.status: README.md $(SOURCES)
	PYTHONPATH=src $(PYTHON) test-readme.py && echo "$$?" > $@

%.lint: %.py
	$(PYLINT) --rcfile lint.rc $(VERBOSE_FLAG) $< && echo "$$?" > $@

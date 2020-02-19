BLACK=cblack
PYTHON:=python3
PYLINT:=pylint
VERBOSE:=0


SOURCES=$(wildcard src/piston/*.py)
TESTS=$(wildcard tests/*.py)

VERBOSE_FLAG=$(if $(shell test $(VERBOSE) -gt 0 && echo 1),--verbose)
PY=PYTHONPATH=src $(PYTHON)

check: check/black check-docstring check-unit lint

check/black:
	$(BLACK) --line-length 80 $$(find . -name *.py)

check-docstring: $(patsubst %.py,%.status,$(SOURCES)) README.status

check-unit: $(patsubst %.py,%.status,$(TESTS))

lint: $(patsubst %.py,%.lint,$(SOURCES))

tests/%.status: tests/%.py $(SOURCES)
	$(PY) -m unittest $< && echo "$$?" > $@

%.status: %.py $(SOURCES) doctest-wrapper.py
	$(PY) doctest-wrapper.py $< && echo "$$?" > $@

README.status: README.md $(SOURCES) doctest-wrapper.py
	$(PY) doctest-wrapper.py $< && echo "$$?" > $@

%.lint: %.py
	$(PYLINT) --rcfile lint.rc $(VERBOSE_FLAG) $< && echo "$$?" > $@

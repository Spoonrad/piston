# Piston is a self-templating markup format

[![Build Status](https://travis-ci.org/mefyl/piston.svg?branch=master)](https://travis-ci.org/mefyl/piston) [![Coverage Status](https://coveralls.io/repos/github/mefyl/piston/badge.svg?branch=master)](https://coveralls.io/github/mefyl/piston?branch=master)

Piston syntax inserts meta-controls inside python basic objects that
can be evaluated to new objects. It is intended to be used in literal
markup languages such as JSON or Yaml that can then easily be
parameterized.

While this approach certainly has drawbacks - mainly mixin metadata
and data - it can also be very lean when JSON/Yaml is almost enough
but not quite. It also fits easily in pipelines that manipulate pure
JSON/Yaml, and lets you have a late evaluation instead of a templated
pre-rendering.

## Basic usage

Piston evaluates any python value.

```python
>>> piston(0)
0
>>> piston({'some': 'python value'})
{'some': 'python value'}

```

It can be passed a context with values to be used while expanding
templates.

```python
>>> piston({'some': 'python {value}'}, context={'value': 'fun'})
{'some': 'python fun'}

```

Expressions are traversed through built-in collections.

```python
>>> piston([0, {'foo': ['{i}']}, 2], context={'i': 1})
[0, {'foo': ['1']}, 2]

```

## Controls

All controls inherit from `piston.Control` and are documented directly
in python docstrings.

    * literal strings are expanded through `str.format`.
    * `$for` and `$in`: Repeat an object for each element of a collection.
    * `$if`, `$then`, `$else`: Conditionally include a value or another.
    * `$merge`: Merge a dictionary inside its parent.

## Context

A context can be passed containing variables accessible in python
expressions.

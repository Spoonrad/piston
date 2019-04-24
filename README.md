# Piston is a self-templating markup format.

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

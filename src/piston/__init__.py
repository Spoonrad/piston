'''Piston, for Python templated object notation, adds templating capabilities to Python objects. '''

import abc
import ast
import collections
import collections.abc

from itertools import chain

import simpleeval

def _specialize(name):
  return '${}'.format(name)

class _SortedDict(dict):

  def __repr__(self):
    return '{{{}}}'.format(', '.join('{!r}: {!r}'.format(k, v) for k, v in sorted(self.items())))

class Control(abc.ABC, metaclass=abc.ABCMeta):

  '''Pluggable piston templating feature.'''

  def __init__(self, name, piston):
    self.__name = name
    self.__piston = piston

  @property
  def name(self):
    '''The name of the control to refer to it in Python objects.'''
    return self.__name

  @property
  def piston(self):
    '''The piston driver.'''
    return self.__piston

  @abc.abstractmethod
  def match(self, python):
    '''Whether this control triggers on the given Python object.'''

  @abc.abstractmethod
  def apply(self, python, match, context=None):
    '''Execute on the given matched Python object.'''

class KeyControl(Control):

  '''Control triggered by a dictionary key.'''

  def match(self, python):
    if isinstance(python, collections.Mapping):
      try:
        return python.pop(_specialize(self.name))
      except KeyError:
        return None
    else:
      return None

class Merge(KeyControl):

  '''A key control that merges its dictionary argument in the current dictionary.

  >>> piston({'a': 0, '$merge': {}, 'c': 2})
  {'a': 0, 'c': 2}
  >>> piston({'a': 0, '$merge': {'b': 1}, 'c': 2})
  {'a': 0, 'b': 1, 'c': 2}
  >>> piston({'a': 0, '$merge': {'$merge': {'b': 1}}, 'c': 2})
  {'a': 0, 'b': 1, 'c': 2}
  '''

  def __init__(self, piston):
    super().__init__('merge', piston=piston)

  def apply(self, python, match, context=None):
    return _SortedDict(#python.__class__(
      chain(python.items(), self.piston.apply(match).items()))

class If(KeyControl):

  '''A key control that conditionnaly evaluate to a value or another.

  >>> piston({'$if': 'True', '$then': 1, '$else': 0})
  1
  >>> piston({'$if': 'False', '$then': 1, '$else': 0})
  0

  Missing element is considered as None:

  >>> piston({'$if': 'True', '$else': 0}) is None
  True
  >>> piston({'$if': 'False', '$then': 1}) is None
  True

  Condition can freely grab from the context:


  >>> piston({'$if': 'a > 2', '$then': 1, '$else': 0}, context={'a': 8})
  1
  >>> piston({'$if': 'a > 2', '$then': 1, '$else': 0}, context={'a': 1})
  0
  >>> piston({'$if': 'a > 2', '$then': 0}) is None
  Traceback (most recent call last):
  ...
  simpleeval.NameNotDefined: 'a' is not defined for expression 'a > 2'

  Condition must be a string:

  >>> piston({'$if': {}, '$then': 1, '$else': 0})
  Traceback (most recent call last):
  ...
  Exception: condition must be a string
  '''

  def __init__(self, piston):
    super().__init__('if', piston=piston)

  def apply(self, python, match, context=None):
    if not isinstance(match, str):
      raise Exception('condition must be a string')
    then = python.pop(_specialize('then'), None)
    else_ = python.pop(_specialize('else'), None)
    if simpleeval.simple_eval(match, names=context or {}):
      return then
    else:
      return else_

class For(KeyControl):

  '''A key control that instatiate the current value for all items in a collection.

  >>> piston({'$for': 'i', '$in': '[0, 1, 2, 3]', 'a': '{i}'})
  [{'a': '0'}, {'a': '1'}, {'a': '2'}, {'a': '3'}]

  The '$in' key is required:

  >>> piston({'$for': '[]'})
  Traceback (most recent call last):
  ...
  Exception: missing $in

  '''

  def __init__(self, piston):
    super().__init__('for', piston=piston)

  def apply(self, python, match, context=None):
    in_ = python.pop(_specialize('in'), None)
    if in_ is None:
      raise Exception('missing $in')
    return [
      self.piston.apply(
        python, context=dict(chain([(match, v)], context.items if context is not None else [])))
      for v in self.piston.eval(in_, names=context)
    ]


class Format(Control):

  '''Expand literal strings using Python format.

  >>> piston('some {value}', context={'value': 'thing'})
  'some thing'
  '''

  def __init__(self, piston):
    super().__init__('for', piston=piston)

  def match(self, python):
    return python if isinstance(python, str) else None

  def apply(self, python, match, context=None):
    return match.format(**(context or {}))


class Piston:

  '''The main driver for evaluating Piston expressions.'''

  def __init__(self):
    self.__controls = [
      For(self),
      Format(self),
      If(self),
      Merge(self),
    ]

  @property
  def controls(self):
    '''The controls enabled when evaluating.'''
    return self.__controls

  def eval(self, exp, **kwargs):
    '''Evaluate Python expression safely.'''
    evaluate = simpleeval.EvalWithCompoundTypes(**kwargs)
    return evaluate.eval(exp)

  def apply(self, python, context=None):
    '''Evaluate a Piston expression.'''
    for ctrl in self.__controls:
      match = ctrl.match(python)
      if match is not None:
        return ctrl.apply(python, match, context=context)
    if isinstance(python, collections.abc.Mapping):
      return _SortedDict(#python.__class__(
        (k, self.apply(v, context)) for k, v in python.items())
    elif isinstance(python, collections.abc.Collection) and not isinstance(python, str):
      return python.__class__(self.apply(v, context) for v in python)
    else:
      return python


def piston(python, context=None):
  '''Evaluate a Piston value.

  Basic python values evaluate to themselves:

  >>> piston({})
  {}
  >>> piston({'bar': 0, 'baz': 1})
  {'bar': 0, 'baz': 1}

  '''
  piston = Piston()
  return piston.apply(python, context=context)

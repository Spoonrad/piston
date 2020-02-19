"""Jinja integration with Piston."""

import jinja2
import piston


class Format(piston.Control):

  """Expand literal strings using Jinja templating.

  >>> piston('some {{value}}', context={'value': 'thing'})
  'some thing'
  """

  def __init__(self, piston):
    super().__init__("jinja", piston=piston)

  def match(self, python):
    return python if isinstance(python, str) else None

  def apply(self, python, match, context=None):
    return jinja2.Template(match).render(**(context or {}))

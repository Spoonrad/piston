import doctest
import piston
import sys

path = sys.argv[1]
if path.endswith(".py") and path.startswith("src/"):
  import importlib
  import inspect

  path = path[:-3][4:].replace("/", ".")
  if path.endswith(".__init__"):
    path = path[:-9]
  module = importlib.import_module(path)
  controls = []
  for _, c in inspect.getmembers(module):
    if (
      inspect.isclass(c)
      and not inspect.isabstract(c)
      and issubclass(c, piston.Control)
    ):
      controls.append(c)
  p = piston.Piston(controls)
  failures, tests = doctest.testmod(module, globs={"piston": p.apply})
else:
  failures, tests = doctest.testfile(
    sys.argv[1], globs={"piston": piston.piston}
  )

if failures > 0:
  exit(1)

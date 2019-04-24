import doctest
import piston
doctest.testfile("README.md", globs={"piston": piston.piston})

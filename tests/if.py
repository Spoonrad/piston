import piston
import unittest


class If(unittest.TestCase):
  def test_recurse(self):
    self.assertEqual(
      piston.piston(
        {"$if": "True", "$then": {"$if": "True", "$then": "recurse"}}
      ),
      "recurse",
    )

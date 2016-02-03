from unittest import TestCase
from monoalphabetic_cypher_tools import reverse_dict


class TestReverse_dict(TestCase):
  def test_reverse_dict(self):
    d = {'a':'b', 'c':'d', 'e':'f'}
    self.assertDictEqual(reverse_dict(d), {'b':'a', 'd':'c', 'f':'e'})

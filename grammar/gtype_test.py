from .gtype import GType
import unittest

class GTypeTest(unittest.TestCase):
    def test_gtype_unit(self):
        lines = [":Unit"]
        obj = GType()
        self.assertTrue(obj.match(lines, 0,0))

    def test_type_with_space(self):
        lines = [": Unit"]
        obj = GType()
        self.assertTrue(obj.match(lines, 0,0))

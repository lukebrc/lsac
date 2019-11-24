from .gname import GName
import unittest

class GWordTest(unittest.TestCase):
    def test_one_letter_name(self):
        obj = GName()
        lines = ["a"]
        self.assertTrue( obj.match(lines, 0,0) )
        self.assertEqual("a", obj.get_name())
        pos = obj.get_current_pos()
        self.assertEqual(1, pos[0])

    def test_spaces(self):
        obj = GName()
        lines = [" \t test_name"]
        self.assertTrue( obj.match(lines, 0,3) )
        pos = obj.get_current_pos()
        self.assertEqual(1, pos[0])

    def test_underscore_name(self):
        obj = GName()
        lines = ["", "aBBa"]
        self.assertTrue( obj.match(lines, 1,0) )
        pos = obj.get_current_pos()
        self.assertEqual("aBBa", obj.get_name())
        self.assertEqual(2, pos[0])

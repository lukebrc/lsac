from .gname import GName
import unittest

class GWordTest(unittest.TestCase):
    def test_one_letter_name(self):
        obj = GName()
        lines = ["a"]
        self.assertTrue( obj.match(lines, 0,0) )
        self.assertEqual("a", obj.get_name())
        self.assertEqual((0,0), obj.get_start_pos())
        self.assertEqual((0,0), obj.get_last_pos())

    def test_spaces(self):
        obj = GName()
        lines = [" \t test_name"]
        self.assertTrue( obj.match(lines, 0,3) )
        self.assertEqual((0,len(lines[0])-1), obj.get_last_pos())

    def test_underscore_name(self):
        obj = GName()
        lines = ["", "aBBa"]
        self.assertTrue( obj.match(lines, 1,0) )
        pos = obj.get_last_pos()
        self.assertEqual("aBBa", obj.get_name())
        self.assertEqual((1,3), obj.get_last_pos())

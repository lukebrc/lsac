from .gword import GWord
import unittest

class GWordTest(unittest.TestCase):
    def test_one_char(self):
        obj = GWord("a")
        lines = ["a"]
        self.assertTrue( obj.match(lines, 0,0) )
        self.assertEqual((0,0), obj.get_end_pos())

    def test_two_chars(self):
        obj = GWord("aB")
        lines = ["aBBa"]
        self.assertTrue( obj.match(lines, 0,0) )
        self.assertEqual((0,0), obj.get_start_pos())
        self.assertEqual((0,1), obj.get_end_pos())

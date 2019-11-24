from .gword import GWord
import unittest

class GWordTest(unittest.TestCase):
    def test_one_char(self):
        obj = GWord("a")
        lines = ["a"]
        self.assertTrue( obj.match(lines, 0,0) )
        pos = obj.get_current_pos()
        self.assertEqual(1, pos[0])

    def test_two_chars(self):
        obj = GWord("aB")
        lines = ["aBBa"]
        self.assertTrue( obj.match(lines, 0,0) )
        pos = obj.get_current_pos()
        self.assertEqual(0, pos[0])
        self.assertEqual(2, pos[1])

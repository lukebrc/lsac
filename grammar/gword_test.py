from .gword import GWord
from iterator.text_iterator import TextIterator
import unittest


class GWordTest(unittest.TestCase):
    def test_one_char(self):
        obj = GWord("a")
        text = "a"
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        self.assertEqual((0,1), obj.get_end_pos().tuple())

    def test_two_chars(self):
        obj = GWord("aB")
        text = "aBBa"
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        self.assertEqual((0, 0), obj.get_start_pos().tuple())
        self.assertEqual((0, 1), obj.get_end_pos().tuple())

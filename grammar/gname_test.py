from .gname import GName
from iterator.text_iterator import TextIterator
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class GWordTest(unittest.TestCase):
    def test_one_letter_name(self):
        obj = GName()
        text = "a"
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        self.assertEqual("a", obj.get_name())
        self.assertEqual((0, 0), obj.get_start_pos().tuple())
        self.assertEqual((0, 0), obj.get_last_pos().tuple())

    def test_spaces(self):
        obj = GName()
        text = " \t test_name"
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        self.assertEqual((0, len(text)-1), obj.get_last_pos().tuple())

    def test_underscore_name(self):
        obj = GName()
        text = "\naBBa"
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        self.assertEqual("aBBa", obj.get_name())
        self.assertEqual((1, 3), obj.get_last_pos().tuple())

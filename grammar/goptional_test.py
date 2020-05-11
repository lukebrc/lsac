from .goptional import GOptional
from .gword import GWord
from .gname import GName
from iterator.text_iterator import TextIterator
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class GOptionalTest(unittest.TestCase):
    def test_single_word(self):
        word = "a"
        obj = GOptional(GWord(word))
        text = word
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        self.assertEqual("a", obj.get_found_obj().get_text())
        self.assertEqual((0, 0), obj.get_start_pos().tuple())
        self.assertEqual((0, 0), obj.get_last_pos().tuple())

    def test_empty_str(self):
        obj = GOptional(GName())
        text = ""
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))

    def test_underscore_name(self):
        obj = GOptional(GName())
        text = "\naBBa"
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        self.assertEqual("aBBa", obj.get_found_obj().get_name())
        self.assertEqual((1, 3), obj.get_last_pos().tuple())

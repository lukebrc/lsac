from .gany import GAny
from iterator.text_iterator import TextIterator
import unittest
import logging

# logging.basicConfig(filename="log.txt", filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class GAnyTest(unittest.TestCase):

    def test_empty_text(self):
        text = ""
        text_iterator = TextIterator(text)
        gany = GAny()
        self.assertFalse(gany.match(text_iterator))
        self.assertEqual("", gany.get_text())

    def test_single_line(self):
        text = "asdf"
        text_iterator = TextIterator(text)
        gany = GAny()
        self.assertTrue(gany.match(text_iterator))
        pos = gany.get_last_pos()
        self.assertEqual("asdf", gany.get_text())
        self.assertEqual((0, 3), pos.tuple())

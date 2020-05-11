from .gchoice import GChoice
from .gname import GName
from .gword import GWord
from .gsequence import GSequence
from iterator.text_iterator import TextIterator

import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class GChoiceTest(unittest.TestCase):
    def test_single_word(self):
        a = GWord("A")
        b = GWord("B")
        obj = GChoice([a, b])
        text = "B"
        text_iterator = TextIterator(text)
        self.assertTrue(obj.match(text_iterator))
        pos = obj.get_last_pos()
        self.assertEqual(1, pos[0])
        self.assertEqual(b, obj.get_chosen())

    def test_sequence(self):
        int_choose = GWord("int")
        float_choose = GWord("float")
        tchoice = GChoice([int_choose, float_choose])

        def_choice = GChoice([GWord(";"), GWord("= 1;")])
        name = GName()
        seq = GSequence([tchoice, name, def_choice])
        text = "int num;"
        text_iterator = TextIterator(text)
        self.assertTrue(seq.match(text_iterator))
        self.assertEqual("num", name.get_name())
        self.assertEqual(int_choose, tchoice.get_chosen())


from .bracket_exp import BracketExp
from .gany import GAny
from iterator.text_iterator import TextIterator
import unittest
import logging

# logging.basicConfig(filename="log.txt", filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class BracketExpTest(unittest.TestCase):

    def test_fun_arguments(self):
        exp = BracketExp("(", ")")
        exp.set_recursive_definitions([exp, GAny()])
        text = "(a,b,c)"
        text_iterator = TextIterator(text)
        self.assertTrue(exp.match(text_iterator))
        pos = exp.get_end_pos()
        self.assertEqual((1, 0), pos.tuple())
        body = exp.get_body().get_text()
        self.assertEqual("a,b,c", body)

    def test_empty_braces(self):
        exp = BracketExp("(", ")")
        text = "()"
        text_iterator = TextIterator(text)
        self.assertTrue(exp.match(text_iterator))
        pos = exp.get_end_pos()
        self.assertEqual((1,0), pos.tuple())
        body = exp.get_body().get_text()
        self.assertEqual("", body)

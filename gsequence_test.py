from grammar.gsequence import GSequence
from grammar.gword import GWord
from grammar.gtype import GType
from grammar.gname import GName
from grammar.goptional import GOptional
from grammar.bracket_exp import BracketExp
from iterator.text_iterator import TextIterator
import unittest
import logging

logging.basicConfig(level=logging.DEBUG)


class GSequenceTest(unittest.TestCase):

    def test_3_words(self):
        defs = GSequence( [GWord("def"), GWord("def"), GWord("def")] )
        lines = ["def def", "   def"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        self.assertEqual((1,len(lines[1])-1), defs.get_last_pos().tuple(), "Position should be in last line")

    def test_3_words_invalid(self):
        defs = GSequence( [GWord("def"), GWord("def"), GWord("def")] )
        lines = ["def def", "   abc"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertFalse( defs.match(text_iterator) )

    def test_def_name(self):
        defs = GSequence( [GWord("def"), GName() ])
        lines = ["def Test_Fun123", ""]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos()
        self.assertEqual((0, 14), pos.tuple())
        self.assertEqual("Test_Fun123", defs.get_definitions()[1].get_name())

    def test_def_fun_incomplete(self):
        defs = GSequence([GWord("def"), GName()])
        lines = ["def Test_Fun123(a: Integer)", ""]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos().tuple()
        self.assertEqual(0, pos[0])
        self.assertEqual(len("def Test_Fun123") - 1, pos[1])
        self.assertEqual("Test_Fun123", defs.get_definitions()[1].get_name())

    def test_optional_type(self):
        defs = GSequence([GWord("def"), GName(), GOptional(GWord(":")), GName(), GWord("{")])
        lines = ["def test: test_name {"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos()
        self.assertEqual((0, 19), pos)

    def test_optional_invalid(self):
        defs = GSequence( [GWord("def"), GName(), GOptional(GWord(":")), GName(), GWord("{")] )
        lines = ["def test {"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertFalse( defs.match(text_iterator) )

    def test_bracket_exp_def(self):
        bracket_exp = BracketExp("(", ")")
        defs = GSequence([GWord("def"), bracket_exp])
        # defs.set_recursive_definitions([defs])
        lines = ["def(a, b, c) "]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos().tuple()
        self.assertEqual((0, len(lines[0])-2), pos)
        self.assertEqual("a, b, c", bracket_exp.get_body().get_text())

    def test_bracket_exp_fun(self):
        bracket_exp = BracketExp("(", ")")
        gname = GName()
        defs = GSequence([GWord("def"), gname, bracket_exp])
        # defs.set_recursive_definitions([defs])
        lines = ["def TestFun(a, b, c)"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos().tuple()
        self.assertEqual((0, len(lines[0])-1), pos)
        self.assertEqual("a, b, c", bracket_exp.get_body().get_text())
        self.assertEqual("TestFun", gname.get_name())

    def test_bracket_exp_fun2(self):
        bracket_exp = BracketExp("(", ")")
        rdefs = GWord("a, b, c")
        bracket_exp.set_recursive_definitions([rdefs])
        defs = GSequence([GWord("def"), GName(), bracket_exp])
        # defs.set_recursive_definitions([defs])
        lines = ["def TestFun_123(a, b, c) "]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos().tuple()
        self.assertEqual((0, len(lines[0])-2), pos)
        self.assertNotEqual(None, bracket_exp.get_body())

    def test_bracket_exp2(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), BracketExp("{", "}") ] )
        defs.set_recursive_definitions([defs])
        lines = ["def TestFun_123(a, b, c) {", " print(123) ", "print(456)", "}"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos()
        self.assertEqual(len(lines), pos[0])

    def test_bracket_exp3(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), GType() ] )
        lines = ["def TestFun_123(a, b, c) :Unit"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos()
        self.assertEqual(len(lines), pos[0])

    def test_bracket_exp4(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), GType(), GWord("="), BracketExp("{", "}") ] )
        lines = ["def TestFun_123(a, b, c) :Unit = {", " print(123) ", "print(456)", "}" ]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue(defs.match(text_iterator))
        pos = defs.get_last_pos()
        self.assertEqual(len(lines), pos[0])

    def test_nested_bracket_exps(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), BracketExp("{", "}") ] )
        nestedFun = "def hello() { print(\"hello\") }"
        lines = ["def TestFun_123(a, b, c) {", nestedFun, "}"]
        text = "\n".join(lines)
        text_iterator = TextIterator(text)
        self.assertTrue( defs.match(text_iterator) )
        pos = defs.get_last_pos()
        self.assertEqual(len(lines), pos[0])


if __name__ == '__main__':
    unittest.main()

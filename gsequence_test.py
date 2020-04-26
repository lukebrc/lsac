from grammar.gsequence import GSequence
from grammar.gword import GWord
from grammar.gtype import GType
from grammar.gname import GName
from grammar.goptional import GOptional
from grammar.bracket_exp import BracketExp
import unittest


class GSequenceTest(unittest.TestCase):

    def test_3_words(self):
        defs = GSequence( [GWord("def"), GWord("def"), GWord("def")] )
        lines = ["def def", "   def"]
        self.assertTrue( defs.match(lines, 0,0) )
        self.assertEqual((1,len(lines[1])-1), defs.get_end_pos(), "Position should be in last line")

    def test_3_words_invalid(self):
        defs = GSequence( [GWord("def"), GWord("def"), GWord("def")] )
        lines = ["def def", "   abc"]
        self.assertFalse( defs.match(lines, 0,0) )

    def test_def_name(self):
        defs = GSequence( [GWord("def"), GName() ])
        lines = ["def Test_Fun123", ""]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual((0,14), pos)
        self.assertEqual("Test_Fun123", defs.get_definitions()[1].get_name())

    def test_def_fun_incomplete(self):
        defs = GSequence( [GWord("def"), GName() ])
        lines = ["def Test_Fun123(a: Integer)", ""]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual(0, pos[0])
        self.assertEqual(len("def Test_Fun123"), pos[1])
        self.assertEqual("Test_Fun123", defs.get_definitions()[1].get_name())

    def test_optional_type(self):
        defs = GSequence( [GWord("def"), GName(), GOptional(GWord(":")), GName(), GWord("{")] )
        lines = ["def test: test_name {"]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual((0,20), pos)

    def test_optional_invalid(self):
        defs = GSequence( [GWord("def"), GName(), GOptional(GWord(":")), GName(), GWord("{")] )
        lines = ["def test {"]
        self.assertFalse( defs.match(lines, 0,0) )

    def test_bracket_exp1(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")") ] )
        defs.set_recursive_definitions([defs])
        lines = ["def TestFun_123(a, b, c) "]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual((0,len(lines[0]-2)), pos)

    def test_bracket_exp2(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), BracketExp("{", "}") ] )
        defs.set_recursive_definitions([defs])
        lines = ["def TestFun_123(a, b, c) {", " print(123) ", "print(456)", "}" ]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual(len(lines), pos[0])

    def test_bracket_exp2(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), GType() ] )
        lines = ["def TestFun_123(a, b, c) :Unit"]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual(len(lines), pos[0])

    def test_bracket_exp3(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), GType(), GWord("="), BracketExp("{", "}") ] )
        lines = ["def TestFun_123(a, b, c) :Unit = {", " print(123) ", "print(456)", "}" ]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual(len(lines), pos[0])

    def test_nested_bracket_exps(self):
        defs = GSequence( [GWord("def"), GName(), BracketExp("(", ")"), BracketExp("{", "}") ] )
        nestedFun = "def hello() { print(\"hello\") }"
        lines = ["def TestFun_123(a, b, c) {", nestedFun, "}" ]
        self.assertTrue( defs.match(lines, 0,0) )
        pos = defs.get_end_pos()
        self.assertEqual(len(lines), pos[0])


if __name__ == '__main__':
    unittest.main()

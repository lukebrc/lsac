from gdefinition import GDefinition
from gword import GWord
from gname import GName
import unittest


class GDefinitionTest(unittest.TestCase):
    def test_3_words(self):
        defs = GDefinition( [GWord("def"), GWord("def"), GWord("def")] )
        lines = ["def def", "   def"]
        pos = defs.match(lines, [0,0])
        self.assertEqual(2, pos[0], "Position should be after last line")

    def test_3_words_invalid(self):
        defs = GDefinition( [GWord("def"), GWord("def"), GWord("def")] )
        lines = ["def def", "   abc"]
        pos = defs.match(lines, [0,0])
        self.assertEqual([0,0], pos)

    def test_def_name(self):
        defs = GDefinition( [GWord("def"), GName() ])
        lines = ["def Test_Fun123", ""]
        pos = defs.match(lines, [0,0])
        self.assertEqual(2, pos[0])
        self.assertEqual("Test_Fun123", defs.getDefinitions()[1].getName())

    def test_def_fun_incomplete(self):
        defs = GDefinition( [GWord("def"), GName() ])
        lines = ["def Test_Fun123(a: Integer)", ""]
        pos = defs.match(lines, [0,0])
        self.assertEqual(0, pos[0])
        self.assertEqual(len("def Test_Fun123"), pos[1])
        self.assertEqual("Test_Fun123", defs.getDefinitions()[1].getName())


if __name__ == '__main__':
    unittest.main()

from .gchoice import GChoice
from .gname import GName
from .gword import GWord
from .gsequence import GSequence
import unittest


class GChoiceTest(unittest.TestCase):
    def test_single_word(self):
        a = GWord("A")
        b = GWord("B")
        obj = GChoice( [a, b] )
        lines = ["B"]
        self.assertTrue( obj.match(lines, 0,0) )
        pos = obj.get_last_pos()
        self.assertEqual(1, pos[0])
        self.assertEqual(b, obj.get_chosen())

    def test_sequence(self):
        int_choose = GWord("int")
        float_choose = GWord("float")
        tchoice = GChoice( [int_choose, float_choose] )

        def_choice = GChoice( [GWord(";"), GWord("= 1;")] )
        name = GName()
        seq = GSequence( [tchoice, name, def_choice] )
        lines = ["int num;"]
        self.assertTrue( seq.match(lines, 0,0) )
        self.assertEqual("num", name.get_name())
        self.assertEqual(int_choose, tchoice.get_chosen())


from .bracket_exp import BracketExp
import unittest

class BracketExpTest(unittest.TestCase):
    def test_fun_arguments(self):
        exp = BracketExp("(", ")")
        lines = ["(a,b,c)"]
        self.assertTrue( exp.match(lines, (0,0)) )
        pos = exp.get_current_pos()
        self.assertEqual( (1,0), pos )


from parsers import scalaparser
import unittest

parser = scalaparser.ScalaParser()
#lines = '''class A {
#    private var _a: A = null
#}'''.split('\n')



class GSequenceTest(unittest.TestCase):
    def test_empty_class(selfs):
        lines = '''class A() {
        }'''.split('\n')

        objMap = parser.parseClasses(lines)
        assert ('A' in objMap)


    # def test_simple_class(self):
    #     lines = '''class A() {
    #         def fun() {}
    #     }'''.split('\n')
    #
    #     objMap = parser.parseClasses(lines)
    #     assert ('A' in objMap)
        #assert ('_a' in objMap['A'])

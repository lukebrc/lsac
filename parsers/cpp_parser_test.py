from cpp_parser import CppParser

import unittest
import logging

logging.basicConfig(level=logging.DEBUG)


class GSequenceTest(unittest.TestCase):

    def test_simple_class(self):
        simple_class = """
            class A {
                class AB {
                }
            }
        """
        parser = CppParser(simple_class)
        objects = parser.parse_objects()
        print(objects)

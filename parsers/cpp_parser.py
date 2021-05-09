from .code_model import CodeModel
from grammar.gword import GWord
from grammar.gname import GName
from grammar.bracket_exp import BracketExp
from grammar.gsequence import GSequence
from grammar.gany import GAny
from grammar.goptional import GOptional
from iterator.text_iterator import TextIterator

SCALA_TYPE = GSequence( [GWord(":"), GName] )


class ClassDefinition(GSequence):
    def __init__(self):
        super().__init__([GWord("class"), GName(), BracketExp("{", "}") ])


class CppParser(object):
    def __init__(self, text):
        self._text_iterator = TextIterator(text)
        self._definitions = [
            ClassDefinition(),
            GSequence( [GAny()] )
        ]
        for df in self._definitions:
            df.set_recursive_definitions(self._definitions)

    def parse_objects(self):
        for definition in self._definitions:
            print(definition)
            if definition.match(self._text_iterator):
                pos = definition.get_last_pos()
                print("matches: pos {}", pos)
                print("parsed definition: {}".format(definition))
                continue
        print(self._definitions)
        return self.create_code_model(self._definitions)

    def create_code_model(self, definitions):
        code = CodeModel()
        for d in definitions:
            d.accept(code)

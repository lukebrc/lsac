from abc import ABC, abstractmethod
from iterator.text_iterator import TextIterator


class GObject(ABC):
    def __init__(self):
        self._start_pos = None
        self._end_pos = None

    def match(self, text_iterator: TextIterator):
        text_iterator.skip_whitespace()
        start_pos = text_iterator.current_pos().copy()
        end_pos = self.find_end_pos(text_iterator)
        if end_pos is not None:
            self._start_pos = start_pos
            self._end_pos = end_pos
            return True
        return False

    # sprawdz czy znaleziono ten obiekt w lines poczynajac od pozycji (r,c)
    # jesli tak, to zwroc koncowa pozycje, w.p.p. None
    @abstractmethod
    def find_end_pos(self, text_iterator):
        pass

    def get_start_pos(self):
        return self._start_pos

    def get_end_pos(self):
        return self._end_pos

    @staticmethod
    def parse_definitions(lines, definitions):
        t = TextIterator(lines)
        def_list = []
        for definition in definitions:
            print(definition)
            if definition.match(t):
                end_pos = definition.get_end_pos()
                def_list.append(definition)
                print("matches: pos {}", end_pos)
                print("parsed definition: {}".format(definition))
                continue
        if len(def_list) == 0:
            return GAny()
        if len(def_list) == 1:
            return def_list[0]
        return GSequence(def_list)

    def set_next_pos(self, r, c):
        self._current_pos = (r,c)

    def set_recursive_definitions(self, definitions):
        self._definitions = definitions


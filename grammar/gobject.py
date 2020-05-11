from iterator.text_iterator import TextIterator
from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)


class GObject(ABC):
    def __init__(self):
        self._start_pos = None
        # pozycja ostatniego znaku gobject
        self._last_pos = None

    def match(self, text_iterator: TextIterator):
        start_pos = text_iterator.current_pos().copy()
        try:
            text_iterator.skip_whitespace()
            last_pos = self.find_last_pos(text_iterator)
            if last_pos is not None:
                self._start_pos = start_pos
                self._last_pos = last_pos
                return True
        except StopIteration:
            log.debug("GObject:match - StopIteration")
        text_iterator.set_current_pos(start_pos)
        return False

    # sprawdz czy znaleziono ten obiekt w lines poczynajac od aktualnej pozycji w text_iterator
    # jesli tak, to zwroc koncowa pozycje, w.p.p. None
    @abstractmethod
    def find_last_pos(self, text_iterator: TextIterator):
        pass

    def get_start_pos(self):
        return self._start_pos

    def get_last_pos(self):
        return self._last_pos

    @staticmethod
    def parse_definitions(lines, definitions):
        t = TextIterator(lines)
        def_list = []
        for definition in definitions:
            print(definition)
            if definition.match(t):
                last_pos = definition.get_last_pos()
                def_list.append(definition)
                continue
        if len(def_list) == 0:
            return GAny()
        if len(def_list) == 1:
            return def_list[0]
        return GSequence(def_list)

    def set_next_pos(self, r, c):
        self._last_pos = (r,c)

    def set_recursive_definitions(self, definitions):
        self._definitions = definitions


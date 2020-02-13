from abc import ABC, abstractmethod

class GObject(ABC):
    def __init__(self):
        self._start_pos = None
        self._end_pos = None

    def match(self, lines, r,c):
        (r,c) = GObject.skip_whitespace(lines, r, c)
        start_pos = (r,c)
        end_pos = self.do_match(lines, r,c)
        if end_pos is not None:
            self._start_pos = start_pos
            self._end_pos = end_pos
            return True
        return False

    # sprawdz czy znaleziono ten obiekt w lines poczynajac od pozycji (r,c)
    # jesli tak, to zwroc koncowa pozycje, w.p.p. None
    @abstractmethod
    def do_match(self, lines, r,c):
        pass

    def get_start_pos(self):
        return self._start_pos

    def get_end_pos(self):
        return self._end_pos

    @staticmethod
    def get_next_pos(lines, r, c):
        c += 1
        if c >= len(lines[r]):
            c = 0
            r += 1
        return (r,c)

    @staticmethod
    def is_valid_pos(lines, r, c):
        if r < len(lines)-1:
            return True
        if r >= len(lines):
            return False
        return c < len( lines[r] )

    @staticmethod
    def skip_whitespace(lines, r, c):
        while(GObject.is_valid_pos(lines, r,c) and GObject.is_whitespace(lines, r,c)):
            (r,c) = GObject.get_next_pos(lines, r,c)
        return (r,c)

    @staticmethod
    def is_whitespace(lines, r,c):
        c = lines[r][c]
        return c == ' ' or c == '\t' or c == '\n'

    @staticmethod
    def parse_definitions(lines, definitions):
        (r,c) = (0,0)
        def_list = []
        while r < len(lines):
            for definition in definitions:
                print(definition)
                if definition.match(lines, r, c):
                    (r,c) = definition.get_end_pos()
                    def_list.append(definition)
                    print("matches: pos {}", (r,c))
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


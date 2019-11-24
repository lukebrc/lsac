from abc import ABC, abstractmethod

class GObject(ABC):
    def __init__(self):
        self._current_pos = None

    @abstractmethod
    def match(self, lines, r,c):
        pass

    def get_current_pos(self):
        return self._current_pos

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

    def set_next_pos(self, r, c):
        self._current_pos = (r,c)


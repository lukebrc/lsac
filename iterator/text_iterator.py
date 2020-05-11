from .position import Position
import logging

log = logging.getLogger(__name__)


class TextIterator(object):
    def __init__(self, text: str):
        self._lines = text.split("\n")
        self._pos = Position()
        self._marked_pos = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_after_end():
            raise StopIteration()
        char = self.current_char()
        self._pos.move_next(self._lines)
        return char

    def prev(self):
        if (self._r, self._c) == (0, 0):
            raise StopIteration()
        char = self.current_char()
        self._pos.move_prev()
        return char

    def skip_whitespace(self):
        while self.is_valid_pos() and self.is_whitespace():
            log.debug("Skipping whitespace")
            self.__next__()

    def is_whitespace(self):
        # if self._lines[]
        char = self._pos.get_char(self._lines)
        return char == ' ' or char == '\t' or char == '\n' or char is None

    def is_valid_pos(self):
        return self._pos.is_valid(self._lines)

    def get_lines(self):
        return self._lines

    def current_char(self):
        if self.is_after_end() or len(self._lines[self._pos.r]) == 0:
            return None
        return self._lines[self._pos.r][self._pos.c]

    def current_pos(self):
        return self._pos

    def set_current_pos(self, pos):
        self._pos = pos

    def is_after_end(self):
        return self._pos.is_after_end(self._lines)

    def eol_reached(self):
        return self._pos.eol_reached(self._lines)

    def get_substr(self, start, end):
        pos = start
        text = ''
        while pos != end:
            text += pos.get_char(self._lines)
            pos.move_next(self._lines)
        return text

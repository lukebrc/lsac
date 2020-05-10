from iterator.text_iterator import TextIterator
from .gobject import GObject
from .gany import GAny
from .gword import GWord
import logging

log = logging.getLogger(__name__)


class BracketExp(GObject):
    def __init__(self, lbrace, rbrace):
        self._lbrace = lbrace
        self._rbrace = rbrace
        self._lbrace_count = 0
        self._rbrace_count = 0
        self._body = GAny()
        self._definitions = None

    def match(self, text_iterator: TextIterator):
        log.debug("match start")
        if self._find_matching_braces(text_iterator):
            content_start = self._start_pos.move(1, text_iterator.get_lines())
            content_end = self._end_pos.move(-1, text_iterator.get_lines())
            inside_text = text_iterator.get_substr(content_start, content_end)
            log.debug("Parsing inside definition {}\n".format(inside_text))
            if self._definitions is not None:
                self._body = GObject.parse_definitions(inside_text, self._definitions)
                self._body.set_recursive_definitions(self._definitions)
            else:
                self._body = GWord(inside_text)
            return True
        return False

    def find_last_pos(self, lines, r, c):
        raise NotImplementedError()

    def get_body(self):
        return self._body

    def __str__(self):
        return self._lbrace + str(self._body) + self._rbrace

    def _find_matching_braces(self, text_iterator):
        self._start_pos = text_iterator.current_pos().copy()
        text_iterator.skip_whitespace()
        char = text_iterator.current_char()
        if char != self._lbrace:
            log.debug("invalid start character: {}".format(char))
            return False
        self._start_pos = text_iterator.current_pos().copy()
        it = iter(text_iterator)
        next(it)
        self._lbrace_count = 1
        while not text_iterator.is_after_end():
            log.debug("pos: {}\n".format(text_iterator.current_pos))
            char = next(it)
            if char == self._lbrace:
                self._lbrace_count += 1
            elif char == self._rbrace:
                self._rbrace_count += 1
            if self._lbrace_count == self._rbrace_count:
                self._end_pos = text_iterator.current_pos()
                return True
        log.debug("end reached: {}\n".format(text_iterator.current_pos))
        return False

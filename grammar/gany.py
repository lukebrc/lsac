from .gobject import GObject
from iterator.text_iterator import TextIterator
import logging

log = logging.getLogger(__name__)


class GAny(GObject):
    def __init__(self, text = None):
        self._text = text

    def find_last_pos(self, text_iterator: TextIterator):
        raise NotImplementedError()

    def match(self, text_iterator: TextIterator):
        self._start_pos = text_iterator.current_pos().copy()
        self._text = ''
        while True:
            if text_iterator.is_valid_pos():
                self._text += text_iterator.current_char()
            if text_iterator.is_after_end() or text_iterator.eol_reached():
                break
            next(text_iterator)
        self._last_pos = text_iterator.current_pos().copy()
        if not text_iterator.is_after_end():
            next(text_iterator)
        return True

    def __str__(self):
        return "GAny({})".format(self._text)

    def get_text(self):
        return self._text

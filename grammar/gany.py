from .gobject import GObject
from iterator.text_iterator import TextIterator
import logging

log = logging.getLogger(__name__)


class GAny(GObject):
    def __init__(self):
        self._text = ""

    def find_last_pos(self, text_iterator: TextIterator):
        raise NotImplementedError()

    def match(self, text_iterator: TextIterator):
        try:
            text_iterator.skip_whitespace()
            self._start_pos = text_iterator.current_pos().copy()
            self._text = ''
            while True:
                if text_iterator.is_valid_pos():
                    self._text += next(text_iterator)
                if text_iterator.current_pos().r > self._start_pos.r:
                    break
                self._last_pos = text_iterator.current_pos().copy()
        except StopIteration:
            log.debug("GAny - StopIteration")
        return len(self._text) > 0

    def __str__(self):
        return "GAny({})".format(self._text)

    def get_text(self):
        return self._text

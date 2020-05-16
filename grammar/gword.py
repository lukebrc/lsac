from grammar.gobject import GObject
from iterator.text_iterator import TextIterator
import logging

log = logging.getLogger(__name__)


class GWord(GObject):
    def __init__(self, word):
        self._word = word

    def find_last_pos(self, text_iterator: TextIterator):
        pos = None
        for i in range(0, len(self._word)):
            pos = text_iterator.current_pos()
            v = next(text_iterator)
            if v != self._word[i]:
                log.debug("Word: {} mismatch at pos {}".format(self._word, pos))
                return None
        log.debug("Found word: {} at pos: {}".format(self._word, pos))
        return pos

    def __str__(self):
        return '"{}"'.format(self._word)

    def get_text(self):
        return self._word

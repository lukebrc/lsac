from grammar.gobject import GObject
from iterator.text_iterator import TextIterator


class GWord(GObject):
    def __init__(self, word):
        self._word = word

    def find_end_pos(self, text_iterator: TextIterator):
        for i in range(0, len(self._word)):
            v = next(text_iterator)
            if v != self._word[i]:
                return None
        # TODO: catch
        pos = text_iterator.current_pos().copy()
        return pos.move_prev(text_iterator.get_lines())

    def __str__(self):
        return '"{}"'.format(self._word)

    def get_text(self):
        return self._word

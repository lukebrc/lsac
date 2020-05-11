from grammar.gobject import GObject
from iterator.text_iterator import TextIterator
import logging

log = logging.getLogger(__name__)


class GName(GObject):
    def __init__(self):
        self._name = ''

    def find_last_pos(self, text_iterator: TextIterator):
        self._name = ''
        it = iter(text_iterator)
        while text_iterator.is_valid_pos():
            last_pos = text_iterator.current_pos().copy()
            char = next(it)
            if not GName.is_name_char(char):
                break
            self._name += char
        if len(self._name) > 0:
            log.debug("GName:last_pos {}".format(last_pos))
            return last_pos
        return None

    def get_name(self):
        return self._name

    @staticmethod
    def is_name_char(char):
        return char.isalnum() or (char == '_')

    def __str__(self):
        return "GName({})".format(self._name)

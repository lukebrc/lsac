from grammar.gobject import GObject
from iterator.text_iterator import TextIterator


class GOptional(GObject):
    def __init__(self, obj):
        self._object = obj
        self._foundObj = None

    def find_last_pos(self, text_iterator: TextIterator):
        do_match = self._object.match(text_iterator)
        if do_match:
            self._foundObj = self._object
            self._start_pos = self._foundObj.get_start_pos()
            self._last_pos = self._foundObj.get_last_pos()
            return self.get_last_pos()
        return None

    def __str__(self):
        return "GOptional({})".format(self._foundObj or "")

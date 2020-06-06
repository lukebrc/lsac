from grammar.gobject import GObject
from iterator.text_iterator import TextIterator
import logging

log = logging.getLogger(__name__)


class GOptional(GObject):
    def __init__(self, obj):
        self._object = obj
        self._found_obj = None

    def match(self, text_iterator: TextIterator):
        try:
            start_pos = text_iterator.current_pos().copy()
            if self._object.match(text_iterator):
                self._found_obj = self._object
                self._start_pos = self._object.get_start_pos().copy()
                self._last_pos = self._object.get_last_pos().copy()
                return True
        except StopIteration:
            log.debug("GObject:match - StopIteration")
        text_iterator.set_current_pos(start_pos)
        return True

    def find_last_pos(self, text_iterator: TextIterator):
        raise Exception("NOT IMPLEMENTED")

    def get_found_obj(self):
        return self._found_obj

    def __str__(self):
        return "GOptional({})".format(self._found_obj or "")

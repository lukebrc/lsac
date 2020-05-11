from .gobject import GObject
from iterator.text_iterator import TextIterator


class GChoice(GObject):
    def __init__(self, obj_list):
        self._objList = obj_list
        self._chosen = None

    def match(self, text_iterator: TextIterator):
        for df in self._objList:
            text_iterator.skip_whitespace()
            if df.match(text_iterator):
                self._chosen = df
                return True
        return False

    def get_chosen(self):
        return self._chosen

    def find_last_pos(self, text_iterator):
        raise Exception('NOT IMPLEMENTED')

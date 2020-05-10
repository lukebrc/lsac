from iterator.text_iterator import TextIterator
from .gobject import GObject


class GSequence(GObject):
    def __init__(self, def_list):
        self._defList = def_list

    def find_last_pos(self, text_iterator: TextIterator):
        for i in range(0, len(self._defList)):
            df = self._defList[i]
            if not df.match(text_iterator):
                return None
        return text_iterator.current_pos()

    def get_definitions(self):
        return self._defList

    def set_recursive_definitions(self, definitions):
        super().set_recursive_definitions(definitions)
        for df in self._defList:
            df.set_recursive_definitions(definitions)

    def __str__(self):
        list_str = map(str, self._defList)
        return "GSequence({})".format(",".join(list_str))

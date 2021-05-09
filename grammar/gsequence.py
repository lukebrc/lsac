from iterator.text_iterator import TextIterator
from .gobject import GObject
import logging

log = logging.getLogger(__name__)


class GSequence(GObject):
    def __init__(self, def_list):
        self._defList = def_list

    def find_last_pos(self, text_iterator: TextIterator):
        last_pos = None
        for i in range(0, len(self._defList)):
            df = self._defList[i]
            if not df.match(text_iterator):
                return None
            last_pos = df.get_last_pos()
            log.debug("last_pos: {}".format(last_pos))
        return last_pos

    def get_definitions(self):
        return self._defList

    def set_recursive_definitions(self, definitions):
        super().set_recursive_definitions(definitions)
        for df in self._defList:
            df.set_recursive_definitions(definitions)

    def to_dict(self):
        return {
            "defList": [elem.to_dict() for elem in self._defList]
        }

    def load_dict_int(self, dict):
        self._defList = []
        for e in dict['defList']:
            class_name = e['class_name']
            elem = GObject.create_instance(class_name)
            elem.load_dict(e)

    def accept(self, visitor):
        visitor.visit(self)
        for d in self._defList:
            d.accept(visitor)

    def __str__(self):
        list_str = map(str, self._defList)
        return "GSequence({})".format(",".join(list_str))

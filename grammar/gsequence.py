from .gobject import GObject


class GSequence(GObject):
    def __init__(self, defList):
        self._defList = defList

    def find_end_pos(self, lines, r,c):
        for i in range(0, len(self._defList)):
            df = self._defList[i]
            (r,c) = GObject.skip_whitespace(lines, r, c)
            if not df.match(lines, r,c):
                return None
            (r,c) = df.get_end_pos()
            if i != len(self._defList)-1:
                (r,c) = GObject.get_next_pos(lines, r,c)
        return (r,c)

    def get_definitions(self):
        return self._defList

    def set_recursive_definitions(self, definitions):
        super().set_recursive_definitions(definitions)
        for df in self._defList:
            df.set_recursive_definitions(definitions)

    def __str__(self):
        list_str = map(str, self._defList)
        return "GSequence({})".format(",".join(list_str))

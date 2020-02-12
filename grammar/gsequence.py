from .gobject import GObject


class GSequence(GObject):
    def __init__(self, defList):
        self._defList = defList

    def match(self, lines, r,c):
        for df in self._defList:
            (r,c) = GObject.skip_whitespace(lines, r, c)
            if not df.match(lines, r,c):
                return False
            (r,c) = df.get_current_pos()
        self.set_next_pos(r,c)
        return True

    def get_definitions(self):
        return self._defList

    def __str__(self):
        seq_str = "GSequence("
        for df in self._defList:
            seq_str += str(df)
        list_str = map(str, self._defList)
        return "GSequence({})".format(",".join(list_str))

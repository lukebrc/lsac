from .gobject import GObject

class GSequence(GObject):
    def __init__(self, defList):
        self._defList = defList

    def match(self, lines, currentPos):
        (r,c) = (currentPos[0], currentPos[1])
        for df in self._defList:
            (r,c) = GObject.skip_whitespace(lines, r, c)
            if not df.match(lines, (r,c)):
                return False
            (r,c) = df.get_current_pos()
        self.set_next_pos(r,c)
        return True

    def get_definitions(self):
        return self._defList

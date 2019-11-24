from grammar.gobject import GObject

class GOptional(GObject):
    def __init__(self, obj):
        self._object = obj
        self._foundObj = None

    def match(self, lines, currentPos):
        row = currentPos[0]
        col = currentPos[1]
        doMatch = self._object.match(lines, currentPos)
        if doMatch:
            self._foundObj = self._object
            pos = self._object.get_current_pos()
            self.set_next_pos(pos[0], pos[1])
        return True

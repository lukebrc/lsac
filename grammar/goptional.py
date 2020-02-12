from grammar.gobject import GObject


class GOptional(GObject):
    def __init__(self, obj):
        self._object = obj
        self._foundObj = None

    def match(self, lines, r,c):
        doMatch = self._object.match(lines, r,c)
        if doMatch:
            self._foundObj = self._object
            pos = self._object.get_current_pos()
            self.set_next_pos(pos[0], pos[1])
        return True

    def __str__(self):
        return "GOptional({})".format(self._foundObj or "")

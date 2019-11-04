from .gobject import GObject

class GAny(GObject):
    def match(self, lines, currentPos):
        return [currentPos[0]+1, 0]


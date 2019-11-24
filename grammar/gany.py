from .gobject import GObject

class GAny(GObject):
    def match(self, lines, currentPos):
        self.set_next_pos(currentPos[0]+1,0)
        return True


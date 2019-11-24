from .gobject import GObject


class GAny(GObject):
    def match(self, lines, r,c):
        self.set_next_pos(r+1,0)
        return True


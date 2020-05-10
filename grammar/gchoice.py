from .gobject import GObject


class GChoice(GObject):
    def __init__(self, objList):
        self._objList = objList
        self._chosen = None

    def match(self, lines, r,c):
        for df in self._objList:
            (r,c) = GObject.skip_whitespace(lines, r, c)
            if df.match(lines, r,c):
                (r,c) = df.get_last_pos()
                self.set_next_pos(r,c)
                self._chosen = df
                return True
        return False

    def get_chosen(self):
        return self._chosen

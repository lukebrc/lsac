from grammar.gobject import GObject


class GWord(GObject):
    def __init__(self, word):
        self._word = word

    def match(self, lines, r,c):
        if lines[r][c:].find(self._word) == 0:
            c += len(self._word)
            if c >= len(lines[r]):
                r += 1
                c = 0
            self.set_next_pos(r, c)
            return True
        return False


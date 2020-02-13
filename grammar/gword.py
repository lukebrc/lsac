from grammar.gobject import GObject


class GWord(GObject):
    def __init__(self, word):
        self._word = word

    def do_match(self, lines, r,c):
        if lines[r][c:].find(self._word) == 0:
            return (r,c+len(self._word)-1)
        return None

    def __str__(self):
        return '"{}"'.format(self._word)

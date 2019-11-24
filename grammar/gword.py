from grammar.gobject import GObject

class GWord(GObject):
    def __init__(self, word):
        self._word = word

    def match(self, lines, currentPos):
        row = currentPos[0]
        col = currentPos[1]
        if lines[row][col:].find(self._word) == 0:
            col += len(self._word)
            if col >= len(lines[row]):
                row += 1
                col = 0
            self.set_next_pos(row, col)
            return True
        return False


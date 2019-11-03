
class GWord(object):
    def __init__(self, word):
        self._word = word

    def match(self, lines, currentPos):
        row = currentPos[0]
        col = currentPos[1]
        if lines[row][col:].find(self._word) == 0:
            return [row, col+len(self._word)]
        return currentPos


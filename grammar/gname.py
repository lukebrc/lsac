class GName(object):
    def __init__(self):
        self._name = ''

    def match(self, lines, currentPos):
        self._name = ''
        r = currentPos[0]
        c = currentPos[1]
        if r >= len(lines):
            return currentPos
        while c < len(lines[r]):
            if not GName.isNameChar(lines[r][c]):
                return [r,c]
            self._name += lines[r][c]
            c += 1
            if c >= len(lines[r]):
                return [r+1, 0]

    def getName(self):
        return self._name

    @staticmethod
    def isNameChar(char):
        return char.isalnum() or (char == '_')


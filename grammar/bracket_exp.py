from .gobject import GObject

class BracketExp(GObject):
    def __init__(self, lbrace, rbrace):
        self._lbrace = lbrace
        self._rbrace = rbrace
        self._lbrace_count = 0
        self._rbrace_count = 0
        self._body = ''

    def match(self, lines, currentPos):
        r = currentPos[0]
        c = currentPos[1]

        if lines[r][c] != self._lbrace:
            return currentPos

        while True:
            if lines[r][c] == self._lbrace:
                self._lbrace_count += 1
            elif lines[r][c] == self._rbrace:
                self._rbrace_count += 1
            (r,c) = GObject.movePos(lines, r, c)
            if self._lbrace_count == self._rbrace_count:
                return [r,c]
            if r >= len(lines):
                return currentPos
            self._body += lines[r][c]


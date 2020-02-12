from .gobject import GObject

class BracketExp(GObject):
    def __init__(self, lbrace, rbrace):
        self._lbrace = lbrace
        self._rbrace = rbrace
        self._lbrace_count = 0
        self._rbrace_count = 0
        self._body = ''

    def match(self, lines, r,c):
        if lines[r][c] != self._lbrace:
            return False
        self._lbrace_count = 1
        (r,c) = GObject.get_next_pos(lines, r, c)
        while True:
            if lines[r][c] == self._lbrace:
                self._lbrace_count += 1
            elif lines[r][c] == self._rbrace:
                self._rbrace_count += 1
            (r,c) = GObject.get_next_pos(lines, r, c)
            if self._lbrace_count == self._rbrace_count:
                self.set_next_pos(r,c)
                return True
            if r >= len(lines):
                return False
            self._body += lines[r][c]

    def __str__(self):
        return self._lbrace + str(self._body) + self._rbrace

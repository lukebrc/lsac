import logging

log = logging.getLogger(__name__)


class Position(object):
    def __init__(self, r=0, c=0):
        self.r = r
        self.c = c

    def move(self, num, lines):
        pos = Position(self.r, self.c)
        if num >= 0:
            for i in range(0, num):
                pos.move_next(lines)
        else:
            for i in range(0, -num):
                pos.move_prev(lines)
        return pos

    def move_next(self, lines):
        if self.is_after_end(lines):
            raise StopIteration()
        log.debug("Moving next {},{}".format(self.r, self.c))
        self.c += 1
        if self.c >= len(lines[self.r]):
            self.c = 0
            self.r += 1
        return self

    def move_prev(self, lines):
        if self.c == 0:
            self.r -= 1
            self.c = len(lines[self.r]) - 1
        else:
            self.c -= 1
        return self

    def get_char(self, lines):
        log.debug("get_char: {},{}".format(self.r, self.c))
        log.debug(lines)
        if len(lines[self.r]) > 0:
            return lines[self.r][self.c]
        return None

    def is_after_end(self, lines):
        if self.r < len(lines) - 1:
            return False
        if self.r >= len(lines):
            return True
        return self.c >= len(lines[self.r])

    def eol_reached(self, lines):
        if self.r >= len(lines) or len(lines[self.r]) == 0:
            return True
        return self.c == len(lines[self.r]) - 1

    def is_valid(self, lines):
        if self.r < len(lines)-1:
            return True
        if self.r >= len(lines):
            return False
        return self.c < len(lines[self.r]) or self.c == 0

    def tuple(self):
        return self.r, self.c

    def copy(self):
        return Position(self.r, self.c)

    def __str__(self):
        return "({},{})".format(self.r, self.c)

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

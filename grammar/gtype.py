from grammar.gobject import GObject

class GType(GObject):
    def __init__(self):
        self._type = ''

    def match(self, lines, currentPos):
        self._name = ''
        r = currentPos[0]
        c = currentPos[1]
        if r >= len(lines):
            return False
        if lines[r][c] != ':':
            return False
        (r,c) = GObject.get_next_pos(lines, r,c)
        (r,c) = GObject.skip_whitespace(lines, r, c)
        while GObject.isValidPos(lines, r,c):
            if not GType.is_type_char(lines[r][c]):
                break
            self._type += lines[r][c]
            (r,c) = GObject.get_next_pos(lines, r, c)
        if len(self._type) > 0:
            self.set_next_pos(r,c)
            return True
        return False

    def get_type(self):
        return self._type

    @staticmethod
    def is_type_char(char):
        return char.isalnum() or (char == '_')

from grammar.gobject import GObject


class GName(GObject):
    def __init__(self):
        self._name = ''

    def match(self, lines, r,c):
        self._name = ''
        if r >= len(lines):
            return False
        while GObject.is_valid_pos(lines, r,c):
            if not GName.is_name_char(lines[r][c]):
                self.set_next_pos(r,c)
                break
            self._name += lines[r][c]
            (r,c) = GObject.get_next_pos(lines, r, c)
        if len(self._name) > 0:
            self.set_next_pos(r,c)
            return True
        return False

    def get_name(self):
        return self._name

    @staticmethod
    def is_name_char(char):
        return char.isalnum() or (char == '_')

    def __str__(self):
        return "GName({})".format(self._name)

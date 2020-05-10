from grammar.gobject import GObject


class GName(GObject):
    def __init__(self):
        self._name = ''

    def find_last_pos(self, lines, r, c):
        self._name = ''
        if r >= len(lines):
            return None
        while GObject.is_valid_pos(lines, r,c):
            if not GName.is_name_char(lines[r][c]):
                break
            self._name += lines[r][c]
            end_pos = (r,c)
            (r,c) = GObject.get_next_pos(lines, r, c)
        if len(self._name) > 0:
            return end_pos
        return None

    def get_name(self):
        return self._name

    @staticmethod
    def is_name_char(char):
        return char.isalnum() or (char == '_')

    def __str__(self):
        return "GName({})".format(self._name)

from grammar.gobject import GObject


class GOptional(GObject):
    def __init__(self, obj):
        self._object = obj
        self._foundObj = None

    def find_last_pos(self, lines, r, c):
        do_match = self._object.match(lines, r,c)
        if do_match:
            self._foundObj = self._object
            self._start_pos = self._foundObj.get_start_pos()
            self._last_pos = self._foundObj.get_last_pos()
            return self.get_last_pos()
        return GOptional._get_previous_pos(lines, r,c)

    def __str__(self):
        return "GOptional({})".format(self._foundObj or "")

    def _get_previous_pos(lines, r,c):
        if c > 0:
            return (r, c)
        if r == 0:
            return (0, 0)
        r -= 1
        c = len(lines[r]) - 1
        return (r, c)


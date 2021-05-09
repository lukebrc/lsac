class CodeModel(object):
    def __init__(self):
        self._classes = []
        self._functions = []
        self._variables = []

    def visit(self, gobject):
        # if gobject is ClassDefinition:
            # zaladuj nazwe klasy
        pass


class ClassData(object):
    def __init__(self):
        self._data = {
            'name': '',
            'path': '',
            'start_row': 0,
            'start_col': 0,
            'end_row': 0,
            'end_col': 0,
        }


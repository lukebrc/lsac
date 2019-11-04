from abc import ABC, abstractmethod

class GObject(ABC):
    def __init__(self):
        self._found = False

    @abstractmethod
    def match(self, lines, currentPos):
        pass

    @staticmethod
    def movePos(lines, r, c):
        c += 1
        if c >= len(lines[r]):
            c = 0
            r += 1
        return (r,c)

    def setFound(self):
        self._found = True

    def isFound(self):
        return self._found

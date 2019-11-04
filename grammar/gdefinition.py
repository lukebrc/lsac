from .gobject import GObject

class GDefinition(GObject):
    def __init__(self, defList):
        self._defList = defList

    def match(self, lines, currentPos):
        pos = [currentPos[0], currentPos[1]]
        for df in self._defList:
            pos2 = df.match(lines, pos)
            if(pos2 == pos):
                return currentPos
            if pos2[0] >= len(lines):
                return pos2
            pos = GDefinition.movePos(lines, pos2)
        return pos

    @staticmethod
    def movePos(lines, pos):
        while True:
            if pos[0] >= len(lines):
                return pos
            if pos[1] >= len(lines[pos[0]]):
                pos = [pos[0]+1, 0]
                continue
            if lines[pos[0]][pos[1]] == ' ' or lines[pos[0]][pos[1]] == '\t':
                pos = [pos[0], pos[1]+1]
                continue
            else:
                return pos

    def getDefinitions(self):
        return self._defList

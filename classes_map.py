
class ClassesMap(object):
    def __init__(self):
        self._fileObjects = {}

    def addObjects(self, fileName, objMap):
        self._fileObjects[fileName] = objMap

    def getObjects(self, fileName):
        return self._fileObjects[fileName]

    def __str__(self):
        classesStr = ''
        for fn in self._fileObjects:
            classesStr += "File: {}\n".format(fn)
            classesStr += str(self._fileObjects[fn]) + "\n"
        return classesStr

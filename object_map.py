
class ObjectMap(object):
    def __init__(self):
        self._objects = {}

    def addClass(self, name):
        if not name in self._objects:
            self._objects[name] = set()

    def addFunction(self, className, funId):
        self.addClass(className)
        self._objects[className].add(funId)

    def addVar(self, className, varId):
        self.addClass(className)
        self._objects[className].add(varId)

    def contains(self, name):
        return name in self._objects

    def __str__(self):
        ret = ''
        for className in self._objects:
            ret += "\t{}:\n".format(className)
            classObjects = self._objects[className]
            for objName in classObjects:
                ret += "\t\t{}\n".format(objName)
        return ret


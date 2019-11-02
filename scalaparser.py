import re
from classes_map import ClassesMap
from scala_file_parser import ScalaFileParser


class ScalaParser(object):
    def __init__(self):
        self._classesMap = ClassesMap()

    def parseClasses(self, fileName):
        with open(fileName, 'r') as file:
            lines = file.readlines()
        fileParser = ScalaFileParser(lines)
        objects = fileParser.parseObjects()
        self._classesMap.addObjects(fileName, objects)

    def getAllObjects(self):
        return self._classesMap

    def getFileObjects(self, fileName):
        return self._classesMap.getObjects(fileName)

    def completeMe(self, currentLine):
        r1 = re.findall(r"\s*(.*)\.(.*)\s*", currentLine)
        if len(r1) == 0:
            return []
        varName = r1[0][0]
        funPref = r1[0][1]
        if varName in self._objMap:
            return self._objMap[varName]
        className = self._findVarClass(varName)
        if className is None:
            return []
        return self._getFunctionsStartingWith(className, funPref)

    def _getFunctionsStartingWith(self, className, funPref):
        funcs = self._objMap[className]
        if len(funPref) == 0:
            return funcs
        matchingFuncs = []
        for name in self._objMap[className]:
            if ScalaParser._prefixMatches(funPref, name):
                matchingFuncs.append(name)
        return matchingFuncs

    @staticmethod
    def _prefixMatches(pref, word):
        return word.find(pref) == 0

    def _findVarClass(self, varName):
        if varName == "this":
            return self._findNearestClass(varName)
        return self._findNearestDefinition(varName)

    def _findNearestClass(self, varName):
        currentRange = self._currentRange
        for i in range(currentRange.start-1, -1, -1):
            line = self._lines[i]
            if self._isClassDef(line):
                className = ScalaParser._getClassName(line)
                if (className is not None) and (className in self._objMap):
                    return className
        return None

    def _findNearestDefinition(self, varName):
        currentRange = self._currentRange
        for i in range(currentRange.start-1, -1, -1):
            line = self._lines[i]
            if ScalaParser._isVarDef(line):
                varDef = ScalaParser._getVarType(line)
                if (varDef is not None) and (varDef in self._objMap):
                    return varDef
        return None


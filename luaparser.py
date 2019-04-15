import re


class LuaParser(object):
    def __init__(self):
        self.__objMap = {}

    def parseClasses(self, lines, currentRange, filename):
        self.__lines = lines
        self.__currentRange = currentRange
        self.__moduleObject = LuaParser.__findModuleObject()
        self.__currentFilename = filename
        i = 0
        while i < len(lines):
            line = lines[i]
            if LuaParser.__isFunDef(line):
                while line.find(')') == -1:
                    if i+1 >= len(lines):
                        line += lines[i+1]
                        i += 1
                className, funName, funArgs = LuaParser.__parseFunDef(line)
                if className not in self.__objMap:
                    self.__objMap[className] = []
                self.__objMap[className].append(funName + "(" + funArgs + ")")
        self.__replaceModuleClass()
        return self.__objMap

    def completeMe(self, currentLine):
        r1 = re.findall(r"\s*(.*)\.(.*)\s*", currentLine)
        if len(r1) == 0:
            return []
        varName = r1[0][0]
        funPref = r1[0][1]
        if varName in self.__objMap:
            return self.__objMap[varName]
        className = self.__findVarClass(varName)
        if className is None:
            return []
        return self.__getFunctionsStartingWith(className, funPref)

    def __findModuleObject(self):
        for i in range(len(self.__lines)-1, -1, -1):
            line = self.__lines(i)
            if LuaParser.__isClassReturn(line):
                return LuaParser.__getModuleClass(line)
        return None

    def __getFunctionsStartingWith(self, className, funPref):
        funcs = self.__objMap[className]
        if len(funPref) == 0:
            return funcs
        matchingFuncs = []
        for name in self.__objMap[className]:
            if LuaParser.__prefixMatches(funPref, name):
                matchingFuncs.append(name)
        return matchingFuncs

    @staticmethod
    def __prefixMatches(pref, word):
        return word.find(pref) == 0

    def __findVarClass(self, varName):
        if varName == "this":
            return self.__findNearestClass(varName)
        return self.__findNearestDefinition(varName)

    def __findNearestClass(self, varName):
        currentRange = self.__currentRange
        for i in range(currentRange.start-1, -1, -1):
            line = self.__lines[i]
            if self.__isClassDef(line):
                className = LuaParser.__getClassName(line)
                if (className is not None) and (className in self.__objMap):
                    return className
        return None

    def __findNearestDefinition(self, varName):
        currentRange = self.__currentRange
        for i in range(currentRange.start-1, -1, -1):
            line = self.__lines[i]
            if LuaParser.__isVarDef(line):
                varDef = LuaParser.__getVarType(line)
                if (varDef is not None) and (varDef in self.__objMap):
                    return varDef
        return None

    @staticmethod
    def __isVarDef(line):
        r1 = re.findall(r"\s*va[rl]\s+(\w+)(\s*:\s*\w+)?\s*=(.*)", line)
        return len(r1) > 0

    @staticmethod
    def __isClassDef(line):
        return re.match(r"\s*(class|object)\s+(\w+)", line)

    @staticmethod
    def __getVarType(line):
        r1 = re.findall(r"\s*(\w+)\s*:\s*(\w+)\s*", line)
        if len(r1) != 0:
            return r1[0][1]
        r1 = re.findall(r"\s*(\w+)\s*=\s*new\s+(\w+)", line)
        if len(r1) != 0:
            return r1[0][1]
        r1 = re.findall(r"\s*(\w+)\s*=\s*(\w+)\(.*\)", line)
        if len(r1) != 0:
            return r1[0][1]
        return None

    @staticmethod
    def __getClassName(line):
        match = re.findall(r"\s*class\s+(\w+)", line)
        if len(match) == 0:
            match = re.findall(r"\s*object\s+(\w+)", line)
        return match[0]

    def __parseClassArguments(self, className, line):
        r1 = re.findall(r"\s*class\s+(\w+)(.*)", line)
        argsStr = r1[0][1]
        for arg in argsStr.split(','):
            argName, argType = LuaParser.__parseArgDecl(arg)
            self.__objMap[className].add(argName)

    @staticmethod
    def __parseArgDecl(argStr):
        if argStr.find(':') == -1:
            return argStr, ''
        r1 = re.findall(r"\s*(\w+)\s*:\s*(\w+)", argStr)
        return r1[0][0], r1[0][1]

    @staticmethod
    def __isFunDef(line):
        return re.match(r"\s*function ([a-z0-9A-Z_.:]+).*\(", line)

    @staticmethod
    # returns tuple (className, funName, funArgs)
    def __parseFunDef(line):
        if LuaParser.__isClassFun(line):
            return LuaParser.__parseClassFunDef(line)
        return LuaParser.__parseSimpleFunDef(line)

    @staticmethod
    # returns tuple (className, funName, funArgs)
    def __parseClassFunDef(line):
        r1 = re.findall(r"\s*function\s+([\w.]+)([.:])(\w+)\((.*)\)",
                        line)
        return r1[0][0], r1[0][2], r1[0][3]

    def __parseSimpleFunDef(line):
        r1 = re.findall(r"\s*function\s+([\w.]+)\((.*)\)", line)
        return '', r1[0][0], r1[0][1]

    def __replaceModuleClass(self):
        if self.__moduleObject is None:
            return
        for k in self.__objMap:
            if k.find(self.__moduleObject) == 0:
                postfix = k[len(self.__moduleObject):]
                # _M.A.f -> filename.A.f
                newName = self.__currentFilename[0:-4] + postfix
                self.__objMap[newName] = self.__objMap[k]

    @staticmethod
    def __parseVarDef(line):
        r1 = re.findall(r"\s*(private|public)?\s+va[rl]\s+(\w+)", line)
        if len(r1) == 0:
            return None, None
        varName = r1[0][-1]
        varType = LuaParser.__getVarType(line)
        return varName, varType
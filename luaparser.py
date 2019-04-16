import re


class LuaParser(object):
    def __init__(self):
        self.__objMap = {}

    def parseClasses(self, lines, currentRange, currentPath):
        self.__lines = lines
        self.__currentRange = currentRange
        self.__moduleObject = self.__findModuleObject()
        self.__currentPath = currentPath
        i = 0
        while i < len(lines):
            line = lines[i]
            if LuaParser.__isFunDef(line):
                while line.find(')') == -1:
                    if i+1 >= len(lines):
                        line += lines[i+1]
                        i += 1
                self.__processFunDef(line)
            i += 1
        self.__replaceModuleClass()
        return self.__objMap

    def completeMe(self, currentLine, currentPath):
        r1 = re.findall(r"\s*([\w.]+)[.:](\w*)\s*", currentLine)
        if len(r1) == 0:
            return []
        varName = r1[0][0]
        funPref = r1[0][1]
        completions = LuaParser.__findObjMapRecursive(varName, self.__objMap)
        if len(completions) > 0:
            if len(funPref) > 0:
                completions = filter(lambda x: x.find(funPref) == 0,
                                     completions)
                completions = list(completions)
            return completions
        className = self.__findVarType(varName)
        if className is None:
            return []
        return self.__getFunctionsStartingWith(className, funPref)

    def __findModuleObject(self):
        for i in range(len(self.__lines)-1, -1, -1):
            line = self.__lines[i]
            if LuaParser.__isClassReturn(line):
                return LuaParser.__getModuleClass(line)
        return None

    @staticmethod
    def __isClassReturn(line):
        return re.match(r"\s*return\s+\w+", line) or \
            re.match(r"\s*return\(\s*\w+\s*\)", line)

    @staticmethod
    def __getModuleClass(line):
        if re.match(r"\s*return \w+", line):
            r1 = re.findall(r"return (\w+)", line)
        else:
            r1 = re.findall(r"return\((\w+)\)", line)
        return r1[0]

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

    def __findVarType(self, varName):
        if varName == "self":
            return self.__findNearestClass()
        return self.__findNearestDefinition(varName)

    def __findNearestClass(self):
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
            if LuaParser.__isVarDef(line, varName):
                varDef = LuaParser.__getVarType(line, varName)
                if (varDef is not None) and (varDef in self.__objMap):
                    return varDef
        return None

    @staticmethod
    def __isVarDef(line, varName):
        return re.match(r"\s*{}\s+=\s*(.+):new".format(varName), line)

    @staticmethod
    def __isClassDef(line):
        return re.match(r"\s*function\s+[\w.]+[.:]\w+", line)

    @staticmethod
    def __getVarType(line, varName):
        r1 = re.findall(r"\s*{}\s+=\s*(.+):new".format(varName), line)
        return r1[0]

    @staticmethod
    def __getClassName(line):
        match = re.findall(r"\s*function\s+([\w.]+)[.:](\w+)", line)
        return match[0][0]

    @staticmethod
    def __isFunDef(line):
        return re.match(r"\s*function ([a-z0-9A-Z_.:]+).*\(", line)

    def __processFunDef(self, line):
        if LuaParser.__isClassFun(line):
            return self.__processClassFunDef(line)
        return self.__processSimpleFunDef(line)

    @staticmethod
    # is it class function?
    def __isClassFun(line):
        return re.match(r"\s*function\s+[\w.]+[.:]\w+\(", line)

    def __processClassFunDef(self, line):
        r1 = re.findall(r"\s*function\s+([\w.]+)([.:])(\w+)\((.*)\)",
                        line)
        res = r1[0]
        className = res[0]
        funName = res[2]
        funArgs = res[3]
        if className not in self.__objMap:
            self.__objMap[className] = []
        self.__objMap[className].append(funName + "(" + funArgs + ")")

    def __processSimpleFunDef(self, line):
        r1 = re.findall(r"\s*function\s+([\w.]+)\((.*)\)", line)
        res = r1[0]
        funName = res[0]
        funArgs = res[1]
        self.__objMap[''].append(funName + "(" + funArgs + ")")

    def __replaceModuleClass(self):
        if self.__moduleObject is None:
            return
        newObjs = {}
        for k in self.__objMap:
            if k.find(self.__moduleObject) == 0:
                postfix = k[len(self.__moduleObject)+1:]
                # _M.ClassName -> filename.ClassName
                luaPath = self.__currentPath[0:-4].replace('/', '.')
                if luaPath not in newObjs:
                    newObjs[luaPath] = {}
                newObjs[luaPath][postfix] = self.__objMap[k]
        self.__objMap.update(newObjs)

    @staticmethod
    def __parseVarDef(line):
        r1 = re.findall(r"\s*(private|public)?\s+va[rl]\s+(\w+)", line)
        if len(r1) == 0:
            return None, None
        varName = r1[0][-1]
        varType = LuaParser.__getVarType(line)
        return varName, varType

    @staticmethod
    def __findObjMapRecursive(varPath, objMap):
        if len(varPath) == 0:
            return []
        parts = varPath.split('.')
        if parts[0] not in objMap:
            return []
        objMap = objMap[parts[0]]
        if len(parts) == 1:
            return objMap
        varPath = ".".join(parts[1:])
        return LuaParser.__findObjMapRecursive(varPath, objMap)

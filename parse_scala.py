import vim
import re
import sys


def completeMe(currentLine):
    r1 = re.findall(r"\s*(.*)\.(.*)\s*", currentLine)
    if len(r1) == 0:
        return []
    varName = r1[0][0]
    funPref = r1[0][1]
    if varName in objMap:
        return objMap[varName]
    className = findVarDef(varName)
    if className is None:
        return []
    return getFunctionsStartingWith(className, funPref)


def getFunctionsStartingWith(className, funPref):
    funcs = objMap[className]
    if len(funPref) == 0:
        return funcs
    matchingFuncs = []
    for name in objMap[className]:
        if prefixMatches(funPref, name):
            matchingFuncs.append(name)
    return matchingFuncs


def prefixMatches(pref, word):
    return word.find(pref) == 0


def findVarDef(varName):
    currentRange = vim.current.range
    for i in range(currentRange.start-1, -1, -1):
        line = vim.current.buffer[i]
        if isVarDef(varName, line):
            varDef = getVarType(varName, line)
            if (varDef is not None) and (varDef in objMap):
                return varDef
    return None


def isVarDef(varName, line):
    r1 = re.findall(r"\s*va[rl]\s+(\w+)(\s*:\s*\w+)?\s*=(.*)", line)
    # r1 = re.findall(r"\s*va[rl]\s+(\w+)\s*", line)
    return len(r1) > 0


def getVarType(varName, line):
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


def isClassDef(line):
    return re.match(r"\s*(class|object)\s+(\w+)", line)


def getClassName(line):
    match = re.findall(r"\s*class\s+(\w+)", line)
    if len(match) == 0:
        match = re.findall(r"\s*object\s+(\w+)", line)
    return match[0]


def parseArgDecl(argStr):
    if argStr.find(':') == -1:
        return argStr, ''
    r1 = re.findall(r"\s*(\w+)\s*:\s*(\w+)", argStr)
    return r1[0][0], r1[0][1]


def parseClassArguments(className, line):
    r1 = re.findall(r"\s*class\s+(\w+)(.*)", line)
    argsStr = r1[0][1]
    for arg in argsStr.split(','):
        argName, argType = parseArgDecl(arg)
        objMap[className].add(argName)


def isFunDef(line):
    return re.match(r"\s*(private|public)?\s*def \w+\s*\(.*\)", line)


def parseFunDecl(line):
    r1 = re.findall(r"\s*(private|public)*\s*def (\w+\s*\(.*\))",
                    line)
    return r1[0][1]


def parseClasses(lines):
    currentClass = ''
    objMap[''] = set()
    i = 0
    while i < len(lines):
        line = lines[i]
        if isClassDef(line):
            currentClass = getClassName(line)
            if currentClass not in objMap:
                objMap[currentClass] = set()
            if line.find('(') != -1:
                while line.find(')') == -1:
                    if i+1 < len(lines):
                        break
                    line += lines[i+1]
                    i += 1
                parseClassArguments(currentClass, line)
        elif isFunDef(line):
            if line.find('(') != -1:
                while line.find(')') == -1:
                    if i+1 < len(lines):
                        break
                    line += lines[i+1]
                    i += 1
            funId = parseFunDecl(line)
            objMap[currentClass].add(funId)
        i += 1


try:
    objMap
except NameError:
    objMap = {}
    parseClasses(vim.current.buffer)

if sys.argv[0] == 'parse':
    parseClasses(vim.current.buffer)
    print(objMap)
else:
    currentLine = vim.eval('s:currentLine')
    # currentWord = vim.eval('s:wordUnderCursor')
    functions = completeMe(currentLine)
    print(functions)

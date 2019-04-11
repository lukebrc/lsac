import vim
import re
import sys


def getClass(word):
    for line in vim.current.buffer:
        r1 = re.findall(r"%s\s*=\s*([a-zA-Z_]+)" % (currentWord), line)
        if len(r1) > 0:
            return r1[0]
    return None


def complete(word):
    className = getClass(word)
    if className is None:
        return []
    return objMap[className]


def isClassDef(line):
    return re.match(r"\s*(class|object)\s+([a-zA-Z0-9_]+)", line)


def getClassName(line):
    match = re.findall(r"\s*class\s+([a-zA-Z0-9_]+)", line)
    if len(match) == 0:
        match = re.findall(r"\s*object\s+([a-zA-Z0-9_]+)", line)
    return match[0]


def parseArgDecl(argStr):
    if argStr.find(':') == -1:
        return argStr, ''
    r1 = re.findall(r"\s*([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_]+)", argStr)
    return r1[0][0], r1[0][1]


def parseClassArguments(className, line):
    r1 = re.findall(r"\s*class\s+([a-zA-Z0-9_]+)(.*)", line)
    argsStr = r1[0][1]
    for arg in argsStr.split(','):
        argName, argType = parseArgDecl(arg)
        objMap[className].append(argName)


def isFunDef(line):
    return re.match(r"\s*(private|public)?\s*def [a-zA-Z0-9_]+\s*\(.*\)", line)


def parseFunDecl(line):
    r1 = re.findall(r"\s*(private|public)*\s*def ([a-zA-Z0-9_]+\s*\(.*\))",
                    line)
    return r1[0][1]


def parseClasses(lines):
    currentClass = ''
    objMap[''] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if isClassDef(line):
            currentClass = getClassName(line)
            if currentClass not in objMap:
                objMap[currentClass] = []
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
            objMap[currentClass].append(funId)
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
    currentWord = vim.eval('s:wordUnderCursor')
    functions = complete(currentWord)
    print(functions)

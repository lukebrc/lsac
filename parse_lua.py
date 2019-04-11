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


def parseClasses(lines):
    currentClass = None
    for line in lines:
        r1 = re.findall(r"\s*function ([a-z0-9A-Z_.:]+)\(([a-z0-9A-Z_, ]*)\)", line)
        if len(r1) > 0:
            funPath = r1[0][0]
            funArgs = r1[0][1]
            r2 = re.findall(r"([A-Za-z_.]+)[.:]([a-zA-Z_]+)", funPath)
            if len(r2) == 0:
                continue
            r2 = r2[0]
            currentClass = r2[0]
            funName = r2[-1]
            if currentClass not in objMap:
                objMap[currentClass] = []
            objMap[currentClass].append(funName + "(" + funArgs + ")")


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

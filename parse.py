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
        r1 = re.findall(r"\s*class\s+([a-zA-Z_]+)", line)
        if len(r1) > 0:
            currentClass = r1[0]
            objMap[currentClass] = []
        elif currentClass is not None:
            r1 = re.findall(r"def\s+([a-zA-Z_]+)", line)
            if len(r1) > 0:
                objMap[currentClass].append(r1[0])


try:
    objMap
except NameError:
    objMap = {}
    parseClasses(vim.current.buffer)

if sys.argv[0] == 'parse':
    parseClasses(vim.current.buffer)
else:
    currentWord = vim.eval('s:wordUnderCursor')
    functions = complete(currentWord)
    print(functions)

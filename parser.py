import sys
import os

import scalaparser
import luaparser


def printFunctions(functions):
    for f in functions:
        print(f)


def startScala():
    global scalaParser
    try:
        scalaParser
    except NameError:
        scalaParser = scalaparser.ScalaParser()
    return scalaParser


def startLua():
    global luaParser
    try:
        luaParser
    except NameError:
        luaParser = luaparser.LuaParser()
    return luaParser


def parse(fileType, operation, currentFile, currentPos):
    parser = None
    lines = open(currentFile, 'r').readlines()
    if fileType == 'scala':
        parser = startScala()
    elif fileType == 'lua':
        parser = startLua()
    else:
        raise 'Unknown filetype %s' % fileType

    if operation == 'parse':
        objMap = parser.parseClasses(lines)
        print(objMap)
    elif operation == 'complete':
        parser.parseClasses(currentFile)
        # currentWord = vim.eval('s:wordUnderCursor')
        functions = parser.completeMe(lines[currentPos[0]], currentPos[1])
        printFunctions(functions)
    else:
        print('Unknown operation: ' + operation)


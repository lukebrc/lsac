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


def parseFile(fileName, fileType, currentPos):
    parser = None
    if fileType == 'scala':
        parser = startScala()
    elif fileType == 'lua':
        parser = startLua()
    else:
        raise 'Unknown filetype %s' % fileType

    parser.parseClasses(fileName)
    print(parser.getAllObjects())

def complete(fileName, currentPos):
    raise RuntimeError('Not implemented')
    #parser.parseClasses(currentFile)
    #functions = parser.completeMe(lines[currentPos[0]], currentPos[1])
    #printFunctions(functions)



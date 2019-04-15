import vim
import sys
import os

pluginPath = vim.eval('s:pyPluginPath')
pluginPath = os.path.realpath(pluginPath)
if pluginPath not in sys.path:
    sys.path.append(pluginPath)

import scalaparser
import luaparser


def printFunctions(functions):
    for f in functions:
        print(f)


def startScala():
    try:
        scalaParser
    except NameError:
        scalaParser = scalaparser.ScalaParser()
    return scalaParser


def startLua():
    try:
        luaParser
    except NameError:
        luaParser = luaparser.LuaParser()
    return luaParser


def main(argv):
    parser = None
    if argv[0] == 'scala':
        parser = startScala()
    elif argv[0] == 'lua':
        parser = startLua()
    else:
        raise 'Unknown filetype'

    currentPath = vim.eval('s:currentPath')
    if sys.argv[1] == 'parse':
        objMap = parser.parseClasses(vim.current.buffer,
                                     vim.current.range,
                                     currentPath)
        print(objMap)
    elif sys.argv[1] == 'complete':
        # parser.parseClasses(vim.current.buffer,
        #                    vim.current.range)
        currentLine = vim.eval('s:currentLine')
        # currentWord = vim.eval('s:wordUnderCursor')
        functions = parser.completeMe(currentLine, currentPath)
        printFunctions(functions)
    else:
        print('Unknown argument: ' + sys.argv[0])


if __name__ == "__main__":
    main(sys.argv)

import vim
import sys
import scalaparser


def printFunctions(functions):
    for f in functions:
        print(f)


def startScala():
    try:
        scalaParser
    except NameError:
        scalaParser = ScalaParser()
    return scalaParser


def main(argv):
    parser = None
    if argv[0] == 'scala':
        parser = startScala()
    else:
        raise 'Unknown filetype'

    if sys.argv[0] == 'parse':
        objMap = parser.parseClasses(vim.current.buffer,
                                     vim.current.range)
        print(objMap)
    elif sys.argv[0] == 'complete':
        # parser.parseClasses(vim.current.buffer,
        #                    vim.current.range)
        currentLine = vim.eval('s:currentLine')
        # currentWord = vim.eval('s:wordUnderCursor')
        functions = parser.completeMe(currentLine)
        printFunctions(functions)
    else:
        print('Unknown argument: ' + sys.argv[0])


if __name__ == "__main__":
    main(sys.argv)

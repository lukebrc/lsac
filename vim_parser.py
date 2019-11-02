import vim
import sys
import os
import parser

pluginPath = vim.eval('s:pyPluginPath')
pluginPath = os.path.realpath(pluginPath)
if pluginPath not in sys.path:
    sys.path.append(pluginPath)


def main(argv):
    parser.parse(argv[0], argv[1], vim.current.buffer, currentPath)


if __name__ == "__main__":
    main(sys.argv)

import sys
import os
import parser

plugin_path = '/home/lukasz/prog/lsac'
plugin_path = os.path.realpath(plugin_path)
if plugin_path not in sys.path:
    sys.path.append(plugin_path)



def main(argv):
    with open(argv[2], 'r') as file:
        buffer = file.read()
    parser.parse(argv[0], argv[1], buffer, currentPath)


if __name__ == "__main__":
    main(sys.argv)

#!/usr/bin/env python3
import sys
import os
from parsers import parser
import argparse

plugin_path = '/home/lukasz/prog/lsac'
plugin_path = os.path.realpath(plugin_path)
if plugin_path not in sys.path:
    sys.path.append(plugin_path)


def parse_arguments(argv):
    arg_parser = argparse.ArgumentParser(description='File syntax parser')

    arg_parser.add_argument('--operation', help='Operation to perform (parse, complete)')
    arg_parser.add_argument('--root_dir', metavar='r', help='Base directory of sources')
    arg_parser.add_argument('--type', help='Type of source (scala|python)')
    arg_parser.add_argument('--file', help='File to be processed')
    arg_parser.add_argument('--line', help='Line number')
    arg_parser.add_argument('--column', help='Column number')
    return arg_parser.parse_args()


def main(argv):
    parsed_args = parse_arguments(argv)

    current_pos = [parsed_args.line, parsed_args.column]

    if parsed_args.operation == 'parse':
        parser.parseFile(parsed_args.file,
                         parsed_args.type,
                         current_pos)
    else:
        raise RuntimeError("Unknown operation: {}".format(parsed_args.operation))


if __name__ == "__main__":
    main(sys.argv)


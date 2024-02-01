import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.

sys.path.append(parent)

# now we can import the module in the parent
# directory.

import parser.cminus_parser as cminus_parser

if __name__ == '__main__':
  cminus_parser.compile_program(sys.argv[1])
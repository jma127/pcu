import re

import globals
import settings

# Formatting Rules

rules = [
    lambda str: re.sub('\$INFILE', settings.inputfile, str),
    lambda str: re.sub('\$OUTFILE', settings.outputfile, str),
    lambda str: re.sub('\$SRCFILE', globals.getsrc(), str),
    lambda str: re.sub('\$PROB', globals.getprob(), str),
    lambda str: re.sub('\$EXT', globals.getext(), str),
    lambda str: re.sub('\$USER', settings.username, str)
]

# String Formatter

def convert (str):
    for rule in rules:
        str = rule(str)
    return str

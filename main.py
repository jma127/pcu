#!/usr/bin/env python

import os

import helper
import parse
import globals
import pattern
import settings

# PCU main function

def main ():
    # Read command line options

    globals.probsettings = parse.parseopts()

    # Initialize problem

    helper.makedir(globals.sandboxdir)
    if globals.getprob() is not None:
        globals.probdir = os.path.join(globals.tmpdir, 'probs', globals.getprob())
        globals.probsettingsfile = os.path.join(globals.probdir, 'probsettings.dat')
        helper.makedir(globals.probdir)

    # Merge dictionary with command line options

    if globals.getprob() is not None:
        opts = helper.readdict(globals.probsettingsfile) # Previous settings
        for key in opts:
            if key not in globals.probsettings or globals.probsettings[key] is None:
                globals.probsettings[key] = opts[key]

    # Assert that basic values are present in settings

    if globals.getext() is None:
        globals.probsettings['langext'] = settings.defaultlangext

    if globals.getmode() is None:
        globals.probsettings['mode'] = settings.defaultmode

    # Execute command

    print settings.bigdivider
    globals.commands[globals.probsettings['command']]()

    # Write new settings dict to file

    if globals.getprob() is not None:
        helper.writedict(globals.probsettingsfile, globals.probsettings)

    # Clear sandbox directory

    helper.deldir(globals.sandboxdir)

    print settings.bigdivider

if __name__ == '__main__':
    main()

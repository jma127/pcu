import os

import globals
import helper
import pattern
import settings

# Compile Engine

def compile ():
    print 'Compiling ' + globals.getsrc()
    lang = settings.langexts[globals.getext()]
    print 'Language detected: ' + lang
    if not helper.copy(os.path.join(globals.working, globals.getsrc()), globals.sandboxdir):
        print 'Source file not found in working directory'
        return False
    compcommand = settings.compcommands[lang]
    if compcommand is None:
        print 'No compilation necessary'
        return True
    else:
        compcommand = pattern.convert(compcommand)
        print 'Compilation command: ' + compcommand
        compresult = helper.runproc(compcommand, globals.sandboxdir, timelim=settings.compilelimit)
        if compresult[0] is None: # Time limit exceeded
            print 'Compile time limit exceeded ({:.2f} seconds)'.format(settings.compilelimit)
            return False
        message = compresult[3].strip()
        if compresult[0] != 0: # Runtime error
            helper.printdesc(message, 'Compile errors', settings.smalldivider, False)
            return False
        print 'Successful compile ({:.2f} seconds)'.format(compresult[1])
        if len(message) > 0: # Check for warnings
            helper.printdesc(message, 'Compile warnings', settings.smalldivider, False)
        return True

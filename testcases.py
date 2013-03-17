import os
import sys

import globals
import helper
import parse
import settings

# Test Case Management Engine

exttotype = {
    '.in': 'input',
    '.ans': 'answer',
    '.out': 'output',
    '.stdout': 'stdout',
    '.stderr': 'stderr'
}

# Read input and set test case data

def setfile (ext):
    file = globals.probsettings['filename']
    type = exttotype[ext]
    testid = globals.gettestid()
    print 'Setting test case {} {} for problem {}'.format(testid, type, globals.getprob())
    input = ''
    if file is None:
        print 'Enter {} below (Ctrl-{} when finished)'.format(type, 'Z' if helper.iswindows() else 'D')
        print settings.smalldivider
        input = sys.stdin.read()
        print settings.smalldivider
    else:
        print 'Retrieving from ' + file.name
        input = file.read()
    helper.write(os.path.join(globals.probdir, testid + ext), input)
    print 'Set {} successfully'.format(exttotype[ext])
    return True

# Get test case data

def getfile (ext):
    file = parse.parseopts()['filename']
    type = exttotype[ext]
    testid = globals.gettestid()
    print 'Getting test case {} {} for problem {}'.format(testid, type, globals.getprob())
    output = helper.read(os.path.join(globals.probdir, testid + ext))
    if output is None:
        print 'Did not find {} file'.format(type)
        return False
    if file is None:
        print 'File found: {} below'.format(type)
        print settings.smalldivider
        print output + ('' if settings.eof is None else settings.eof)
    else:
        try:
            file.write(output)
            file.close()
            print 'Wrote {} to {}'.format(type, file.name)
        except IOError:
            print 'Unable to write to ' + file.name
            return False
    return True

def setin ():
    return setfile('.in')

def setans ():
    return setfile('.ans')

def getin ():
    return getfile('.in')

def getans ():
    return getfile('.ans')

def getout ():
    return getfile('.out')

def getstdout ():
    return getfile('.stdout')

def getstderr ():
    return getfile('.stderr')

# Delete problem test cases

def delcases ():
    print 'Deleting all test cases for problem ' + globals.getprob()
    for file in os.listdir(globals.probdir):
        if not file.endswith('.dat'):
            os.remove(os.path.join(globals.probdir, file))
            print 'Deleted ' + file
    print 'Problem {}: all test cases deleted'.format(globals.getprob())

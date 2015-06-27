import os

import compile
import log
import make
import run
import testcases
import testgen

# Global Variables

working = os.path.abspath(os.getcwd()) # Current working directory
path = os.path.dirname(os.path.abspath(__file__)) # Path directory
tmpdir = os.path.join(path, 'tmp') # Current temporary directory
logfile = os.path.join(tmpdir, 'log.txt')
sandboxdir = os.path.join(tmpdir, 'sandbox') # Sandbox directory
templatedir = os.path.join(path, 'templates') # Template directory
probdir = None # Problem directory
probsettingsfile = None # File of problem settings dictionary
probsettings = None # Problem settings dictionary

# Command Functions

commands = {
    'make': make.make,
    'comp': compile.compile,
    'setin': testcases.setin,
    'setans': testcases.setans,
    'testgen': testgen.testgen,
    'getin': testcases.getin,
    'getans': testcases.getans,
    'getout': testcases.getout,
    'getstdout': testcases.getstdout,
    'getstderr': testcases.getstderr,
    'delcases': testcases.delcases,
    'run': run.run,
    'logstart': log.logstart,
    'logmsg': log.logmsg,
    'logretr': log.logretr
}

# Reusable Options

reusable = ['langext', 'mode']

# Problem Settings Retrieval

def getsetting (setting):
    if setting in probsettings:
        return probsettings[setting]
    return None

def getprob ():
    return getsetting('problem')

def getext ():
    return getsetting('langext')

def getsrc ():
    return getprob() + '.' + getext()

def getmode ():
    return getsetting('mode')

def getnumcases ():
    return getsetting('numcases')
    
def gettestid ():
    return getsetting('testid')

def gettestfile ():
    return getsetting('filename')
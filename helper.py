import cStringIO
import os
import pickle
import shlex
import shutil
import subprocess
import sys
import time

import globals
import settings

# Windows or not

def iswindows ():
    return sys.platform.startswith('win')

# Safely copy files

def copy (src, dest):
    try:
        shutil.copy(src, dest)
        return True
    except IOError:
        return False

# Safely make a directory

def makedir (dir):
    try:
        os.makedirs(dir)
        return True
    except OSError:
        return False

# Safely delete a directory

def deldir (dir):
    try:
        shutil.rmtree(dir)
        return True
    except OSError:
        return False

# Get the total CPU time of a process

def gettime (pid):
    if iswindows():
        return 0.0
    psoutput = subprocess.check_output(shlex.split('ps -p {:d} -o time='.format(pid))).split(':')
    if len(psoutput) == 0:
        return 0.0
    return float(psoutput[0]) * 60.0 + float(psoutput[1])

# Execute a process with time constraints and custom I/O
# Return value: (exitcode, cputime, stdout, stderr)

def runproc (cmd, workingdir, stdin=None, timelim=10.0, sleepintvl=0.01):
    stdinname = os.path.join(workingdir, 'stdin.tmp')
    stdoutname = os.path.join(workingdir, 'stdout.tmp')
    stderrname = os.path.join(workingdir, 'stderr.tmp')
    write(stdinname, stdin, printempty=True)
    stdinfile = open(stdinname, 'rb', 1)
    stdoutfile = open(stdoutname, 'wb', 1)
    stderrfile = open(stderrname, 'wb', 1)
    print cmd
    proc = subprocess.Popen(shlex.split(cmd), cwd=workingdir, stdin=stdinfile,
                            stdout=stdoutfile, stderr=stderrfile)
    cputime = 0.0
    while True:
        retcode = proc.poll()
        if retcode is not None:
            stdoutfile.close()
            stderrfile.close()
            return (retcode, cputime, read(stdoutname), read(stderrname))
        newtime = gettime(proc.pid)
        if newtime > cputime:
            cputime = newtime
        if cputime > timelim:
            proc.kill()
            time.sleep(sleepintvl)
            stdoutfile.close()
            stderrfile.close()
            return (None, None, read(stdoutname), read(stderrname))
        time.sleep(sleepintvl)

# Print test case input/output

def printdesc (str, desc, div, printeof=True):
    if str is None or len(str) == 0:
        return
    print ('>>> ' + desc + ' ' + div)[:len(div)]
    if settings.eof is None or not printeof:
        print str
    else:
        print str + settings.eof

# Read string from file

def read (filename):
    try:
        file = open(filename, 'rb')
        str = file.read()
        file.close()
        return str
    except IOError:
        return None

# Write string to file

def write (filename, str, printempty=False):
    try:
        if str is not None and len(str) > 0:
            file = open(filename, 'wb')
            file.write(str)
            file.close()
        elif printempty:
            file = open(filename, 'wb')
            file.write('')
            file.close()
    except IOError:
        pass

# Read dict from file

def readdict (file):
    data = read(file)
    if data is None:
        return {}
    return pickle.loads(data)

# Write dict to file

def writedict (file, dict):
    newdict = {}
    for key in dict:
        if key in globals.reusable:
            newdict[key] = dict[key]
    data = pickle.dumps(newdict)
    write(file, data)

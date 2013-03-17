import os
import random

import globals
import helper

# Test Generator Framework

def testgen ():
    numcases = globals.getnumcases()
    execorig = globals.getsetting('executable')
    execloc = os.path.join(globals.sandboxdir, execorig.name)
    execfile = open(execloc, 'wb')
    execfile.write(execorig.read())
    execfile.close()
    os.chmod(execloc, 0755)
    print 'Automatically generating {} test cases for problem {} with {}'.format(numcases, globals.getprob(), execorig.name)
    curtest = 0
    for i in range(numcases):
        while True:
            inloc = os.path.join(globals.probdir, 'pcugen{:03d}.in'.format(curtest))
            ansloc = os.path.join(globals.probdir, 'pcugen{:03d}.ans'.format(curtest))
            if not os.path.exists(inloc):
                break
            curtest += 1
        print 'Generating case {:03d}'.format(curtest)
        execresult = helper.runproc('./{} {} {}'.format(execorig.name, curtest, random.randint(0, 2147483647)), globals.sandboxdir, timelim=10.0)
        if execresult[0] != 0:
            print 'Generator executable error'
            break
        infile = open(inloc, 'wb')
        ansfile = open(ansloc, 'wb')
        infile.write(execresult[2])
        ansfile.write(execresult[3])
        infile.close()
        ansfile.close()
        curtest += 1
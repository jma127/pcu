import os
import sys

import datetime
import globals
import helper
import parse
import settings

formatstr = '%d-%m-%Y %H:%M:%S'

def logstart():
    time = datetime.datetime.now().strftime(formatstr)
    helper.write(globals.logfile, 'PCU Contest Log\nstarted ' + time + '\n'
                 + settings.smalldivider + '\n')
    print 'Created contest log with start time ' + time
    return True

def addmsg(msg, system=True):
    logstr = helper.read(globals.logfile)
    if logstr is None:
        return False
    lines = logstr.split('\n')
    time = (datetime.datetime.now() -
            datetime.datetime.strptime(lines[1].split('started ')[1], formatstr))
    timestr = '{:d}:{:02d}'.format(time.seconds / 3600, (time.seconds % 3600) / 60)
    logstr += '> {:>5} - {:>4}:  {}'.format(timestr, 'pcu' if system else 'user', msg)
    if not msg.endswith('\n'):
        logstr += '\n'
    helper.write(globals.logfile, logstr)
    return True

def logmsg():
    sys.stdout.write('Enter message (one line): ')
    input = sys.stdin.readline()
    if addmsg(input, system=False):
        print 'Message entered in contest log'
        return True
    return False

def logretr():
    log = helper.read(globals.logfile)
    if log is None:
        print 'Contest log not found'
        return False
    sys.stdout.write(log)
    return True

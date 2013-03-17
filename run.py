import os

import collections
import globals
import helper
import pattern
import settings

# Program Execution Engine

def run ():
    if not globals.commands['comp']():
        return False
    print settings.meddivider
    stdio = globals.getmode() == 'stdio'
    print 'Executing problem {} in {} I/O mode'.format(globals.getprob(), globals.getmode())
    files = os.listdir(globals.probdir)
    cases = []
    for file in files:
        if file.endswith('.in'):
            cases.append(file[:-3])
    print '{} test inputs found'.format(len(cases))
    sandboxin = os.path.join(globals.sandboxdir, pattern.convert(settings.inputfile))
    sandboxout = os.path.join(globals.sandboxdir, pattern.convert(settings.outputfile))
    execcommand = pattern.convert(settings.execcommands[settings.langexts[globals.getext()]])
    langlim = settings.timeconstraints[settings.langexts[globals.getext()]]
    outcomes = collections.OrderedDict([
        ('Correct', 0),
        ('Runtime Error', 0),
        ('Time Limit Exceeded', 0),
        ('Presentation Error', 0),
        ('Wrong Answer', 0),
        ('No Output Produced', 0),
        ('No Answer File', 0)
    ])
    print 'Time limit per input: {:.2f} seconds'.format(langlim)
    for case in cases:
        print settings.meddivider
        print 'Test input ' + case
        helper.copy(os.path.join(globals.probdir, case + '.in'), sandboxin)
        input = helper.read(sandboxin)
        execresult = helper.runproc(execcommand, globals.sandboxdir, stdin=(input if stdio else None), timelim=langlim)
        output = execresult[2] if stdio else helper.read(sandboxout)
        ans = helper.read(os.path.join(globals.probdir, case + '.ans'))
        wronganswer = False
        if execresult[0] is None: # Time limit exceeded
            print 'Execution time limit exceeded'
            outcomes['Time Limit Exceeded'] += 1
        else:
            print 'Execution time: {:.2f} seconds'.format(execresult[1])
            if execresult[0] != 0:
                print 'Runtime error: exit code ' + repr(execresult[0])
                outcomes['Runtime Error'] += 1
            elif output is None or len(output) == 0:
                print 'Program did not produce output'
                outcomes['No Output Produced'] += 1
            elif ans is None:
                print 'No answer file provided'
                outcomes['No Answer File'] += 1
            elif ans == output or \
                 (''.join(ans.split()) == ''.join(output.split())
                  and settings.acceptformatting):
                print 'Correct'
                outcomes['Correct'] += 1
            elif ''.join(ans.split()) == ''.join(output.split()):
                print 'Presentation Error (extra/missing whitespace)'
                outcomes['Presentation Error'] += 1
                wronganswer = True
            else:
                print 'Wrong Answer'
                outcomes['Wrong Answer'] += 1
                wronganswer = True
        if settings.printinput:
            helper.printdesc(input, 'Input', settings.smalldivider)
        if settings.printoutput:
            helper.printdesc(output, 'Output', settings.smalldivider)
        if wronganswer and settings.printexpected:
            helper.printdesc(ans, 'Expected Output', settings.smalldivider)
        if settings.printstdout and not stdio:
            helper.printdesc(execresult[2], 'Stdout', settings.smalldivider)
        if settings.printstderr:
            helper.printdesc(execresult[3], 'Stderr', settings.smalldivider)
        helper.write(os.path.join(globals.probdir, case + '.out'), output)
        if not stdio:
            helper.write(os.path.join(globals.probdir, case + '.stdout'), execresult[2])
        helper.write(os.path.join(globals.probdir, case + '.stderr'), execresult[3])
    if settings.printsummary:
        print settings.meddivider
        print 'Results Summary'
        for outcome in outcomes:
            print '{:2d} | {:<20}'.format(outcomes[outcome], outcome)
        print 'Total Score: {:.1f}'.format((100.0 * outcomes['Correct']) / max(1, len(cases))); 
    return True

# User Profile

import getpass

username = getpass.getuser() # Your name
defaultlangext = 'cpp' # Preferred language extension
defaultmode = 'stdio' # Preferred I/O mode (stdio or file)
                      # Note that USACO uses file I/O, while other competitions
                      # use stdio
printinput = True # Print test inputs
printoutput = True # Print program outputs
printstdout = True # If stdout output found, print it (file mode only)
printstderr = True # If stderr output found, print it
printexpected = True # If wrong answer found, print expected output
printsummary = True # If true, will print summary of all test results
acceptformatting = False # If true, all "Presentation Error" will be "Correct"
logactions = True # If true, all pcu actions will be recorded in contest logs

# Language Extensions (mapped to language names)

langexts = {
    'c': 'C',
    'cc': 'C++',
    'cpp': 'C++',
    'java': 'Java',
    'py': 'Python',
    'sh': 'Shell'
}

# Time Constraints

compilelimit = 30.0

timeconstraints = {
    'C': 2.0,
    'C++': 2.0,
    'Java': 4.0,
    'Python': 4.0,
    'Shell': 4.0
}

# Compile Commands

compcommands = {
    'C': 'gcc -Wall -Wextra -O2 -o $PROB.exe $SRCFILE',
    'C++': 'g++ -Wall -Wextra -O2 -o $PROB.exe $SRCFILE',
    'Java': 'javac $SRCFILE',
    'Python': 'python -m py_compile $SRCFILE',
    'Shell': None
}

# Execution Commands

execcommands = {
    'C': './$PROB.exe',
    'C++': './$PROB.exe',
    'Java': 'java $PROB',
    'Python': 'python $PROB.pyc',
    'Shell': '$SRCFILE'
}

# File Specifications

inputfile = '$PROB.in' # Input file for file problems
outputfile = '$PROB.out' # Output file for file problems

# Formatting

bigdivider   = '#' * 80
meddivider   = '=' * 64
smalldivider = '-' * 48
eof = '<EOF>' # EOF symbol for console output

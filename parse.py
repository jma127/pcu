import argparse

import globals
import settings

# Option Parser

def parseopts ():
    parser = argparse.ArgumentParser(prog='pcu', description='pcu: comprehensive suite for competitive programming', epilog='Copyright 2013, Jerry Ma. https://github.com/jma127/pcu')
    subparsers = parser.add_subparsers(title='command', metavar='command', dest='command', description='command to be executed')

    make = subparsers.add_parser('make', help='generate problem source file')

    comp = subparsers.add_parser('comp', help='compile problem source file')

    setin = subparsers.add_parser('setin', help='set test case input')
    setin.add_argument('-f', '--filename', help='file to read test case data (default stdin)',
                       type=argparse.FileType('rb'))

    setans = subparsers.add_parser('setans', help='set test case answer')
    setans.add_argument('-f', '--filename', help='file to read test case data (default stdin)',
                        type=argparse.FileType('rb'))

    testgen = subparsers.add_parser('testgen', help='generate tests from program')
    testgen.add_argument('-n', '--numcases', help='number of tests to generate', type=int, default=10)

    getin = subparsers.add_parser('getin', help='get test case input')
    getin.add_argument('-f', '--filename', help='file to write test case data (default stdout)',
                       type=argparse.FileType('wb'))

    getans = subparsers.add_parser('getans', help='get test case answer')
    getans.add_argument('-f', '--filename', help='file to write test case data (default stdout)',
                        type=argparse.FileType('wb'))

    getout = subparsers.add_parser('getout', help='get test case input')
    getout.add_argument('-f', '--filename', help='file to write test case data (default stdout)',
                       type=argparse.FileType('wb'))

    getstdout = subparsers.add_parser('getstdout', help='get test case answer')
    getstdout.add_argument('-f', '--filename', help='file to write test case data (default stdout)',
                        type=argparse.FileType('wb'))

    getstderr = subparsers.add_parser('getstderr', help='get test case answer')
    getstderr.add_argument('-f', '--filename', help='file to write test case data (default stdout)',
                      type=argparse.FileType('wb'))

    delcases = subparsers.add_parser('delcases', help='delete all test cases')

    run = subparsers.add_parser('run', help='run problem against test cases')

    logstart = subparsers.add_parser('logstart', help='start a contest log and deletes previous log (if exists)')

    logmsg = subparsers.add_parser('logmsg', help='add a custom message to the log')

    logretr = subparsers.add_parser('logretr', help='retrieve contest log')
    
    problist = [make, comp, setin, setans, testgen, getin, getans, getout, getstdout, getstderr, delcases, run]
    testlist = [setin, setans, getin, getans, getout, getstdout, getstderr]
    modelist = [make, run]
    langextlist = [make, comp, run]

    for arg in problist:
        arg.add_argument('problem', help='problem name')

    for arg in testlist:
        arg.add_argument('testid', help='desired test case id')

    for arg in modelist:
        arg.add_argument('-m', '--mode', help='I/O mode', choices=['stdio', 'file'])

    for arg in langextlist:
        arg.add_argument('-l', '--langext', help='language extension (see settings.py)', choices=settings.langexts)
    
    testgen.add_argument('executable', help='executable (.sh, .py, .exe, etc.) that generates test data', type=argparse.FileType('rb'))

    return vars(parser.parse_args())

import argparse
import pathlib
import string
import sys

from . import color_utils
from . import config


Args = argparse.Namespace


def _get_parser() -> argparse.ArgumentParser:
    settings = config.get_settings()

    parser = argparse.ArgumentParser(
        prog='pcu',
        description='pcu: comprehensive suite for competitive programming',
        epilog='Copyright 2017, Jerry Ma. https://github.com/jma127/pcu')

    subparsers = parser.add_subparsers(
        title='command',
        metavar='command',
        dest='command',
        description='command to be executed')

    make = subparsers.add_parser('make',
        help='generate problem source file')
    make.add_argument(
        '-S', '--nosrc',
        help="don't create a source file for this problem",
        dest='create_source',
        action='store_false')
    make.add_argument(
        '-C', '--noclean',
        help="don't clean problem data (e.g. config, testcases) before making",
        dest='clean',
        action='store_false')

    comp = subparsers.add_parser('comp',
        help='compile problem source file')
    comp.add_argument(
        '-l', '--local',
        help='Put compiler output files in local directory '
             '(WORKING_DIR/PROBLEM_NAME_compiled/)',
        action='store_true')

    run = subparsers.add_parser('run', help='run problem against test cases')

    getin = subparsers.add_parser('getin',
        help='get test case input')
    getans = subparsers.add_parser('getans',
        help='get test case correct answer')
    getout = subparsers.add_parser('getout',
        help='get test case output')
    geterr = subparsers.add_parser('geterr',
        help='get test case stderr')

    setin = subparsers.add_parser('setin',
        help='set test case input')
    setans = subparsers.add_parser('setans',
        help='set test case correct answer')

    delcases = subparsers.add_parser('delcases',
        help='delete all test cases for a problem')
    delprob = subparsers.add_parser('delprob',
        help='delete all pcu data for a problem')
    delprobs = subparsers.add_parser('delprobs',
        help='delete all pcu data for all problems')

    chgenv = subparsers.add_parser('chgenv',
        help='change environment')

    testgen = subparsers.add_parser('testgen',
        help='generate tests from program')
    testgen.add_argument(
        '-n', '--numcases',
        help='number of tests to generate',
        type=int,
        default=10)

    problem_commands = [
        make,
        comp,
        run,
        getin,
        getans,
        getout,
        geterr,
        setin,
        setans,
        delcases,
        delprob,
        testgen,
    ]
    test_id_commands = [
        getans,
        getin,
        getout,
        geterr,
        setin,
        setans,
    ]
    test_ids_commands = [
        run,
        delcases,
    ]
    env_commands = [
        (chgenv, True),
        (make, False),
    ]

    for command in problem_commands:
        command.add_argument('problem',
            help='problem name')

    for command in test_id_commands:
        command.add_argument('test_id',
            help='desired test case id (e.g. sample1)')

    for command in test_ids_commands:
        command.add_argument(
            'test_ids',
            help='desired test case ids (e.g. sample1). Leave blank to '
                 'run all cases.',
            nargs='*')

    for command, required in env_commands:
        names = ['env'] if required else ['-e', '--env']
        command.add_argument(*names,
            help='environment (e.g. cpp, java, py2). See documentation for '
                 'how to add environments or modify environment settings',
            metavar='env',
            choices=settings.get_env_names_and_aliases(),
            default=(None if required else settings.default_env))

    testgen.add_argument(
        'executable',
        help='executable (.sh, .py, .exe, etc.) that generates test data',
        type=argparse.FileType('rb'))

    return parser


def parse() -> Args:
    parser = _get_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        raise SystemExit(1)

    if 'problem' in vars(args):
        allowed_chars = set(string.ascii_letters + string.digits + '_-.')
        if any(c not in allowed_chars for c in args.problem):
            with color_utils.ColorizeStderrError():
                print('ERROR: problem name', args.problem,
                      'must be an identifier',
                      file=sys.stderr)
                print('(preferably stick to numbers, letters, and undescores)',
                      file=sys.stderr)
            raise SystemExit(1)

    return args

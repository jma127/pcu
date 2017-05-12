import pathlib
import shutil
import sys
import tempfile
from typing import Callable, Dict

from . import arg_parser
from . import color_utils
from . import compiler
from . import config
from . import defaults
from . import paths
from . import problem
from . import runner
from . import testgen


CommandFn = Callable[[arg_parser.Args], bool]
_command_registry = {}  # type: Dict[str, CommandFn]
def register_command(fn: CommandFn) -> CommandFn:
    command_name = fn.__name__.strip('_')
    assert command_name not in _command_registry
    _command_registry[command_name] = fn
    return fn


def dispatch(args: arg_parser.Args) -> None:
    command = _command_registry[args.command]
    if not command(args):
        raise SystemExit(4)


@register_command
def _make(args: arg_parser.Args) -> bool:
    settings = config.get_settings()

    with problem.Problem(args.problem,
                         settings.get_env(args.env),
                         args.clean) as prob:
        env = prob.env

        if args.create_source:
            template_file = env.template_file
            template = defaults.default_template(template_file)

            template_user_loc = paths.template_path(template_file)
            if template_user_loc.is_file():
                with open(template_user_loc, 'r') as infile:
                    template = infile.read()

            if template is None:
                with color_utils.ColorizeStderrError():
                    print('ERROR: Template', template_file, 'was not found --',
                          'please add it to', paths.templates_path(),
                          file=sys.stderr)
                    return False

            template = prob.sub_params(template)

            with open(prob.source_file, 'w') as outfile:
                outfile.write(template)

    with color_utils.ColorizeStderrGood():
        print('Created', env.name, 'problem', prob.name,
              'with source file', prob.source_file,
              file=sys.stderr)

    if not args.create_source:
        with color_utils.ColorizeStderrWarning():
            print('(note: no source file was actually created -- you will need to '
                  'write or copy over your own)',
                  file=sys.stderr)

    return True


@register_command
def _comp(args: arg_parser.Args) -> bool:
    settings = config.get_settings()

    with problem.Problem(args.problem) as prob:
        with tempfile.TemporaryDirectory() as temp_dir:
            working_dir = pathlib.Path(temp_dir)

            if args.local:
                working_dir = pathlib.Path.cwd() / (prob.name + '_compiled')
                if working_dir.exists():
                    if working_dir.is_file():
                        working_dir.unlink()
                    else:
                        shutil.rmtree(working_dir)
                working_dir.mkdir()

            return compiler.compile(prob, working_dir)


@register_command
def _run(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        with tempfile.TemporaryDirectory() as temp_dir:
            working_dir = pathlib.Path(temp_dir)

            if not compiler.compile(prob, working_dir):
                return False

            test_ids = args.test_ids or prob.get_test_ids()
            return runner.run_cases(prob, working_dir, test_ids)


@register_command
def _getin(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        path = prob.get_test_input_path(args.test_id)
        if path.is_file():
            with open(path, 'rb') as infile:
                shutil.copyfileobj(infile, sys.stdout.buffer)
            return True
        else:
            with color_utils.ColorizeStderrError():
                print('ERROR: Input file for test case', args.test_id, 'in',
                      'problem', prob.name, 'not found',
                      file=sys.stderr)
            return False


@register_command
def _getans(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        path = prob.get_test_answer_path(args.test_id)
        if path.is_file():
            with open(path, 'rb') as infile:
                shutil.copyfileobj(infile, sys.stdout.buffer)
            return True
        else:
            with color_utils.ColorizeStderrError():
                print('ERROR: Answer file for test case', args.test_id, 'in',
                      'problem', prob.name, 'not found',
                      file=sys.stderr)
            return False


@register_command
def _getout(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        path = prob.get_test_output_path(args.test_id)
        if path.is_file():
            with open(path, 'rb') as infile:
                shutil.copyfileobj(infile, sys.stdout.buffer)
            return True
        else:
            with color_utils.ColorizeStderrError():
                print('ERROR: Output file for test case', args.test_id, 'in',
                      'problem', prob.name, 'not found',
                      file=sys.stderr)
            return False


@register_command
def _geterr(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        path = prob.get_test_error_path(args.test_id)
        if path.is_file():
            with open(path, 'rb') as infile:
                shutil.copyfileobj(infile, sys.stdout.buffer)
            return True
        else:
            with color_utils.ColorizeStderrError():
                print('ERROR: Standard error file for test case', args.test_id,
                      'in problem', prob.name, 'not found',
                      file=sys.stderr)
            return False


@register_command
def _setin(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        path = prob.get_test_input_path(args.test_id)
        with open(path, 'wb') as outfile:
            if sys.stdin.isatty():
                print('Enter the input for test case', args.test_id, 'below,',
                      'terminated by Ctrl-D',
                      file=sys.stderr)
            shutil.copyfileobj(sys.stdin.buffer.raw, outfile)  # type: ignore

    with color_utils.ColorizeStderrGood():
        print('Read input file for test case', args.test_id, 'in',
              'problem', prob.name,
              file=sys.stderr)

    return True


@register_command
def _setans(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        path = prob.get_test_answer_path(args.test_id)
        with open(path, 'wb') as outfile:
            if sys.stdin.isatty():
                print('Enter the answer for test case', args.test_id, 'below,',
                      'terminated by Ctrl-D',
                      file=sys.stderr)
            shutil.copyfileobj(sys.stdin.buffer.raw, outfile)  # type: ignore

    with color_utils.ColorizeStderrGood():
        print('Read answer file for test case', args.test_id, 'in',
              'problem', prob.name,
              file=sys.stderr)

    return True


@register_command
def _delcases(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        prob_test_ids = set(prob.get_test_ids())
        test_ids = sorted(args.test_ids or prob_test_ids)
        for test_id in test_ids:
            if test_id not in prob_test_ids:
                with color_utils.ColorizeStderrError():
                    print('ERROR: Test case', test_id, 'not found for problem',
                          prob.name,
                          file=sys.stderr)
                    return False

        for test_id in test_ids:
            paths = [
                prob.get_test_input_path(test_id),
                prob.get_test_answer_path(test_id),
                prob.get_test_output_path(test_id),
                prob.get_test_error_path(test_id),
            ]
            for path in paths:
                if path.exists():
                    assert path.is_file()
                    path.unlink()

    with color_utils.ColorizeStderrGood():
        print('Deleted', len(test_ids), 'test cases for',
              'problem', prob.name,
              file=sys.stderr)

    return True


@register_command
def _delprob(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem, delete_on_exit=True):
        return True


@register_command
def _delprobs(args: arg_parser.Args) -> bool:
    problems_path = paths.problems_path()
    for problem_path in problems_path.iterdir():
        if not problem_path.is_dir():
            continue
        shutil.rmtree(problem_path)

    return True


@register_command
def _info(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        with color_utils.ColorizeStderrBar1():
            print('=' * 20, 'Info for problem', prob.name, '=' * 20,
                  file=sys.stderr)
        print('Environment:', prob.env.name,
              file=sys.stderr)
        if prob.env_overrides:
            print('Environment overrides:', prob.env_overrides,
                  file=sys.stderr)

        test_ids = prob.get_test_ids()
        print('Test cases ({}):'.format(len(test_ids)), test_ids,
              file=sys.stderr)

    return True


@register_command
def _chgenv(args: arg_parser.Args) -> bool:
    settings = config.get_settings()

    with problem.Problem(args.problem) as prob:
        prob.original_env = settings.get_env(args.env)
        prob.update_env()
        with color_utils.ColorizeStderrGood():
            print('Changed environment for problem', prob.name,
                  'to', prob.env.name,
                  file=sys.stderr)

    return True


@register_command
def _envoverride(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        if args.new_value:
            prob.env_overrides[args.env_setting] = args.new_value
        else:
            prob.env_overrides.pop(args.env_setting, None)
        prob.update_env()

        with color_utils.ColorizeStderrGood():
            print('Added environment override',
                  args.env_setting + '=' + str(args.new_value),
                  'for problem', prob.name,
                  file=sys.stderr)

    return True


@register_command
def _testgen(args: arg_parser.Args) -> bool:
    with problem.Problem(args.problem) as prob:
        return testgen.generate_tests(
            prob, args.executable, args.prefix, args.numcases)

import collections
import difflib
import enum
import inflection
import pathlib
import shutil
import string
import subprocess
import sys
from typing import DefaultDict, Iterable, List, Optional

from . import color_utils
from . import environment
from . import problem


class TestCaseResult(enum.Enum):
    CORRECT = enum.auto()
    NO_ANSWER_FILE_PROVIDED = enum.auto()
    WRONG_ANSWER = enum.auto()
    PRESENTATION_ERROR = enum.auto()
    NO_OUTPUT_FILE_PRODUCED = enum.auto()
    TIME_LIMIT_EXCEEDED = enum.auto()
    RUNTIME_ERROR = enum.auto()

    def get_colorize_colors(self) -> List:
        if self == TestCaseResult.CORRECT:
            return [color_utils.Fore.BLUE]
        elif self == TestCaseResult.NO_ANSWER_FILE_PROVIDED:
            return [color_utils.Fore.YELLOW]
        else:
            return [color_utils.Fore.RED]


def run_cases(prob: problem.Problem,
              working_dir: pathlib.Path,
              test_ids: Iterable[str],
) -> bool:
    assert(working_dir.is_dir())

    with color_utils.ColorizeStderrBar1():
        print('=' * 20, 'Executing', prob.name, '=' * 20,
              file=sys.stderr)
    print('Command:', prob.run_command,
          file=sys.stderr)

    test_ids = sorted(test_ids)
    if not test_ids:
        with color_utils.ColorizeStderrWarning():
            print('No testcases to run! Generate some with '
                  '"pcu setin" and "pcu setans".',
                  file=sys.stderr)
        return True

    prob_test_ids = set(prob.get_test_ids())
    for test_id in test_ids:
        if test_id not in prob_test_ids:
            with color_utils.ColorizeStderrError():
                print('ERROR: Test case', test_id, 'not found for problem',
                      prob.name,
                      file=sys.stderr)
                return False

    print('Number of testcases:', len(test_ids),
          file=sys.stderr)

    result_counts = \
        collections.defaultdict(int)  # type: DefaultDict[TestCaseResult, int]

    for test_id in test_ids:
        with color_utils.ColorizeStderrBar2():
            print('->', 'Test case', test_id, '-' * 20,
                  file=sys.stderr)
        test_result = _run_case(prob, working_dir, test_id)
        result_counts[test_result] += 1

        with color_utils.ColorizeStderr(*test_result.get_colorize_colors()):
            print('Status:', inflection.humanize(test_result.name))

    with color_utils.ColorizeStderrBar2():
        print('-' * 16, 'Summmary', '-' * 16,
              file=sys.stderr)

    for value in TestCaseResult:
        with color_utils.ColorizeStderr(*value.get_colorize_colors()):
            print('{:25}'.format(inflection.humanize(value.name)),
                  file=sys.stderr, end='')
            print('{:>7} ({:5.1f}%)'.format(result_counts[value],
                                   result_counts[value] * 100.0 / len(test_ids)),
              file=sys.stderr)

    return True


def _run_case(prob, working_dir, test_id) -> TestCaseResult:
    test_input_path = prob.get_test_input_path(test_id)
    test_output_path = prob.get_test_output_path(test_id)
    test_error_path = prob.get_test_error_path(test_id)
    test_answer_path = prob.get_test_answer_path(test_id)
    assert test_input_path.is_file()

    sp_result = None
    input_file = None
    pcu_stdout_path = working_dir / '.pcu_stdout'
    pcu_stderr_path = working_dir / '.pcu_stderr'
    try:
        with open(pcu_stdout_path, 'wb') as stdout, \
                open(pcu_stderr_path, 'wb') as stderr:
            stdin = subprocess.DEVNULL
            if prob.input_file == 'PCU_STDIN':
                input_file = open(test_input_path, 'rb')
                stdin = input_file
            else:
                shutil.copy2(
                    test_input_path, working_dir / prob.input_file)

            try:
                sp_result = subprocess.run(prob.run_command,  # type: ignore
                    cwd = working_dir,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=stderr,
                    timeout=prob.env.run_timelimit_msec * 0.001,
                    shell=True)
            except subprocess.TimeoutExpired:
                return TestCaseResult.TIME_LIMIT_EXCEEDED

    finally:
        if input_file is not None:
            try:
                input_file.close()
            except Exception:
                pass


    assert sp_result is not None
    if sp_result.returncode != 0:
        print('Exit code', sp_result.returncode,
              file=sys.stderr)
        return TestCaseResult.RUNTIME_ERROR

    run_output_path = pcu_stdout_path
    if prob.output_file != 'PCU_STDOUT':
        run_output_path = working_dir / prob.output_file
    if not run_output_path.is_file():
        return TestCaseResult.NO_OUTPUT_FILE_PRODUCED
    shutil.copy2(run_output_path, test_output_path)
    shutil.copy2(pcu_stderr_path, test_error_path)

    if not test_answer_path.is_file():
        return TestCaseResult.NO_ANSWER_FILE_PROVIDED

    with open(test_answer_path, 'r') as infile:
        expected_output = infile.read()
    with open(test_output_path, 'r') as infile:
        actual_output = infile.read()

    match = expected_output == actual_output
    match_minus_whitespace = match or \
        (''.join(expected_output.split()) ==
         ''.join(actual_output.split()))

    if prob.env.format_strictness == environment.FormatStrictness.LAX:
        if match_minus_whitespace:
            return TestCaseResult.CORRECT
    else:
        assert prob.env.format_strictness == environment.FormatStrictness.STRICT
        if match:
            return TestCaseResult.CORRECT

    result = (TestCaseResult.PRESENTATION_ERROR
              if match_minus_whitespace
              else TestCaseResult.WRONG_ANSWER)

    with color_utils.ColorizeStderr(*result.get_colorize_colors()):
        print(inflection.humanize(result.name), "-- here's the diff:",
              file=sys.stderr)

    for line in difflib.unified_diff(expected_output.splitlines(keepends=True),
                                     actual_output.splitlines(keepends=True),
                                     fromfile='expected output',
                                     tofile='actual output',
                                     n=(1 ** 30)):
        sys.stderr.write(line)
        if not line.endswith('\n'):
            sys.stderr.write('<EOF>\n')

    return result

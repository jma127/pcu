import collections
import difflib
import enum
import inflection
import itertools
import os
import pathlib
import shutil
import subprocess
import sys
from typing import DefaultDict, IO, Iterable, List, Optional

from . import color_utils
from . import config
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


def _print_truncate(
    lines: Iterable,
    max_lines: int,
    outfile: IO,
) -> None:
    for i, line in enumerate(itertools.islice(lines, max_lines)):
        if i + 1 == max_lines:
            outfile.write('... (diff goes on) ...\n')
        else:
            outfile.write(line)
            if not line.endswith('\n'):
                outfile.write('<EOF>\n')


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
            print('No test cases to run! Generate some with '
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


def _run_case(prob: problem.Problem,
              working_dir: pathlib.Path,
              test_id: str
) -> TestCaseResult:
    settings = config.get_settings()

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
                    cwd=working_dir,
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

    # Handle some edge cases
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

    # Edge cases are handled, time for the fun stuff now
    with open(test_output_path, 'r') as infile:
        actual_output = infile.read()
        actual_output_lines = actual_output.splitlines()
    result = None
    expected_output = None

    # If no answer file was provided, then we should exit after printing
    # the output/error preview.
    if not test_answer_path.is_file():
        result = TestCaseResult.NO_ANSWER_FILE_PROVIDED

    else:
        with open(test_answer_path, 'r') as infile:
            expected_output = infile.read()
            expected_output_lines = expected_output.splitlines()

        match_exact = expected_output == actual_output
        match_minus_whitespace = match_exact or \
            (''.join(expected_output.split()) ==
             ''.join(actual_output.split()))

        # Figure out the disposition of the test case.
        if prob.env.format_strictness == environment.FormatStrictness.LAX:
            result = (TestCaseResult.CORRECT
                      if match_minus_whitespace
                      else TestCaseResult.WRONG_ANSWER)
        else:
            assert prob.env.format_strictness == environment.FormatStrictness.STRICT
            result = (TestCaseResult.CORRECT
                      if match_exact
                      else (TestCaseResult.PRESENTATION_ERROR
                            if match_minus_whitespace
                            else TestCaseResult.WRONG_ANSWER))

    # If the program was correct, there's nothing to print.
    if result == TestCaseResult.CORRECT:
        return result

    # print either the output or the diff
    if result == TestCaseResult.NO_ANSWER_FILE_PROVIDED:
        with color_utils.ColorizeStderr(*result.get_colorize_colors()):
            print(inflection.humanize(result.name), "-- here's the output:",
                  file=sys.stderr)
        with open(test_output_path, 'r') as infile:
            _print_truncate(infile, settings.max_lines_output, sys.stderr)

    else:
        with color_utils.ColorizeStderr(*result.get_colorize_colors()):
            print(inflection.humanize(result.name), "-- here's the diff:",
                  file=sys.stderr)
        diff_iter = difflib.unified_diff(
            expected_output.splitlines(keepends=True),
            actual_output.splitlines(keepends=True),
            fromfile='expected output',
            tofile='actual output',
            n=(1 ** 30))
        _print_truncate(diff_iter, settings.max_lines_output, sys.stderr)

    # print stderr
    if os.path.getsize(test_error_path) > 0:
        with color_utils.ColorizeStderr(*result.get_colorize_colors()):
            print("> and here's the stderr:",
                  file=sys.stderr)
        with open(test_error_path, 'r') as infile:
            _print_truncate(infile, settings.max_lines_error, sys.stderr)

    return result

import contextlib
import inflection
import itertools
import os
import pathlib
import random
import subprocess
import sys
import tempfile

from . import color_utils
from . import problem


def generate_tests(prob: problem.Problem,
                   executable_path: pathlib.Path,
                   prefix: str,
                   num_cases: int,
) -> bool:
    if not executable_path.is_file():
        with color_utils.ColorizeStderrError():
            print('ERROR:', executable_path, 'is not a file',
                  file=sys.stderr)
        return False

    if not os.access(executable_path, os.X_OK):
        with color_utils.ColorizeStderrError():
            print('ERROR:', executable_path, 'must be executable!',
                  file=sys.stderr)
        return False

    print('Generating', num_cases, 'test cases for problem', prob.name,
          'with executable', executable_path,
          file=sys.stderr)

    existing_test_ids = set(prob.get_test_ids())
    id_gen = (prefix + '{:06d}'.format(i) for i in itertools.count())
    new_test_ids = list(itertools.islice(
        (test_id for test_id in id_gen if test_id not in existing_test_ids),
        num_cases))

    rng = random.SystemRandom()
    for i, test_id in enumerate(new_test_ids):
        seed = rng.getrandbits(31)
        print('Generating', inflection.ordinalize(i), 'case',
              'with id', test_id, 'and seed', seed,
              file=sys.stderr)
        input_path = prob.get_test_input_path(test_id)
        answer_path = prob.get_test_answer_path(test_id)

        if not _generate(i, seed, executable_path, input_path, answer_path):
            with color_utils.ColorizeStderrError():
                print('Terminating early due to error.',
                      file=sys.stderr)
            return False

    with color_utils.ColorizeStderrGood():
        print('Successfully generated', num_cases, 'test cases for',
              'problem', prob.name,
              file=sys.stderr)
    return True


def _generate(seq_num: int,
              seed: int,
              executable_path: pathlib.Path,
              input_path: pathlib.Path,
              answer_path: pathlib.Path,
) -> bool:
    should_unlink_input = False
    should_unlink_answer = False

    try:
        with tempfile.TemporaryDirectory() as tmpdir, \
                open(input_path, 'wb') as input_file, \
                open(answer_path, 'wb') as answer_file:
            args = [
                str(executable_path.resolve()),
                str(seq_num),
                str(seed),
            ]
            try:
                sp_result = subprocess.run(args,
                    cwd=tmpdir,
                    stdin=subprocess.DEVNULL,
                    stdout=input_file,
                    stderr=answer_file)
            except:
                should_unlink_input = True
                should_unlink_answer = True
                raise

        if sp_result.returncode != 0:
            with color_utils.ColorizeStderrError():
                print('ERROR: generator executable finished',
                      'with exit code', sp_result.returncode,
                      file=sys.stderr)
            should_unlink_input = True
            should_unlink_answer = True
            return False

        if os.path.getsize(answer_path) == 0:
            with color_utils.ColorizeStderrWarning():
                print('No answer file generated for this test case.',
                      file=sys.stderr)
                print('(the expected output should be printed to stderr)',
                      file=sys.stderr)
            should_unlink_answer = True

        return True

    finally:
        if should_unlink_input:
            with contextlib.suppress(FileNotFoundError):
                input_path.unlink()
        if should_unlink_answer:
            with contextlib.suppress(FileNotFoundError):
                answer_path.unlink()

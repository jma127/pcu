import pathlib
import shutil
import subprocess
import sys

from . import color_utils
from . import problem


def compile(prob: problem.Problem,
            working_dir: pathlib.Path,
            copy_source:bool = True,
) -> bool:
    assert(working_dir.is_dir())

    source_path = working_dir / prob.source_file

    if copy_source:
        old_source_path = pathlib.Path.cwd() / prob.source_file

        if not old_source_path.is_file():
            with color_utils.ColorizeStderrError():
                print('ERROR: Source file', prob.source_file, 'not found in',
                      'current directory',
                      file=sys.stderr)
                print('(expected at', old_source_path, ')',
                      file=sys.stderr)
                return False

        shutil.copy2(old_source_path, source_path)


    with color_utils.ColorizeStderrBar1():
        print('=' * 20, 'Compiling', prob.name, '=' * 20,
              file=sys.stderr)
    print('Command:', prob.compile_command,
          file=sys.stderr)

    try:
        # typeshed currently says cwd can't be path-like (must be str/bytes)
        sp_result = subprocess.run(prob.compile_command,  # type: ignore
            cwd=working_dir,
            stdin=subprocess.DEVNULL,
            stdout=None,
            stderr=None,
            timeout=prob.env.compile_timelimit_msec * 0.001,
            shell=True)

    except subprocess.TimeoutExpired:
        with color_utils.ColorizeStderrError():
            print('ERROR: Compile timelimit ({} msec) exceeded'.format(
                      prob.env.compile_timelimit_msec),
                  file=sys.stderr)
        return False

    if sp_result.returncode != 0:
        with color_utils.ColorizeStderrError():
            print('ERROR: Compile failed with exit code', sp_result.returncode,
                  file=sys.stderr)
        return False

    with color_utils.ColorizeStderrGood():
        print('Compile was successful!',
              file=sys.stderr)
    return True

#!/usr/bin/env python3

import argparse
import pathlib
import os
import shutil
import subprocess
import venv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dir',
        help='install directory',
        type=pathlib.Path,
        default=(pathlib.Path.home() / '.pcu_venv'),)
    parser.add_argument(
        '-c', '--clean',
        help='whether or not to do a clean install',
        action='store_true')
    args = parser.parse_args()

    builder = venv.EnvBuilder(
        system_site_packages=False,
        clear=args.clean,
        with_pip=True)
    builder.create(args.dir)

    bin_path = args.dir / 'bin'
    pip_path = bin_path / 'pip'
    pcu_path = bin_path / 'pcu'

    subprocess.check_call(
        [pip_path, 'install', pathlib.Path(__file__).parents[0]])

    print('Placing pcu on the system path:')
    placed = False
    path_components = map(pathlib.Path, os.environ['PATH'].split(os.pathsep))
    for path_dir in path_components:
        if placed:
            break
        if not path_dir.is_dir():
            continue
        try:
            potential_pcu_path = path_dir / 'pcu'
            if potential_pcu_path.exists():
                potential_pcu_path.unlink()

            if os.name == 'nt':
                # Windows can't symlink, we need to copy it
                shutil.copy2(pcu_path, potential_pcu_path)
            else:
                os.symlink(pcu_path, potential_pcu_path)

            placed = True
        except Exception:
            pass

    if not placed:
        raise RuntimeError('Unable to place pcu anywhere on the system path!')


if __name__ == '__main__':
    main()

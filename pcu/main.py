import sys

from . import arg_parser
from . import commands
from . import config
from . import paths


def main() -> None:
    try:
        paths.base_path().mkdir(parents=True, exist_ok=True)
        paths.templates_path().mkdir(parents=True, exist_ok=True)
        paths.problems_path().mkdir(parents=True, exist_ok=True)
        paths.locks_path().mkdir(parents=True, exist_ok=True)
        config.get_settings()

        args = arg_parser.parse()

        commands.dispatch(args)

    finally:
        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == '__main__':
    main()

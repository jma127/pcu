import colorama
from colorama import Fore, Back, Style
import sys

from typing import Iterable


class ColorizeStderr(object):
    def __init__(self, *colors) -> None:
        self.colors = colors

    def __enter__(self) -> None:
        colorama.init()
        print(''.join(self.colors), file=sys.stderr, end='')
        sys.stderr.flush()

    def __exit__(self, *args, **kwargs) -> None:
        print(Style.RESET_ALL, file=sys.stderr, end='')
        sys.stderr.flush()
        colorama.deinit()


class ColorizeStderrError(ColorizeStderr):
    def __init__(self, *colors) -> None:
        super().__init__(*(colors + (Fore.RED,)))


class ColorizeStderrWarning(ColorizeStderr):
    def __init__(self, *colors) -> None:
        super().__init__(*(colors + (Fore.YELLOW,)))

class ColorizeStderrGood(ColorizeStderr):
    def __init__(self, *colors) -> None:
        super().__init__(*(colors + (Fore.BLUE,)))


class ColorizeStderrBar1(ColorizeStderr):
    def __init__(self, *colors) -> None:
        super().__init__(*(colors + (Fore.MAGENTA,)))


class ColorizeStderrBar2(ColorizeStderr):
    def __init__(self, *colors) -> None:
        super().__init__(*(colors + (Fore.MAGENTA, Style.BRIGHT)))


def apply_colors(s:str, *colors) -> str:
    return ''.join(colors) + s + Style.RESET_ALL

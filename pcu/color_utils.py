import colorama
from colorama import Fore, Back, Style
import sys
from typing import Any, Optional, Type


class ColorizeStderr(object):
    def __init__(self, *colors: str) -> None:
        self.colors = colors

    def __enter__(self) -> None:
        colorama.init()
        print(''.join(self.colors), file=sys.stderr, end='')
        sys.stderr.flush()

    def __exit__(self,
                 exc_type: Optional[Type],
                 exc_val: Optional[Any],
                 exc_tb: Optional[Any],
    ) -> None:
        print(Style.RESET_ALL, file=sys.stderr, end='')
        sys.stderr.flush()
        colorama.deinit()


class ColorizeStderrError(ColorizeStderr):
    def __init__(self, *colors: str) -> None:
        super().__init__(*(colors + (Fore.RED,)))


class ColorizeStderrWarning(ColorizeStderr):
    def __init__(self, *colors: str) -> None:
        super().__init__(*(colors + (Fore.YELLOW,)))

class ColorizeStderrGood(ColorizeStderr):
    def __init__(self, *colors: str) -> None:
        super().__init__(*(colors + (Fore.BLUE,)))


class ColorizeStderrBar1(ColorizeStderr):
    def __init__(self, *colors: str) -> None:
        super().__init__(*(colors + (Fore.MAGENTA,)))


class ColorizeStderrBar2(ColorizeStderr):
    def __init__(self, *colors: str) -> None:
        super().__init__(*(colors + (Fore.MAGENTA, Style.BRIGHT)))


def apply_colors(s: str, *colors: str) -> str:
    return ''.join(colors) + s + Style.RESET_ALL

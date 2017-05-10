import enum
from typing import Dict, Iterable


class FormatStrictness(enum.Enum):
    LAX = enum.auto()
    STRICT = enum.auto()


class Environment(object):
    def __init__(self,
                 name: str,
                 template_file: str,
                 source_file: str,
                 compile_command: str,
                 run_command: str,
                 input_file: str,
                 output_file: str,
                 compile_timelimit_msec: int,
                 run_timelimit_msec: int,
                 format_strictness: FormatStrictness,
                 aliases: Iterable[str],
    ) -> None:
        self.name = name
        self.template_file = template_file

        # warning: the following five variables are parameterized!
        # use the corresponding variables in Problem.
        self.source_file_p = source_file
        self.compile_command_p = compile_command
        self.run_command_p = run_command
        self.input_file_p = input_file
        self.output_file_p = output_file

        self.compile_timelimit_msec = compile_timelimit_msec
        self.run_timelimit_msec = run_timelimit_msec
        self.format_strictness = format_strictness
        self.aliases = aliases or []

    @classmethod
    def from_dict(cls, d: Dict) -> 'Environment':
        env = cls(
            name=str(d['name']),
            template_file=str(d['template_file']),
            source_file=str(d['source_file']),
            compile_command=str(d['compile_command']),
            run_command=str(d['run_command']),
            input_file=str(d.get('input_file', 'PCU_STDIN')),
            output_file=str(d.get('output_file', 'PCU_STDOUT')),
            compile_timelimit_msec=int(d.get('compile_timelimit_msec', 60000)),
            run_timelimit_msec=int(d.get('run_timelimit_msec', 5000)),
            format_strictness=FormatStrictness[d.get(
                'format_strictness', FormatStrictness.STRICT.name).upper()],
            aliases=d.get('aliases', []),
        )
        return env

    def to_dict(self) -> Dict:
        d = {
            'name': self.name,
            'template_file': self.template_file,
            'source_file': self.source_file_p,
            'compile_command': self.compile_command_p,
            'run_command': self.run_command_p,
            'input_file': self.input_file_p,
            'output_file': self.output_file_p,
            'compile_timelimit_msec': self.compile_timelimit_msec,
            'run_timelimit_msec': self.run_timelimit_msec,
            'format_strictness': self.format_strictness.name.lower(),
            'aliases': self.aliases,
        }
        return d

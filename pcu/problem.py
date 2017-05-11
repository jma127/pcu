import datetime
import filelock
import os
import pathlib
import shutil
import string
import sys
from typing import Any, Dict, Iterable, List, Optional, Type, Union

from . import color_utils
from . import config
from . import environment
from . import paths
from . import yaml_util


class ProblemAlreadyLocked(RuntimeError):
    def __init__(self, problem_name: str, lock_path: Union[str, pathlib.Path]
    ) -> None:
        super().__init__(
            'lock {} is already acquired -- make sure no other pcu '
            'process is running on problem {}'.format(lock_path, problem_name))
        self.problem_name = problem_name
        self.lock_path = lock_path


class ProblemSettingsNotFound(RuntimeError):
    def __init__(self, problem_name: str) -> None:
        super().__init__(
           'Environment constructed with env=None must '
           'already have problem_settings.yaml file. '
           'In other words, the problem {} probably has '
           'not been created via "pcu make" yet.'.format(problem_name))
        self.problem_name = problem_name


class Problem(object):
    def __init__(self,
        name: str,
        env: Optional[environment.Environment] = None,
        clean: bool = False,
        delete_on_exit: bool = False,
        die_on_exc_types: Iterable[Type[BaseException]] = [ProblemAlreadyLocked, ProblemSettingsNotFound],
    ) -> None:
        self.name = name
        self.original_env = env
        self._clean = clean
        self._delete_on_exit = delete_on_exit
        self._die_on_exc_types = tuple(die_on_exc_types)

        # Prepare paths
        self.path = paths.problem_path(self.name)
        self._settings_path = self.path / 'problem_settings.yaml'
        self._lock_path = paths.lock_path('problem.' + self.name)
        self._testcases_path = self.path / 'testcases'

        # Defaults
        self.env_overrides = {}  # type: Dict

        # Set by _init_problem
        self._lock = None  # type: Optional[filelock.FileLock]
        self._acquired = False  # type: bool
        self.env = None  # type: Optional[environment.Environment]

        # Set by _update_mapping
        self.mapping = None  # type: Optional[Dict[str, str]]
        self.source_name = None  # type: Optional[str]
        self.compile_command = None  # type: Optional[str]
        self.run_command = None  # type: Optional[str]
        self.input_file = None  # type: Optional[str]
        self.output_file = None  # type: Optional[str]

    def sub_params(self, s: str) -> str:
        return string.Template(s).safe_substitute(self.mapping)

    def get_test_ids(self) -> List[str]:
        result = []
        for child in self._testcases_path.iterdir():
            if child.is_file() and child.suffix == '.in':
                result.append(child.stem)
        return sorted(result)

    def get_test_input_path(self, test_id: str) -> pathlib.Path:
        return self._testcases_path / (test_id + '.in')

    def get_test_answer_path(self, test_id: str) -> pathlib.Path:
        return self._testcases_path / (test_id + '.ans')

    def get_test_output_path(self, test_id: str) -> pathlib.Path:
        return self._testcases_path / (test_id + '.out')

    def get_test_error_path(self, test_id: str) -> pathlib.Path:
        return self._testcases_path / (test_id + '.err')

    def update_env(self) -> None:
        env_dict = self.original_env.to_dict()
        env_dict.update(self.env_overrides)
        self.env = environment.Environment.from_dict(env_dict)
        self._update_mapping()
        self._write_settings_dict()

    def _get_settings_dict(self) -> Dict:
        d = {
            'env_name': self.original_env.name,
            'env_overrides': self.env_overrides,
        }
        return d

    def _write_settings_dict(self) -> None:
        settings_dict = self._get_settings_dict()
        with open(self._settings_path, 'w') as outfile:
            yaml_util.write_dict(settings_dict, outfile)

    def _update_mapping(self) -> None:
        settings = config.get_settings()

        utc_dt = datetime.datetime.now(datetime.timezone.utc)
        dt = utc_dt.astimezone()
        timestamp = dt.strftime(settings.datetime_format)

        self.mapping = {
            'PCU_USER': settings.user,
            'PCU_DATETIME': timestamp,
            'PCU_PROBLEM_NAME': self.name,
            'PCU_ENV_NAME': self.env.name,
            'PCU_COMPILE_TIMELIMIT_MSEC': str(self.env.compile_timelimit_msec),
            'PCU_RUN_TIMELIMIT_MSEC': str(self.env.run_timelimit_msec),
            'PCU_FORMAT_STRICTNESS': self.env.format_strictness.name,
        }

        self.source_file = self.sub_params(self.env.source_file_p)
        self.mapping['PCU_SOURCE_FILE'] = self.source_file
        self.mapping['PCU_SOURCE_FILE_NOEXT'] = os.path.splitext(self.source_file)[0]

        self.compile_command = self.sub_params(self.env.compile_command_p)
        self.mapping['PCU_COMPILE_COMMAND'] = self.compile_command

        self.run_command = self.sub_params(self.env.run_command_p)
        self.mapping['PCU_RUN_COMMAND'] = self.run_command

        self.input_file = self.sub_params(self.env.input_file_p)
        self.mapping['PCU_INPUT_FILE'] = self.input_file

        self.output_file = self.sub_params(self.env.output_file_p)
        self.mapping['PCU_OUTPUT_FILE'] = self.output_file

    def _init_problem(self) -> None:
        if self._clean and self.path.exists():
            shutil.rmtree(self.path)

        self.path.mkdir(parents=True, exist_ok=True)
        self._testcases_path.mkdir(parents=True, exist_ok=True)

        if self._settings_path.is_file():
            with open(self._settings_path, 'r') as infile:
                data_dict = yaml_util.load_dict(infile.read())
                self.original_env = config.get_settings().get_env(
                    data_dict['env_name'])
                self.env_overrides = data_dict['env_overrides']
        else:
            if self.original_env is None:
                raise ProblemSettingsNotFound(self.name)

        self.update_env()

    def _acquire_lock(self) -> None:
        try:
            if self._lock is None:
                self._lock = filelock.FileLock(self._lock_path)
            self._lock.acquire(0.01)
            self._acquired = True
        except filelock.Timeout:
            self._release_lock()
            raise ProblemAlreadyLocked(self.name, self._lock_path)

    def _release_lock(self) -> None:
        if self._acquired:
            self._lock.release()

    def __enter__(self) -> 'Problem':
        try:
            self._acquire_lock()
            self._init_problem()
            return self
        except:
            self.__exit__(*sys.exc_info())
            raise

    def __exit__(self,
                 exc_type: Optional[Type],
                 exc_val: Optional[Any],
                 exc_tb: Optional[Any],
    ) -> None:
        if self._delete_on_exit:
            try:  # best effort delete
                if self.path.exists():
                    shutil.rmtree(self.path)
            except Exception:
                pass

        self._release_lock()
        if exc_type and issubclass(exc_type, self._die_on_exc_types):
            with color_utils.ColorizeStderrError():
                print('ERROR:', str(exc_val), file=sys.stderr)
                raise SystemExit(3)

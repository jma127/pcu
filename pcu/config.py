import getpass
from typing import Dict, List

from . import defaults
from . import environment
from . import yaml_util
from . import paths


class Settings(object):
    def __init__(self,
                 user: str,
                 default_env: str,
                 datetime_format: str,
                 max_lines_output: int,
                 max_lines_error: int,
                 envs: List[environment.Environment],
    ) -> None:
        self.user = user
        self.default_env = default_env
        self.datetime_format = datetime_format
        self.max_lines_output = max_lines_output
        self.max_lines_error = max_lines_error
        self.envs = envs

        self._envs_dict = {}  # type: Dict[str, environment.Environment]
        for env in self.envs:
            assert env.name not in self._envs_dict
            self._envs_dict[env.name] = env
            for alias in env.aliases:
                assert(alias not in self._envs_dict)
                self._envs_dict[alias] = env

    def get_env_names_and_aliases(self) -> List[str]:
        return list(sorted(self._envs_dict.keys()))

    def get_env(self, env_name: str) -> environment.Environment:
        return self._envs_dict[env_name]

    @classmethod
    def from_dict(cls, d: Dict) -> 'Settings':
        user = str(d['user'])
        if user == 'os_username':
            user = getpass.getuser()

        envs = []
        for k, v in d['envs'].items():
            env_dict = dict(v)
            env_dict['name'] = k
            envs.append(environment.Environment.from_dict(env_dict))

        settings = Settings(
            user=user,
            default_env=str(d['default_env']),
            datetime_format=str(d['datetime_format']),
            max_lines_output=int(d['max_lines_output']),
            max_lines_error=int(d['max_lines_error']),
            envs=envs,
        )
        return settings

    @classmethod
    def from_yaml(cls, default_data: str, settings_data: str) -> 'Settings':
        default = yaml_util.load_dict(default_data)
        settings = yaml_util.load_dict(settings_data)
        all_settings = _update_dict(default, settings)
        return cls.from_dict(all_settings)


def _update_dict(d: Dict, u: Dict) -> Dict:
    for k, v in u.items():
        if isinstance(v, dict):
            r = _update_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def _load_settings() -> Settings:
    default_data = defaults.default_settings_data()
    settings_path = paths.settings_path()

    if not settings_path.is_file():
        with open(settings_path, 'w') as outfile:
            print('# See documentation for comment format', file=outfile)

    with open(settings_path, 'r') as infile:
        settings_data = infile.read()

    return Settings.from_yaml(default_data, settings_data)


_cached_settings = None  # type: Settings
def get_settings() -> Settings:
    global _cached_settings
    if not _cached_settings:
        _cached_settings = _load_settings()
    return _cached_settings

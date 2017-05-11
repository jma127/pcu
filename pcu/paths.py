import functools
import pathlib


@functools.lru_cache(maxsize=None, typed=True)
def base_path() -> pathlib.Path:
    base_path = pathlib.Path.home() / '.pcu'
    return base_path


@functools.lru_cache(maxsize=None, typed=True)
def settings_path() -> pathlib.Path:
    settings_path = base_path() / 'settings.yaml'
    return settings_path


@functools.lru_cache(maxsize=None, typed=True)
def templates_path() -> pathlib.Path:
    templates_path = base_path() / 'templates'
    return templates_path


@functools.lru_cache(maxsize=None, typed=True)
def template_path(template_file: str) -> pathlib.Path:
    template_path = templates_path() / template_file
    return template_path


@functools.lru_cache(maxsize=None, typed=True)
def problems_path() -> pathlib.Path:
    problems_path = base_path() / 'problems'
    return problems_path


@functools.lru_cache(maxsize=None, typed=True)
def problem_path(problem_name: str) -> pathlib.Path:
    problem_path = problems_path() / problem_name
    return problem_path


@functools.lru_cache(maxsize=None, typed=True)
def locks_path() -> pathlib.Path:
    locks_path = base_path() / '.locks'
    return locks_path


@functools.lru_cache(maxsize=None, typed=True)
def lock_path(lock_name: str) -> pathlib.Path:
    lock_fn = lock_name + '.lock'
    lock_path = locks_path() / lock_fn
    return lock_path

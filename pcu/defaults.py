import pkg_resources
from typing import Optional


_TOP_PACKAGE = __name__.rpartition('.')[0]


def exists_static(path: str) -> bool:
    return pkg_resources.resource_exists(_TOP_PACKAGE, 'static/' + path)


def load_static(path: str) -> bytes:
    return pkg_resources.resource_string(_TOP_PACKAGE, 'static/' + path)


def default_settings_data() -> str:
    return load_static('default_settings.yaml').decode()


def default_template(template: str) -> Optional[str]:
    internal_path = 'default_templates/' + template
    return load_static(internal_path).decode() \
        if exists_static(internal_path) else None

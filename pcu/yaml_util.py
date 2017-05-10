from typing import Dict, IO
import yaml


def load_dict(s) -> Dict:
    if not s:
        return {}

    d = yaml.safe_load(s)
    if d is None:
        return {}

    assert(isinstance(d, dict))
    return d


def write_dict(d: Dict, f: IO) -> None:
    yaml.safe_dump(d, stream=f)


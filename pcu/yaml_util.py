from typing import Dict, IO, Optional
import yaml


def load_dict(s: Optional[str]) -> Dict:
    if not s:
        return {}

    d = yaml.safe_load(s)
    if d is None:
        return {}

    assert(isinstance(d, dict))
    return d


def write_dict(d: Dict, f: IO) -> None:
    yaml.safe_dump(d, stream=f)

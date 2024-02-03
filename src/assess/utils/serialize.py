import json
from typing import Dict, List, Union

import tomlkit


def load_text_file(path: str) -> str:
    with open(path) as f:
        result = f.read().strip()
    return result


def write_text_file(text: str, path: str):
    with open(path, "w") as f:
        f.write(text)


def load_toml_file(path: str) -> Dict:
    raw = load_text_file(path)
    return tomlkit.parse(raw)


def write_toml_file(data: Dict, path: str):
    with open(path, "w") as f:
        f.write(tomlkit.dumps(data))


def load_json_file(path: str) -> Union[Dict, List]:
    with open(path) as f:
        result = json.load(f)
    return result


def write_json_file(data: Union[Dict, List], path: str):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

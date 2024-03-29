import json
import os
from typing import Dict, List, Union

import tomlkit
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


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


def load_pdf_file(path: str, as_raw_text: bool = False) -> List[Document]:
    loader = PyPDFLoader(path)
    result = loader.load_and_split()
    if as_raw_text:
        return "\n\n".join(x.page_content for x in result)
    else:
        return result


def load_assesment_criteria(criteria_for: str) -> Dict:
    this_file_dirname = os.path.dirname(os.path.abspath(__file__))
    package_root = os.path.dirname(this_file_dirname)
    crieria_path = os.path.join(
        package_root, "models", "criteria", f"{criteria_for}.toml"
    )
    return load_toml_file(crieria_path)

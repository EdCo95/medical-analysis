import os
from enum import Enum


class TestConstant(Enum):
    DATA_DIRNAME = "data"
    TEXT_FILE = "a_test_file.txt"
    TOML_FILE = "a_test_toml.toml"
    JSON_FILE = "a_test_json.json"


def get_data_dir_path() -> str:
    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.dirname(this_file_dir)
    return os.path.join(tests_dir, TestConstant.DATA_DIRNAME.value)


def get_test_text_file_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.TEXT_FILE.value)


def get_test_toml_file_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.TOML_FILE.value)


def get_test_json_file_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.JSON_FILE.value)

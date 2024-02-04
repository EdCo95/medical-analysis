import os
from enum import Enum
from typing import List, Union

from langchain_core.documents import Document

from assess.utils import serialize


class TestConstant(Enum):
    DATA_DIRNAME = "data"
    TEXT_FILE = "a_test_file.txt"
    TOML_FILE = "a_test_toml.toml"
    JSON_FILE = "a_test_json.json"
    PDF_FILE = "a_test_pdf.pdf"

    MEDICAL_RECORD_ONE = "medical-record-1.pdf"
    MEDICAL_RECORD_TWO = "medical-record-2.pdf"
    MEDICAL_RECORD_THREE = "medical-record-3.pdf"
    NON_MATCHING_RECORD = "non_matching_medical_record.pdf"


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


def get_test_pdf_file_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.PDF_FILE.value)


def get_medical_record_one_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.MEDICAL_RECORD_ONE.value)


def get_medical_record_two_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.MEDICAL_RECORD_TWO.value)


def get_medical_record_three_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.MEDICAL_RECORD_THREE.value)


def get_incorrect_medical_record_path() -> str:
    return os.path.join(get_data_dir_path(), TestConstant.NON_MATCHING_RECORD.value)


def load_medical_record_1(as_raw_text: bool = False) -> Union[List[Document], str]:
    return serialize.load_pdf_file(
        os.path.join(get_data_dir_path(), TestConstant.MEDICAL_RECORD_ONE.value),
        as_raw_text=as_raw_text,
    )


def load_medical_record_2(as_raw_text: bool = False) -> Union[List[Document], str]:
    return serialize.load_pdf_file(
        os.path.join(get_data_dir_path(), TestConstant.MEDICAL_RECORD_TWO.value),
        as_raw_text=as_raw_text,
    )


def load_medical_record_3(as_raw_text: bool = False) -> Union[List[Document], str]:
    return serialize.load_pdf_file(
        os.path.join(get_data_dir_path(), TestConstant.MEDICAL_RECORD_THREE.value),
        as_raw_text=as_raw_text,
    )

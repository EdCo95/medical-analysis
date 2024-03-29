import os
import shutil
import tempfile
import unittest

from assess.utils import serialize
from tests.tools import data_handler


class SerializeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_that_load_text_file_returns_the_contents_of_a_text_file(self):
        expected = "Hello World!"
        result = serialize.load_text_file(data_handler.get_test_text_file_path())
        self.assertEqual(expected, result)

    def test_that_write_text_file_successfully_writes_a_string_to_a_file(self):
        expected = "Hello World!"
        write_path = os.path.join(self.temp_dir, "test.txt")
        self.assertFalse(os.path.exists(write_path))
        serialize.write_text_file(text=expected, path=write_path)
        self.assertTrue(os.path.exists(write_path))
        result = serialize.load_text_file(write_path)
        self.assertEqual(expected, result)

    def test_that_load_toml_file_correctly_loads_data_in_a_toml_file(self):
        expected = {"test-system": {"super_awesome": True}}
        result = serialize.load_toml_file(data_handler.get_test_toml_file_path())
        self.assertDictEqual(expected, result)

    def test_that_write_toml_file_correctly_writes_data_to_a_toml_file(self):
        to_write = {"test-system": {"super_awesome": True}}
        write_path = os.path.join(self.temp_dir, "test.toml")
        self.assertFalse(os.path.exists(write_path))
        serialize.write_toml_file(data=to_write, path=write_path)
        self.assertTrue(os.path.exists(write_path))
        result = serialize.load_toml_file(write_path)
        self.assertDictEqual(to_write, result)

    def test_that_load_json_file_correctly_loads_data_in_a_json_file(self):
        expected = {"super-awesome": True}
        result = serialize.load_json_file(data_handler.get_test_json_file_path())
        self.assertDictEqual(expected, result)

    def test_that_writing_a_json_file_correctly_writes_data_to_a_json_file(self):
        to_write = {"super_awesome": True}
        write_path = os.path.join(self.temp_dir, "test.json")
        self.assertFalse(os.path.exists(write_path))
        serialize.write_json_file(data=to_write, path=write_path)
        self.assertTrue(os.path.exists(write_path))
        result = serialize.load_json_file(write_path)
        self.assertDictEqual(to_write, result)

    def test_that_it_can_load_a_pdf_file(self):
        expected = ["Successfully\nloaded\na\nPDF!"]
        result = serialize.load_pdf_file(data_handler.get_test_pdf_file_path())
        result = [x.page_content for x in result]
        self.assertListEqual(expected, result)

    def test_that_it_can_load_a_pdf_file_as_raw_text(self):
        expected = "Successfully\nloaded\na\nPDF!"
        result = serialize.load_pdf_file(
            data_handler.get_test_pdf_file_path(), as_raw_text=True
        )
        self.assertEqual(expected, result)

    def test_that_it_can_load_assessment_criteria(self):
        expected = data_handler.load_example_treatment_criteria()
        result = serialize.load_assesment_criteria(criteria_for="colonoscopy")
        self.assertDictEqual(expected, result)

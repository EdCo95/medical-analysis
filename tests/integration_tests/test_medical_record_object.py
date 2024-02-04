import unittest

from assess.structures.medical_record import MedicalRecord
from tests.tools import data_handler


class MedicalRecordTestCase(unittest.TestCase):

    def _get_record(self, record_path: str) -> MedicalRecord:
        return MedicalRecord.from_pdf(record_path)

    def test_that_it_can_extract_the_requested_procedure_codes_record_one(self):
        record = self._get_record(data_handler.get_medical_record_one_path())
        expected = "45378"
        result = record.extract_requested_cpt_codes()
        self.assertTrue(expected in result)

    def test_that_it_can_extract_the_requested_procedure_codes_record_two(self):
        record = self._get_record(data_handler.get_medical_record_two_path())
        expected = "45378"
        result = record.extract_requested_cpt_codes()
        self.assertTrue(expected in result)

    def test_that_it_can_extract_the_requested_procedure_codes_record_three(self):
        record = self._get_record(data_handler.get_medical_record_three_path())
        expected = ["43235", "43239"]
        result = record.extract_requested_cpt_codes()
        self.assertTrue(all(x in result for x in expected))

    # def test_that_it_can_verify_the_extracted_procedure_codes(self):
    #     record = self._get_record(data_handler.get_medical_record_one_path())
    #     raise NotImplementedError

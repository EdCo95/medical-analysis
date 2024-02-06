import unittest

from assess.models.assessors import Assessor, GPT4Assessor
from assess.structures.criteria import AssessmentCriteria
from assess.structures.medical_record import MedicalRecord
from tests.tools import data_handler


class AssessorTestCase(unittest.TestCase):

    def _get_assessor(self) -> Assessor:
        return GPT4Assessor()

    def test_that_it_can_assess_a_medical_record_against_a_criteria(self):
        assessor = self._get_assessor()
        criteria = AssessmentCriteria.from_spec("colonoscopy")

        medical_record = data_handler.load_medical_record_1()
        medical_record = MedicalRecord(pages=medical_record)
        result = assessor.assess_criteria(criteria=criteria, record=medical_record)
        self.assertTrue(result.strip().startswith("[YES]"))

        medical_record = data_handler.load_medical_record_2()
        medical_record = MedicalRecord(pages=medical_record)
        result = assessor.assess_criteria(criteria=criteria, record=medical_record)
        self.assertTrue(result.strip().startswith("[YES]"))

        medical_record = data_handler.load_medical_record_3()
        medical_record = MedicalRecord(pages=medical_record)
        result = assessor.assess_criteria(criteria=criteria, record=medical_record)
        self.assertTrue(result.strip().startswith("[NO]"))

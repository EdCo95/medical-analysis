import unittest

from assess.structures.criteria import AssessmentCriteria
from assess.utils import serialize
from tests.tools import data_handler


class CriteriaTestCase(unittest.TestCase):

    def _get_criteria(self) -> AssessmentCriteria:
        return AssessmentCriteria.from_spec("colonoscopy")

    def test_that_it_can_load_sections(self):
        raw_criteria = serialize.load_assesment_criteria("colonoscopy")
        expected_descriptions = []
        for key, value in raw_criteria.items():
            if isinstance(value, dict):
                expected_descriptions.append((key, value["criteria"]))
        criteria = self._get_criteria()
        result = criteria.get_sections()
        self.assertListEqual(expected_descriptions, result)

    def test_that_it_can_load_a_main_description(self):
        expected = data_handler.load_example_treatment_criteria()["description"]
        result = self._get_criteria().get_description()
        self.assertEqual(expected.strip(), result.strip())

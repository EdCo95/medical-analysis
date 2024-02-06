import unittest

from assess.structures.criteria import AssessmentCriteria
from assess.utils import serialize


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
        expected = (
            "This document provides the assessment criteria for whether a "
            "patient is eligible for a colonoscopy procedure.\n\nBelow are "
            "several sections describing different criteria. The title of "
            "each section is delineated by square brackets.\n\nA patient is "
            "eligible for a colonoscopy if they satisfy ANY SINGLE ONE OF THOSE SECTIONS."
        )
        result = self._get_criteria().get_description()
        self.assertEqual(expected.strip(), result.strip())

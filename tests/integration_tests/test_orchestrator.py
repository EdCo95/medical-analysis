import unittest

from assess.models.orchestrator import Orchestrator
from assess.structures.criteria import AssessmentCriteria
from assess.structures.medical_record import MedicalRecord
from tests.tools import data_handler


class OrchestratorTestCase(unittest.TestCase):

    def _get_orchestrator(self) -> Orchestrator:
        return Orchestrator()

    def test_that_given_a_criteria_and_medical_record_path_it_returns_a_markdown_assesment_string(
        self,
    ):
        record = MedicalRecord(data_handler.load_medical_record_1())
        orchestrator = self._get_orchestrator()
        result = orchestrator.run_pipeline(
            criteria=AssessmentCriteria.from_spec("colonoscopy"), record=record
        )
        print(result)

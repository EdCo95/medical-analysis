from assess.models.assessors import GPT4Assessor
from assess.structures.criteria import AssessmentCriteria
from assess.structures.medical_record import MedicalRecord


class Orchestrator:

    def __init__(self):
        self.assessor = GPT4Assessor()

    def run_pipeline(self, criteria: AssessmentCriteria, record: MedicalRecord) -> str:
        """Runs the full assessment pipeline and returns the evidence as a Markdown string."""
        codes = record.extract_and_validate_cpt_codes()
        print(codes)
        input("Wait")

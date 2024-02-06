from assess.models.assessors import GPT4Assessor
from assess.structures.criteria import AssessmentCriteria
from assess.structures.medical_record import MedicalRecord


class DocConstants:
    INTRO = (
        "This document summarises whether the treatment recommended by the doctor"
        " meets the criteria for that assessment."
    )


class Orchestrator:

    def __init__(self):
        self.assessor = GPT4Assessor()

    def run_pipeline(self, criteria: AssessmentCriteria, record: MedicalRecord) -> str:
        """Runs the full assessment pipeline and returns the evidence as a Markdown string."""
        patient_profile = record.extract_patient_profile()

        result = (
            f"# Assessment of Recommended Procedure for {patient_profile['name']}\n"
        )
        result += DocConstants.INTRO + "\n\n"

        # conservative_treatment = record.check_for_previous_conservative_treatment()

        result += "## Recommended Procedure and CPT Codes\n"
        codes = record.extract_and_validate_cpt_codes()
        for title, llm_response in codes.items():
            result += f"### {title}\n"
            result += llm_response + "\n\n"

        print(result)
        # input("Wait")

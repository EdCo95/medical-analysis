from typing import OrderedDict

from loguru import logger

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

    def _add_cpt_code_analysis(self, record: MedicalRecord) -> str:
        result = "## Recommended Procedure and CPT Codes\n"
        codes = record.extract_and_validate_cpt_codes()
        for title, llm_response in codes.items():
            result += f"### {title}\n"
            result += llm_response + "\n\n"
        return result

    def _handle_case_prev_treatment_helped(
        self, record: MedicalRecord, result: str, prev_treatments: OrderedDict[str, str]
    ) -> str:
        logger.info(
            "Previous treatment helped. Stopping pipeline execution and presenting evidence."
        )
        result += "**Assessment:** THIS TREATMENT IS NOT RECOMMENDED.\n"
        result += (
            "**Reason:** Previous conservative treatment has shown improvement and "
            "should be continued (see below)\n\n"
        )

        result += "## Justification for Continuing Conservative Treatment\n"
        result += record.present_evidence_treatment_helped() + "\n\n"

        result += self._add_cpt_code_analysis(record)
        return result

    def _handle_case_prev_treatment_didnt_help(
        self,
        criteria: AssessmentCriteria,
        record: MedicalRecord,
        result: str,
        prev_treatments: OrderedDict[str, str],
    ) -> str:
        logger.info("Previous treatment did not help. Assessing against criteria.")
        # result = self.assessor.assess_criteria(criteria, record)

    def run_pipeline(self, criteria: AssessmentCriteria, record: MedicalRecord) -> str:
        """Runs the full assessment pipeline and returns the evidence as a Markdown string."""
        patient_profile = record.extract_patient_profile()

        result = (
            f"# Assessment of Recommended Procedure for {patient_profile['name']}\n"
        )
        result += DocConstants.INTRO + "\n\n"

        prev_treatments, did_succeed = (
            record.check_for_previous_conservative_treatment()
        )

        if did_succeed:
            return self._handle_case_prev_treatment_helped(
                record, result, prev_treatments
            )
        else:
            return self._handle_case_prev_treatment_didnt_help(result, prev_treatments)

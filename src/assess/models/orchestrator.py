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

    def _add_previous_treatments(
        self, result: str, prev_treatments: OrderedDict[str, str]
    ) -> str:
        result += "## Previous Treatments\n"
        for key, val in prev_treatments.items():
            result += f"### {key}\n{val}\n\n"
        return result

    def _handle_case_prev_treatment_helped(
        self, record: MedicalRecord, result: str, prev_treatments: OrderedDict[str, str]
    ) -> str:
        logger.info(
            "Previous treatment helped. Stopping pipeline execution and presenting evidence."
        )
        result += "**Assessment:** DENIED\n\n"
        result += (
            "**Reason:** Previous conservative treatment has shown improvement and "
            "should be continued (see below)\n\n"
        )

        result = self._add_previous_treatments(result, prev_treatments)

        result += "## Justification for Continuing Conservative Treatment\n"
        result += record.present_evidence_treatment_helped() + "\n\n"

        result += self._add_cpt_code_analysis(record)
        return result

    def _add_approved_stamp(self, result: str) -> str:
        result += "**Assessment:** APPROVED\n\n"
        result += "**Reason:** The patient meets the criteria for the recommended treatment (see below)\n\n"
        return result

    def _add_denied_stamp(self, result: str) -> str:
        result += "**Assessment:** DENIED\n\n"
        result += "**Reason:** The patient does not meet the criteria for the recommended treatment (see below)\n\n"
        return result

    def _add_criteria(self, result: str, criteria: AssessmentCriteria) -> str:
        result += "## Assessment Criteria\n"
        result += criteria.get_description() + "\n"
        for key, val in criteria.get_sections():
            result += f"### {key.replace('-', ' ').title()}\n{val}\n\n"
        return result

    def _handle_case_prev_treatment_didnt_help(
        self,
        criteria: AssessmentCriteria,
        record: MedicalRecord,
        result: str,
        prev_treatments: OrderedDict[str, str],
    ) -> str:
        logger.info("Previous treatment did not help. Assessing against criteria.")
        analysis_dict, approved = self.assessor.assess_criteria(criteria, record)

        if approved:
            result = self._add_approved_stamp(result)
        else:
            result = self._add_denied_stamp(result)

        result = self._add_previous_treatments(result, prev_treatments)

        result += f"## Final Assessment\n{analysis_dict['Final Assessment']}\n\n"

        for key, val in analysis_dict.items():
            if key == "Final Assessment":
                continue
            result += f"## {key}\n{val}\n\n"

        result += self._add_cpt_code_analysis(record)

        result = self._add_criteria(result, criteria)

        return result

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
            return self._handle_case_prev_treatment_didnt_help(
                criteria=criteria,
                record=record,
                result=result,
                prev_treatments=prev_treatments,
            )

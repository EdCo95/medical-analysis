from collections import OrderedDict
from datetime import datetime
from typing import Dict, List, Tuple

from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, Field
from loguru import logger

from assess.models.doc_readers import GPT3_5SingleDocumentInterpreter
from assess.structures import prompts
from assess.structures.prompts import PromptConstant
from assess.utils import retry_tools, serialize


class PatientProfile(BaseModel):
    name: str = Field(description="The name of the patient")
    dob: str = Field(description="The patient's date of birth")


class MedicalRecord:

    def __init__(self, pages: List[Document]):
        self.pages = pages
        self.advisor = GPT3_5SingleDocumentInterpreter()

    def extract_requested_cpt_codes(self) -> str:
        """Reads the document to extract the CPT codes of the recommended procedure."""
        result = self.advisor.ask(prompts.ASK_FOR_CPT_CODES, context=self.pages)
        return result

    def extract_and_validate_cpt_codes(self) -> OrderedDict[str, str]:
        """
        Reads the CPT codes then checks that the procedure they correspond to aligns with the note description.
        """
        result = OrderedDict()
        summary = self.advisor.ask(prompts.SUMMARISE_DOCTORS_ORDERS, context=self.pages)
        result["Summary of Recommended Treatment"] = summary
        logger.info(f"Summary of Doctor's Recommended Treatment: {summary}")

        codes = self.extract_requested_cpt_codes()
        result["Extracted CPT Codes"] = codes
        logger.info(f"Extracted CPT codes: {codes}")

        code_meaning = self.advisor.web_search(
            prompts.CPT_WEB_SEARCH.format(codes=codes)
        )
        code_meaning = self.advisor.ask(
            prompts.SUMMARISE_CODE_MEANINGS.format(codes=codes),
            search_results=code_meaning,
        )
        result["Search Results For Code Meanings"] = code_meaning
        logger.info(
            f"Found and summarised the following online regarding these codes: {code_meaning}"
        )

        does_match = self.advisor.ask(
            s=prompts.DETERMINE_MATCH.format(
                summary=summary, codes=codes, code_meaning=code_meaning
            ),
            context=self.pages,
        )
        result["Codes Match Suggested Treatment"] = does_match
        logger.info(
            f"Confirming that those codes match what the doctor has said in the text: {does_match}"
        )
        return result

    def check_for_previous_conservative_treatment(
        self,
    ) -> Tuple[OrderedDict[str, str], bool]:
        result = OrderedDict()
        summary = self.advisor.ask(
            prompts.SUMMARY_OF_TREATMENT_SO_FAR, context=self.pages
        )
        result["Summary of Treatment Received To Date"] = summary
        logger.info(f"Summarised attempts to help the patient so far: {summary}")

        confirmation = self.advisor.ask(
            prompts.YES_NO_DID_ANYTHING_HELP, context=[Document(page_content=summary)]
        )
        result["Has Any Previous Treatment Helped the Patient?"] = confirmation
        logger.info(f"Interpretation: did anything help the patient? {confirmation}")

        if confirmation.strip() == PromptConstant.YES.value:
            return result, True
        elif confirmation.strip() == PromptConstant.NO.value:
            return result, False
        else:
            raise ValueError(
                f'Confirmation did not respond with yes or no (responded with "{confirmation}")'
            )

    def present_evidence_treatment_helped(self):
        evidence = self.advisor.ask(
            "Please extract evidence which shows that there has been an improvement in the patient's condition, especially as the result of any treatment. QUOTE THE RELEVANT EVIDENCE VERBATIM. Present each piece of evidence in a numbered list. Each item should contain THE VERBATIM QUOTE FROM THE CONTEXT and an explanation of why this constitutes evidence that the patient's condition improved.",
            context=self.pages,
        )
        return evidence

    @retry_tools.retry_on_failure(tolerance=3)
    def extract_patient_profile(self) -> Dict:
        extracted = self.advisor.extract_json(
            "Extract the patient's name and date of birth in JSON format.",
            json_structure=PatientProfile,
            context=self.pages,
        )
        dob_dt = extracted["dob"]
        dob_dt = datetime.strptime(dob_dt, "%m/%d/%Y")
        age = (datetime.now() - dob_dt).days // 365
        extracted["age"] = str(age)
        return extracted

    @classmethod
    def from_pdf(cls, pdf_path: str) -> "MedicalRecord":
        data = serialize.load_pdf_file(pdf_path)
        return cls(pages=data)

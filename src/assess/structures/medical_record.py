from typing import List

from langchain_core.documents import Document
from loguru import logger

from assess.models.advisor import GPT3_5Advisor
from assess.structures import prompts
from assess.utils import serialize


class MedicalRecord:

    def __init__(self, pages: List[Document]):
        self.pages = pages
        self.advisor = GPT3_5Advisor()

    def extract_requested_cpt_codes(self) -> str:
        """Reads the document to extract the CPT codes of the recommended procedure."""
        result = self.advisor.ask(prompts.ASK_FOR_CPT_CODES, context=self.pages)
        return result

    def extract_and_validate_cpt_codes(self) -> str:
        """
        Reads the CPT codes then checks that the procedure they correspond to aligns with the note description.
        """
        summary = self.advisor.ask(prompts.SUMMARISE_DOCTORS_ORDERS, context=self.pages)
        logger.info(f"Summary of Doctor's Recommended Treatment: {summary}")
        codes = self.extract_requested_cpt_codes()
        logger.info(f"Extracted CPT codes: {codes}")
        code_meaning = self.advisor.web_search(
            prompts.CPT_WEB_SEARCH.format(codes=codes)
        )
        code_meaning = self.advisor.ask(
            prompts.SUMMARISE_CODE_MEANINGS.format(codes=codes),
            search_results=code_meaning,
        )
        logger.info(
            f"Found and summarised the following online regarding these codes: {code_meaning}"
        )
        does_match = self.advisor.ask(
            s=prompts.DETERMINE_MATCH.format(
                summary=summary, codes=codes, code_meaning=code_meaning
            ),
            context=self.pages,
        )
        logger.info(
            f"Confirming that those codes match what the doctor has said in the text: {does_match}"
        )
        return does_match

    @classmethod
    def from_pdf(cls, pdf_path: str) -> "MedicalRecord":
        data = serialize.load_pdf_file(pdf_path)
        return cls(pages=data)

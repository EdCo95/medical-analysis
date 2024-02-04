from typing import List

from langchain_core.documents import Document

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

    @classmethod
    def from_pdf(cls, pdf_path: str) -> "MedicalRecord":
        data = serialize.load_pdf_file(pdf_path)
        return cls(pages=data)

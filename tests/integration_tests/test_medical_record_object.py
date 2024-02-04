import unittest

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from assess.structures.medical_record import MedicalRecord
from tests.tools import data_handler


class MedicalRecordTestCase(unittest.TestCase):

    def _get_record(self, record_path: str) -> MedicalRecord:
        return MedicalRecord.from_pdf(record_path)

    def test_that_it_can_extract_the_requested_procedure_codes_record_one(self):
        record = self._get_record(data_handler.get_medical_record_one_path())
        expected = "45378"
        result = record.extract_requested_cpt_codes()
        self.assertTrue(expected in result)

    def test_that_it_can_extract_the_requested_procedure_codes_record_two(self):
        record = self._get_record(data_handler.get_medical_record_two_path())
        expected = "45378"
        result = record.extract_requested_cpt_codes()
        self.assertTrue(expected in result)

    def test_that_it_can_extract_the_requested_procedure_codes_record_three(self):
        record = self._get_record(data_handler.get_medical_record_three_path())
        expected = ["43235", "43239"]
        result = record.extract_requested_cpt_codes()
        self.assertTrue(all(x in result for x in expected))

    def test_that_it_can_verify_the_extracted_procedure_codes_match_what_the_doctor_ordered(
        self,
    ):
        record = self._get_record(data_handler.get_medical_record_one_path())
        result = record.extract_and_validate_cpt_codes()
        self.assertTrue("[ERROR]" not in result)

        record = self._get_record(data_handler.get_incorrect_medical_record_path())
        result = record.extract_and_validate_cpt_codes()
        self.assertTrue("[ERROR]" in result)

    def test_that_it_can_check_for_previous_conservative_treatment(self):
        record = self._get_record(data_handler.get_medical_record_one_path())
        result, prev_treatment_helped = (
            record.check_for_previous_conservative_treatment()
        )
        self.assertTrue(prev_treatment_helped)

        record = self._get_record(data_handler.get_medical_record_two_path())
        result, prev_treatment_helped = (
            record.check_for_previous_conservative_treatment()
        )
        self.assertFalse(prev_treatment_helped)

        record = self._get_record(data_handler.get_medical_record_three_path())
        result, prev_treatment_helped = (
            record.check_for_previous_conservative_treatment()
        )
        self.assertFalse(prev_treatment_helped)

        record = self._get_record(data_handler.get_incorrect_medical_record_path())
        result, prev_treatment_helped = (
            record.check_for_previous_conservative_treatment()
        )
        self.assertFalse(prev_treatment_helped)

    def test_that_it_can_present_evidence_treatment_helped(self):
        record = self._get_record(data_handler.get_medical_record_one_path())
        result = record.present_evidence_treatment_helped()

        check_prompt = ChatPromptTemplate.from_template(
            """Examine the context below. The context should present evidence that treatment helped. Does it? If so, output just the word YES

            <context>
            {context}
            </contex>
            """
        )
        llm = ChatOpenAI()
        chain = check_prompt | llm | StrOutputParser()
        result = chain.invoke({"context": result})
        self.assertEqual(result.strip(), "YES")

import os
import unittest

from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, Field

from assess.models.advisor import (
    Advisor,
    AdvisorFactory,
    AdvisorType,
    MissingApiKeyExcepetion,
)
from assess.utils import serialize
from tests.tools import data_handler


class ExampleJson(BaseModel):
    name: str = Field(description="The patient's name")
    dob: str = Field(description="The patient's date of birth")


class AdvisorTestCase(unittest.TestCase):

    def _get_advisor(self, flavour: AdvisorType = AdvisorType.GPT_4) -> Advisor:
        return AdvisorFactory(flavour).get_advisor()

    def test_that_advisors_can_be_asked_arbitrary_prompts_and_return_strings(self):
        gpt4_advisor = self._get_advisor()
        result = gpt4_advisor.ask("Hello!")
        self.assertIsInstance(result, str)

        gpt3_5_advisor = self._get_advisor(flavour=AdvisorType.GPT_3_5)
        result = gpt3_5_advisor.ask("Hello!")
        self.assertIsInstance(result, str)

    def test_that_advisors_can_answer_questions_based_on_context(self):
        advisor = self._get_advisor(AdvisorType.GPT_3_5)
        context = data_handler.load_medical_record_1()
        expected = "yes"
        result = advisor.ask(
            "Does the provided context seem to be a medical report? Give an extremely "
            "concise answer showing your reasoning.",
            context=context,
        )
        self.assertTrue(expected in result.lower())

    def test_that_advisors_can_answer_questions_based_on_search_results(self):
        advisor = self._get_advisor(AdvisorType.GPT_3_5)
        expected = "yes"
        result = advisor.ask(
            "Is Cheddar a type of cheese?",
            search_results="A very popular type of cheese, Cheddar is also a town in the west country",
        )
        self.assertTrue(expected in result.lower())

    def test_that_advisors_can_answer_questions_based_on_context_and_search_results(
        self,
    ):
        advisor = self._get_advisor(AdvisorType.GPT_3_5)
        context = data_handler.load_medical_record_1()
        expected = "yes"
        result = advisor.ask(
            "Do the search results match the treatment which the doctor has recommended? If so, say 'yes'. "
            "Be concise but show your reasoning.",
            context=context,
            search_results="45378 is a colonoscopy",
        )
        self.assertTrue(expected in result.lower())

    def test_that_no_api_key_raises_an_appropriate_error(self):
        existing_key = os.environ.get("OPENAI_API_KEY")
        if existing_key:
            del os.environ["OPENAI_API_KEY"]

        try:
            self._get_advisor(AdvisorType.GPT_3_5)
        except MissingApiKeyExcepetion:
            print("Test passed.")
        except Exception as e:
            self.fail(
                f"Did not raise the expected exception, raise {type(e).__name__} instead."
            )
        finally:
            if existing_key:
                os.environ["OPENAI_API_KEY"] = existing_key

    def test_that_the_base_advisor_class_provides_a_web_search_function(self):
        advisor = Advisor()
        result = advisor.web_search("CPT Code 43578")
        print(result)

    def test_that_json_structures_can_be_extracted(self):
        advisor = self._get_advisor(AdvisorType.GPT_3_5)
        context = data_handler.load_medical_record_1()
        result = advisor.extract_json(
            "Extract the patient's name and date of birth in JSON format.",
            context=context,
            json_structure=ExampleJson,
        )
        expected = {"name": "James Freeman", "dob": "06/16/1982"}
        self.assertDictEqual(expected, result)

    def test_that_an_assessment_criteria_can_be_given_alongside_a_document(self):
        advisor = self._get_advisor(AdvisorType.GPT_3_5)
        context = data_handler.load_medical_record_1()
        extra_context = Document(page_content="Age: 42")
        context.append(extra_context)
        criteria_dict = serialize.load_assesment_criteria(criteria_for="colonoscopy")
        criteria = (
            "Does the patient satisfy this criteria for a colonoscopy?"
            + "\n\n"
            + criteria_dict["risk-profile"]["criteria"]
        )
        result = advisor.assess_against_criteria(
            to_be_assessed=context, criteria=criteria
        )
        print(result)
        input("wait")
        # TODO: make the input better to highlight the age so that it does not need to calculate it itself - add a new section dedicated to metadata

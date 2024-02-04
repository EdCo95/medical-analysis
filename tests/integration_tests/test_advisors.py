import os
import unittest

from assess.models.advisor import (
    Advisor,
    AdvisorFactory,
    AdvisorType,
    MissingApiKeyExcepetion,
)
from tests.tools import data_handler


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

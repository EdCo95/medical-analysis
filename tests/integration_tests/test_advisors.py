import unittest

from assess.models.advisor import Advisor, AdvisorType, GPT3_5Advisor, GPT4Advisor
from tests.tools import data_handler


class AdvisorTestCase(unittest.TestCase):

    def _get_advisor(self, flavour: AdvisorType = AdvisorType.GPT_4) -> Advisor:
        if flavour == AdvisorType.GPT_4:
            return GPT4Advisor()
        elif flavour == AdvisorType.GPT_3_5:
            return GPT3_5Advisor()

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

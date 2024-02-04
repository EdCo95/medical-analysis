from tests.integration_tests.test_advisors import AdvisorTestCase

# from tests.integration_tests.test_medical_record_object import MedicalRecordTestCase

tc = AdvisorTestCase()
tc.setUp()
tc.test_that_advisors_can_answer_questions_based_on_context_and_search_results()
tc.tearDown()

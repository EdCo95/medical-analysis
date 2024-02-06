# from tests.integration_tests.test_advisors import AdvisorTestCase
# from tests.integration_tests.test_medical_record_object import MedicalRecordTestCase
from tests.integration_tests.test_orchestrator import OrchestratorTestCase

tc = OrchestratorTestCase()
tc.setUp()
tc.test_that_given_a_criteria_and_medical_record_path_it_returns_a_markdown_assesment_string()
tc.tearDown()

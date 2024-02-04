from tests.integration_tests.test_advisors import AdvisorTestCase

# from tests.integration_tests.test_medical_record_object import MedicalRecordTestCase

tc = AdvisorTestCase()
tc.setUp()
tc.test_that_an_assessment_criteria_can_be_given_alongside_a_document()
tc.tearDown()

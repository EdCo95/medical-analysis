from tests.integration_tests.test_assessor import AssessorTestCase

tc = AssessorTestCase()
tc.setUp()
tc.test_that_it_can_assess_a_medical_record_against_a_criteria()
tc.tearDown()

# from tests.integration_tests.test_advisors import AdvisorTestCase
from tests.integration_tests.test_medical_record_object import MedicalRecordTestCase

tc = MedicalRecordTestCase()
tc.setUp()
tc.test_that_it_can_present_evidence_treatment_helped()
tc.tearDown()

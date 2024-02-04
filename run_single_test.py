from tests.integration_tests.test_medical_record_object import MedicalRecordTestCase

tc = MedicalRecordTestCase()
tc.setUp()
tc.test_that_it_can_extract_the_requested_procedure_codes_record_one()
tc.tearDown()

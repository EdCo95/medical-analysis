from tests.unit_tests.test_serialize import SerializeTestCase

tc = SerializeTestCase()
tc.setUp()
tc.test_that_it_can_load_a_pdf_file()
tc.tearDown()

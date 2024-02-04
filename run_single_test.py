from tests.integration_tests.test_advisors import AdvisorTestCase

tc = AdvisorTestCase()
tc.setUp()
tc.test_that_no_api_key_raises_an_appropriate_error()
tc.tearDown()

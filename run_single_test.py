from tests.integration_tests.test_advisors import AdvisorTestCase

tc = AdvisorTestCase()
tc.setUp()
tc.test_that_the_base_advisor_class_provides_a_web_search_function()
tc.tearDown()

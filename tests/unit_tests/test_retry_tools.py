import unittest

from assess.utils import retry_tools


class RetryToolsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.counter = 0

    def _i_will_fail_twice_and_succeed_third_time(self):
        if self.counter < 2:
            self.counter += 1
            raise Exception("A generic failure")

    def test_that_it_will_retry_the_specified_number_of_times(self):
        with self.assertRaises(Exception):
            self._i_will_fail_twice_and_succeed_third_time()

        decorated = retry_tools.retry_on_failure(tolerance=3)(
            self._i_will_fail_twice_and_succeed_third_time
        )

        # If this succeeds without error, the test passes
        decorated()

# Standard lib imports
import unittest

# Third party imports
# None

# Project level imports
from ecsclient.common.util import get_formatted_time_string


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(WhenTestingCommonFunctions())
    return test_suite


class WhenTestingCommonFunctions(unittest.TestCase):

    def setUp(self):
        self.time_bucket_no_minute = '2014-11-18T00'
        self.time_bucket_with_minute = '2014-11-18T00:01'

    def test_should_get_properly_formatted_timestamp_no_minute(self):
            self.assertEqual(self.time_bucket_no_minute,
                             get_formatted_time_string(2014, 11, 18, 0, None))

    def test_should_get_properly_formatted_timestamp_with_minute(self):
            self.assertEqual(self.time_bucket_with_minute,
                             get_formatted_time_string(2014, 11, 18, 0, 1))

    def test_should_throw_value_error(self):
            self.assertRaises(ValueError,
                              get_formatted_time_string, 2014, 11, 18, 'abc')

if __name__ == '__main__':
    unittest.main()

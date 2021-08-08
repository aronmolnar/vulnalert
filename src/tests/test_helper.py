import unittest

from utils.helper import truncate_string


class TestHelper(unittest.TestCase):
    def test_truncate(self):
        maxlen = 10
        test_strings = [
            ('This is a test string', 'This is...'),
            ('Thisisateststring', 'Thisisa...'),
            ('This is a ', 'This is a ')
        ]
        for test_string in test_strings:
            self.assertEqual(truncate_string(test_string[0], maxlen=maxlen), test_string[1])

import unittest
import pep8


class TestCodeFormat(unittest.TestCase):

    def test_pep8_conformance(self):
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['monadic', 'test'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

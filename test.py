import pdfplumber
import utils
import sys
import unittest
from snapshottest import TestCase

class APITestCase(TestCase):
    def test_small(self):
        self.assertMatchSnapshot(utils.file_to_markdown("test/small.pdf"))
    def test_example(self):
        self.assertMatchSnapshot(utils.file_to_markdown("test/example.pdf"))

if __name__ == "__main__":
    unittest.main()

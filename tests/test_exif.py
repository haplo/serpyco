#!/usr/bin/env python3

from datetime import datetime
import os
import unittest

try:
    from unittest import mock
except:
    import mock

from serpyco import extract_date_from_exif
from serpyco import ExifError


TESTS_DIR = os.path.dirname(__file__)
EMPTY_EXIF_JPEG = os.path.join(TESTS_DIR, 'data', 'empty.jpg')
NOT_AN_IMAGE_FILE = os.path.join(TESTS_DIR, 'data', 'not_an_image.txt')
VALID_EXIF_JPEG = os.path.join(TESTS_DIR, 'data', 'smiley1.jpg')


class ExifTests(unittest.TestCase):

    def test_success_on_jpeg(self):
        extracted_date = extract_date_from_exif(VALID_EXIF_JPEG)
        self.assertEqual(extracted_date, datetime(2004, 7, 13, 21, 23, 44))

    def test_success_on_raw(self):
        # FIXME
        pass

    def test_error_because_no_exif_data_present(self):
        self.assertRaises(IOError,
                          extract_date_from_exif, NOT_AN_IMAGE_FILE)

    def test_error_because_empty_date(self):
        self.assertRaises(ExifError,
                          extract_date_from_exif, EMPTY_EXIF_JPEG)


if __name__ == '__main__':
    unittest.main()

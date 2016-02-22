#!/usr/bin/env python3

from datetime import datetime
import unittest

try:
    from unittest import mock
except:
    import mock

from serpyco import generate_rename_plan


class RenamePlanTests(unittest.TestCase):

    def test_files_are_sorted_by_date(self):
        files_and_dates = [
            ("file1.jpg", datetime(2013, 5, 13, 7, 32, 3)),
            ("file2.jpg", datetime(2015, 8, 20, 8, 40, 14)),
            ("file3.jpg", datetime(2012, 2, 2, 12, 45, 42)),
        ]
        rename_plan = generate_rename_plan(
            files_and_dates, "TEST_", date_as_filename=False
        )
        self.assertEqual(list(rename_plan), [
            ("file3.jpg", "./TEST_1.jpg"),
            ("file1.jpg", "./TEST_2.jpg"),
            ("file2.jpg", "./TEST_3.jpg"),
        ])

    @unittest.expectedFailure
    def test_use_same_prefix_if_files_have_same_extension(self):
        files_and_dates = [
            ("file1.jpg", datetime(2012, 2, 2, 12, 45, 42)),
            ("file2.jpg", datetime(2015, 8, 20, 8, 40, 14)),
            # files can come in any order, don"t rely on files being
            # alphabetically sorted
            ("file1.raw", datetime(2012, 2, 2, 12, 45, 42)),
            ("file2.raw", datetime(2015, 8, 20, 8, 40, 14)),
        ]
        rename_plan = generate_rename_plan(
            files_and_dates, "TEST_", date_as_filename=False
        )
        self.assertEqual(list(rename_plan), [
            ("file1.jpg", "./TEST_1.jpg"),
            ("file1.raw", "./TEST_1.raw"),
            ("file2.jpg", "./TEST_2.jpg"),
            ("file2.raw", "./TEST_2.raw"),
        ])

    def test_renaming_using_dates_without_prefix(self):
        files_and_dates = [
            ("file1.jpg", datetime(2013, 5, 13, 7, 32, 3)),
            ("file2.jpg", datetime(2015, 8, 20, 8, 40, 14)),
            ("file3.jpg", datetime(2012, 2, 2, 12, 45, 42)),
        ]
        rename_plan = generate_rename_plan(
            files_and_dates, "", date_as_filename=True
        )
        self.assertEqual(list(rename_plan), [
            ("file3.jpg", "./2012-02-02 12.45.42.jpg"),
            ("file1.jpg", "./2013-05-13 07.32.03.jpg"),
            ("file2.jpg", "./2015-08-20 08.40.14.jpg"),
        ])

    @unittest.expectedFailure
    def test_renaming_using_dates_honors_prefix(self):
        files_and_dates = [
            ("file1.jpg", datetime(2013, 5, 13, 7, 32, 3)),
            ("file2.jpg", datetime(2015, 8, 20, 8, 40, 14)),
            ("file3.jpg", datetime(2012, 2, 2, 12, 45, 42)),
        ]
        rename_plan = generate_rename_plan(
            files_and_dates, "TEST ", date_as_filename=True
        )
        self.assertEqual(list(rename_plan), [
            ("file3.jpg", "./TEST 2012-02-02 12.45.42.jpg"),
            ("file1.jpg", "./TEST 2013-05-13 07.32.03.jpg"),
            ("file2.jpg", "./TEST 2015-08-20 08.40.14.jpg"),
        ])

    def test_error_if_a_date_is_not_provided_for_a_file(self):
        # fixme: code is not checking for datetimes
        files_and_dates = [
            ("file1.jpg", datetime(2013, 5, 13, 7, 32, 3)),
            ("file2.jpg", ),
            ("file3.jpg", datetime(2012, 2, 2, 12, 45, 42)),
        ]
        rename_plan = generate_rename_plan(
            files_and_dates, "TEST_", date_as_filename=False
        )


if __name__ == "__main__":
    unittest.main()

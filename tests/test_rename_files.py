#!/usr/bin/env python3

import unittest

try:
    from unittest import mock
except:
    import mock

from serpyco import rename_files


class RenameFilesTests(unittest.TestCase):

    @mock.patch('os.rename')
    def test_files_are_renamed_if_dry_run_is_false(self, mock_rename):
        rename_files([['file1.jpg', 'newfile1.jpg']], dry_run=False)
        mock_rename.assert_called_with('file1.jpg', 'newfile1.jpg')

    @mock.patch('os.rename')
    def test_files_are_not_renamed_if_dry_run_is_true(self, mock_rename):
        rename_files([['file1.jpg', 'newfile1.jpg']], dry_run=True)
        mock_rename.assert_not_called()


if __name__ == '__main__':
    unittest.main()

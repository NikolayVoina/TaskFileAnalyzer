import os
import unittest
from unittest.mock import patch

from task_analyzer import process_file

class TestProcessFile(unittest.TestCase):
    """
    Unit tests for the `process_file` function from the `task_analyzer` module.

    This class tests the `process_file` function, which processes files by extracting
    information such as file size, category (e.g., text or image), file permissions,
    and identifying unusual permissions.
    """

    @patch("os.stat")
    @patch("os.path.splitext")
    def test_process_file(self, mock_splitext, mock_stat):
        """
        Test the normal behavior of the `process_file` function.

        This test checks how the `process_file` function handles a file with normal parameters:
        correctly extracting the file size, category, permissions, and detecting unusual permissions.
        """

        # Mock the behavior of os.path.splitext to return a specific file extension
        mock_splitext.return_value = ("filename", ".txt")

        # Mock the behavior of os.stat to return the file size and permissions
        mock_stat.return_value.st_size = 1024
        mock_stat.return_value.st_mode = 0o766

        file_path = "/path/to/file.txt"  # Path to the test file

        # Call the `process_file` function
        file_path, size, category, permissions, unusual_permissions = process_file(file_path)

        # Check the results
        self.assertEqual(file_path, "/path/to/file.txt")
        self.assertEqual(size, 1024)
        self.assertEqual(category, "text")
        self.assertEqual(permissions, "0o766")
        self.assertEqual(len(unusual_permissions), 1)

    @patch("os.stat")
    def test_process_file_error(self, mock_stat):
        """
        Test error handling in the `process_file` function.

        This test checks how the `process_file` function handles errors, such as when the
        file does not exist (OSError).
        """

        # Mock an error when trying to get file information
        mock_stat.side_effect = OSError(2, "No such file or directory")

        file_path = "/path/to/non_existent_file.txt"  # Path to a non-existent file

        # Call the `process_file` function, expecting it to handle the error
        file_path, size, category, permission, unusual_permissions = process_file(file_path)

        # Check the results when an error occurs
        self.assertEqual(file_path, "/path/to/non_existent_file.txt")
        self.assertEqual(size, 0)
        self.assertEqual(category, "unknown")
        self.assertEqual(permission, "")
        self.assertEqual(len(unusual_permissions), 0)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from task_analyzer import handle_os_error


class TestHandleOSError(unittest.TestCase):
    """    Test for handle_os_error function. This test verifies if errors related to file access
           (file not found, permission denied, and unexpected errors) are handled and logged correctly
    """

    @patch('logging.error')
    def test_handle_os_error_file_not_exist(self, mock_logging_error) -> None:

        """Test case to check if 'File not found' errors are logged correctly"""
        mock_error = MagicMock()
        mock_error.errno = 2
        mock_error.strerror = "No such file or directory"
        file_path = "/path/to/nonexistent/file"

        # Calling the function to handle the error
        handle_os_error(mock_error, file_path)

        # Verifying that the correct error message is logged
        mock_logging_error.assert_called_with(f"Error: File or directory does not exist: {file_path}")

    @patch('logging.error')
    def test_handle_os_error_permission_denied(self, mock_logging_error) -> None:
        """
        Test case to check if 'Permission denied' errors are logged correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 13
        mock_error.strerror = "Permission denied"
        file_path = "/home/mikalai/test_dir/permissions.txt"

        handle_os_error(mock_error, file_path)

        # Verifying that the correct error message is logged
        mock_logging_error.assert_called_with(f"Error: Permission denied for file: {file_path}")

    @patch('logging.error')
    def test_handle_os_error_unexpected_error(self, mock_logging_error) -> None:
        """
        Test case to check if unexpected errors are logged correctly with their error code.
        """
        mock_error = MagicMock()
        mock_error.errno = 999
        mock_error.strerror = "Unexpected error"
        file_path = "/home/mikalai/test_dir/permissions.txt"

        handle_os_error(mock_error, file_path)

        # Verifying that the unexpected error is logged correctly
        mock_logging_error.assert_called_with(f"Unexpected error (999) with file {file_path}: Unexpected error")


if __name__ == '__main__':
    unittest.main()

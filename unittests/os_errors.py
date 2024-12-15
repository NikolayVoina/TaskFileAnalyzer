import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from task_analyzer import handle_os_error

class TestHandleOSError(unittest.TestCase):
    """
    Test the handle_os_error function. This test verifies that different OSError codes are handled
    correctly and that appropriate messages are printed when errors such as file not found, permission
    denied, and other unexpected errors occur.
    """

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_file_not_exist(self, mock_stdout) -> None:
        """
        Test case to check if 'File not found' errors (errno 2) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 2
        mock_error.strerror = "No such file or directory"
        file_path = "/path/to/nonexistent/file"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: File or directory does not exist: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_permission_denied(self, mock_stdout) -> None:
        """
        Test case to check if 'Permission denied' errors (errno 13) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 13
        mock_error.strerror = "Permission denied"
        file_path = "/home/mikalai/test_dir/permissions.txt"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: Permission denied for file: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_bad_file_number(self, mock_stdout) -> None:
        """
        Test case to check if 'Bad file number' errors (errno 9) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 9
        mock_error.strerror = "Bad file descriptor"
        file_path = "/path/to/file"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: Bad file number for file: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_is_directory(self, mock_stdout) -> None:
        """
        Test case to check if 'Trying to open a directory as a file' errors (errno 21) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 21
        mock_error.strerror = "Is a directory"
        file_path = "/path/to/directory"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: Trying to open a directory as a file: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_not_a_directory(self, mock_stdout) -> None:
        """
        Test case to check if 'Not a directory' errors (errno 20) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 20
        mock_error.strerror = "Not a directory"
        file_path = "/path/to/non-directory"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: Not a directory: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_not_a_terminal_device(self, mock_stdout) -> None:
        """
        Test case to check if 'Not a terminal device' errors (errno 25) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 25
        mock_error.strerror = "Not a typewriter"
        file_path = "/path/to/terminal/device"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: Not a terminal device: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_no_such_process(self, mock_stdout) -> None:
        """
        Test case to check if 'No such process' errors (errno 3) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 3
        mock_error.strerror = "No such process"
        file_path = "/path/to/process"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: No such process while accessing: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_io_error(self, mock_stdout) -> None:
        """
        Test case to check if 'I/O error' errors (errno 5) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 5
        mock_error.strerror = "I/O error"
        file_path = "/path/to/io_error/file"

        handle_os_error(mock_error, file_path)

        expected_message = f"Error: I/O error while accessing file: {file_path}"
        self.assertIn(expected_message, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_os_error_unexpected_error(self, mock_stdout) -> None:
        """
        Test case to check if unexpected errors (non-standard errno) are handled and printed correctly.
        """
        mock_error = MagicMock()
        mock_error.errno = 999  # Unknown errno
        mock_error.strerror = "Unexpected error"
        file_path = "/home/mikalai/test_dir/permissions.txt"

        handle_os_error(mock_error, file_path)

        expected_message = f"Unexpected error (999) with file {file_path}: Unexpected error"
        self.assertIn(expected_message, mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()

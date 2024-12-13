import unittest
from collections import defaultdict
from unittest.mock import patch, MagicMock
from task_analyzer import process_file


class TestProcessFile(unittest.TestCase):
    """
    Test for the process_file function. This test checks whether the file is correctly processed,
    categorized, and whether its size and permissions are recorded accurately.
    """

    @patch("os.stat")
    def test_process_file(self, mock_stat) -> None:
        """
        Test case for checking file categorization, size calculation, and permission checks.
        """

        # Mocking os.stat to return fake file information
        mock_stat.return_value = MagicMock(st_size=1500, st_mode=0o777)

        file = "testfile.txt"
        root = "/path/to"
        size_threshold = 1000
        categorized_files = defaultdict(list)
        total_sizes = defaultdict(int)
        unusual_permissions = []
        large_files = []

        # Calling the function to process the file
        process_file(file, root, size_threshold, categorized_files, total_sizes, unusual_permissions, large_files)

        # Checking file categorization
        self.assertIn("text", categorized_files)
        self.assertEqual(len(categorized_files["text"]), 1)

        self.assertEqual(total_sizes["text"], 1500)

        self.assertIn(("/path/to/testfile.txt", "777"), unusual_permissions)

        # Checking if the file is considered large
        self.assertEqual(len(large_files), 1)


if __name__ == "__main__":
    unittest.main()

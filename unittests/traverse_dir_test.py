import os
import unittest
from unittest.mock import patch

from task_analyzer import traverse_directory_mp


class TestTraverseDirectoryMP(unittest.TestCase):


    @patch("os.walk")
    @patch("multiprocessing.Pool")
    @patch("os.stat")  # Mock os.stat as well to avoid accessing real files
    def test_traverse_directory_mp(self, mock_stat, mock_pool, mock_walk):

        # Mock os.walk to simulate directory structure
        mock_walk.return_value = [
            ("/test/dir", [], ["file1.txt", "file2.jpg"]),
        ]

        # Mock os.stat to return mock file size and permissions
        mock_stat.return_value.st_size = 1024  # Mocking file size for both files
        mock_stat.return_value.st_mode = 0o755  # Simulating file permissions

        # Mock Pool instance and its map method
        mock_pool_instance = mock_pool.return_value
        mock_pool_instance.map.return_value = [
            ("/test/dir/file1.txt", 1024, "text", "755", []),
            ("/test/dir/file2.jpg", 1024, "image", "644", []),
        ]

        directory = "/test/dir"
        size_threshold = 1025
        categorized_files, total_sizes, unusual_permissions, large_files = traverse_directory_mp(directory,
                                                                                                 size_threshold)

        # Assertions for the categorized files
        self.assertEqual(len(categorized_files["text"]), 1)
        self.assertEqual(categorized_files["text"][0], ("/test/dir/file1.txt", 1024))

        self.assertEqual(len(categorized_files["image"]), 1)
        self.assertEqual(categorized_files["image"][0], ("/test/dir/file2.jpg", 1024))

        # Assertions for total sizes
        self.assertEqual(total_sizes["text"], 1024)
        self.assertEqual(total_sizes["image"], 1024)

        # Assertions for unusual permissions and large files
        self.assertEqual(len(unusual_permissions), 0)  # No unusual permissions because permissions are standard
        self.assertEqual(len(large_files), 0)  # No large files because both are below threshold



if __name__ == '__main__':
    unittest.main()

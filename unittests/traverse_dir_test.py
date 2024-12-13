import unittest
from unittest.mock import patch, MagicMock

from task_analyzer import traverse_directory


class TestFileSystemAnalysis(unittest.TestCase):
    """
    Test for traverse_directory function. This test checks if files are correctly categorized, large files
    are identified, and unusual permissions are flagged correctly.
    """
    @patch('os.walk')  # Mocking os.walk to simulate file structure
    @patch('os.stat')  # Mocking os.stat to simulate file statistics (like size and permissions)
    def test_traverse_directory(self, mock_stat: MagicMock, mock_walk: MagicMock) -> None:
        mock_walk.return_value = [
            ('/test_dir', ('subdir1',), ('file1.txt', 'file2.txt')),
            ('/test_dir/subdir1', (), ('file3.txt',)),
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=5000, st_mode=0o755),  # file1.txt (normal permissions)
            MagicMock(st_size=10001, st_mode=0o777),  # file2.txt (unusual permissions)
            MagicMock(st_size=20000, st_mode=0o000),
        ]


        directory = '/test_dir'
        size_threshold = 10000

        categorized_files, total_sizes, unusual_permissions, large_files = traverse_directory(directory, size_threshold)

        print(unusual_permissions)
        #print(large_files)

        """Assert that files were correctly categorized as 'text' files"""
        self.assertIn('text', categorized_files)
        self.assertEqual(len(categorized_files['text']), 3)

        """Assert total size for 'text' category is correct"""
        self.assertEqual(total_sizes['text'], 35001)

        """Assert that there are two large files"""
        self.assertEqual(len(large_files), 2)  # file2.txt and file3.txt are large files

        """Assert that there are two files with unusual permissions"""
        self.assertEqual(len(unusual_permissions), 2)
        self.assertIn(('/test_dir/file2.txt', '777'), unusual_permissions)


if __name__ == '__main__':
    unittest.main()

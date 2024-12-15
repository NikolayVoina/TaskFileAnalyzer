import os
import unittest
from task_analyzer import get_file_category

class TestFileCategorization(unittest.TestCase):
    """
    Test for get_file_category function. This test checks if files are correctly categorized
    based on their extensions.
    """

    """Test cases to verify that get_file_category categorizes files correctly based on their extensions."""
    def test_get_file_category(self) -> None:
        # Testing categorization of different file types
        self.assertEqual(get_file_category("document.txt", "/home/mikalai/test_dir/subdir2/document.txt"), "text")
        self.assertEqual(get_file_category("image.jpg", "/home/mikalai/test_dir/subdir2/image.jpg"), "image")
        self.assertEqual(get_file_category("script.sh", "/home/mikalai/test_dir/subdir2/script.sh"), "executable")
        self.assertEqual(get_file_category("movie.mp4", "/home/mikalai/test_dir/subdir2/movie.mp4"), "video")
        self.assertEqual(get_file_category("audio.mp3", "/home/mikalai/test_dir/subdir2/audio.mp3"), "audio")
        self.assertEqual(get_file_category("archive.zip", "/home/mikalai/test_dir/subdir2/archive.zip"), "archive")
        self.assertEqual(get_file_category("unknown.xyz", "/home/mikalai/test_dir/subdir2/unknown.xyz"), "other")

if __name__ == "__main__":
    unittest.main()

import os
import stat
from collections import defaultdict
from typing import Dict, List, Tuple, AnyStr
import logging
import concurrent.futures
import threading


"""Logging settings"""
logging.basicConfig(
    filename='error_log.txt',
    level=logging.ERROR,
    format='%(asctime)s - %(message)s',
    filemode='w'
)


FILE_CATEGORIES: Dict[str, List[str]] = {
    "text": [".txt", ".log", ".md", ".csv"],
    "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "executable": [".sh", ".exe", ".bin", ".run"],
    "video": [".mp4", ".mkv", ".avi", ".mov"],
    "audio": [".mp3", ".wav", ".ogg", ".flac"],
    "archive": [".zip", ".tar", ".gz", ".bz2", ".7z"],
}

default_size_treshold = 104857600  # 100 MB
unknown_ext: defaultdict[str, List[str]] = defaultdict(list)


"""Semaphore for limiting concurrent threads"""
semaphore = threading.Semaphore(10)


"""Sort files by size in descending order"""
def quick_sort(files: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    if len(files) <= 1:
        return files
    pivot = files[0]
    smaller = [x for x in files[1:] if x[1] <= pivot[1]]
    larger = [x for x in files[1:] if x[1] > pivot[1]]
    return quick_sort(larger) + [pivot] + quick_sort(smaller)


"""Determine the category of a file based on its extension """
def get_file_category(filename: str, file_path: str) -> str:
    _, ext = os.path.splitext(filename)
    for category, extensions in FILE_CATEGORIES.items():
        if ext.lower() in extensions:
            return category
    unknown_ext[ext.lower()].append(file_path)
    return "other"


"""Handle specific OSError and print appropriate messages"""
def handle_os_error(e: OSError, file_path: str):
    error_messages = {
        2: f"Error: File or directory does not exist: {file_path}",  # ENOENT (No such file or directory)
        13: f"Error: Permission denied for file: {file_path}", # EACCES (Permission denied)
        9: f"Error: Bad file number for file: {file_path}", # EBADF (Bad file number)
        21: f"Error: Trying to open a directory as a file: {file_path}", # EISDIR (Is a directory)
        24: f"Error: Too many open files for file: {file_path}", # EMFILE (Too many open files)
        20: f"Error: Not a directory: {file_path}", # ENOTDIR (Not a directory)
        25: f"Error: Not a terminal device: {file_path}", # ENOTTY (Not a typewriter)
        3: f"Error: No such process while accessing: {file_path}", # ESRCH (No such process)
        5: f"Error: I/O error while accessing file: {file_path}", # EIO (I/O error)
    }

    # Default error message for unknown error codes
    message = error_messages.get(e.errno, f"Unexpected error ({e.errno}) with file {file_path}: {e.strerror}")
    print(message)
    logging.error(message)


"""Helper function for processing each file with semaphore to limit parallelism"""
def process_file(file: str, root: str, size_threshold: int, categorized_files, total_sizes, unusual_permissions, large_files):
    with semaphore:
        try:
            file_path = os.path.join(root, file)
            stat_info = os.stat(file_path)
            size = stat_info.st_size
            category = get_file_category(file, file_path)

            categorized_files[category].append((file_path, size))
            total_sizes[category] += size

            # Check for unusual file permissions
            if stat_info.st_mode & (stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH):
                unusual_permissions.append((file_path, oct(stat_info.st_mode)[-3:]))

            # Check for large files
            if size > size_threshold:
                large_files.append((file_path, size))

        except OSError as e:
            handle_os_error(e, file_path)


"""Traverse the directory and categorize files"""
def traverse_directory(directory: str, size_threshold: int) -> Tuple[Dict[str, List[Tuple[str, int]]], Dict[str, int], List[Tuple[str, str]], List[Tuple[str, int]]]:
    categorized_files: defaultdict[str, List[Tuple[str, int]]] = defaultdict(list)
    total_sizes: defaultdict[str, int] = defaultdict(int)
    unusual_permissions: List[Tuple[str, str]] = []
    large_files: List[Tuple[str, int]] = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk(directory):
            for file in files:
                futures.append(executor.submit(process_file, file, root, size_threshold, categorized_files, total_sizes, unusual_permissions, large_files))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

    for category in categorized_files:
        categorized_files[category] = quick_sort(categorized_files[category])

    return categorized_files, total_sizes, unusual_permissions, large_files


"""Display the categorized files, unusual permissions, and large files"""
def display_results(categorized_files: Dict[str, List[Tuple[str, int]]], total_sizes: Dict[str, int],
                    unusual_permissions: List[Tuple[str, str]], large_files: List[Tuple[str, int]]):
    print("\nFile Type Categorization")
    print("=" * 50)
    for category, files in categorized_files.items():
        print(f"{category.capitalize()} ({len(files)} files): {total_sizes[category]} bytes")

    print("\nFiles with Unusual Permissions")
    print("=" * 50)
    for i, (file, permissions) in enumerate(unusual_permissions, 1):
        print(f"{i}. {file} (Permissions: {permissions})")

    print("\nLarge Files")
    print("=" * 50)
    for i, (file, size) in enumerate(large_files, 1):
        print(f"{i}. {file} ({size} bytes)")

    print("\nOther Extension: ")
    print("=" * 50)
    if unknown_ext:
        print("Other extensions found:", end="")
        for ext, files in unknown_ext.items():
            print(f"\nExtension: {ext}")
            for file in files:
                print(f"  - {file}")


"""Prompt the user for valid input (directory and size threshold)"""
def get_valid_input() -> Tuple[str, int]:
    while True:
        try:
            directory = input("Enter the directory to analyze: ").strip()

            if directory == "1":
                exit(0)

            if not os.path.isdir(directory):
                raise ValueError("Directory does not exist.")

            size_threshold = input(
                f"Enter size threshold for large files (in bytes, default {default_size_treshold}): ").strip()

            size_threshold = int(size_threshold) if size_threshold else default_size_treshold
            return directory, size_threshold

        except ValueError as e:
            print(f"Error: {e}. Please try again.")


if __name__ == "__main__":
    while True:
        print("If u want exit press '1'")
        directory, size_threshold = get_valid_input()
        print("Analyzing directory...")
        categorized_files, total_sizes, unusual_permissions, large_files = traverse_directory(directory, size_threshold)
        display_results(categorized_files, total_sizes, unusual_permissions, large_files)
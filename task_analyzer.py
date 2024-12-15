import os
import stat
import time
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Tuple, AnyStr

FILE_CATEGORIES: Dict[str, List[str]] = {
    "text": [".txt", ".log", ".md", ".csv"],
    "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "executable": [".sh", ".exe", ".bin", ".run"],
    "video": [".mp4", ".mkv", ".avi", ".mov"],
    "audio": [".mp3", ".wav", ".ogg", ".flac"],
    "archive": [".zip", ".tar", ".gz", ".bz2", ".7z"],
}

NORMAL_PERMISSIONS = [0o755, 0o644, 0o700, 0o744]

default_size_threshold = 104857600  # 100 MB
unknown_ext: defaultdict[str, List[str]] = defaultdict(list)


def check_permissions(file_path: str) -> List[Tuple[str, str]]:
    """
    Check the file permissions and compare them with the standard ones.
    Return a list of files with unusual permissions.

    Args:
        file_path (str): Path to the file.

    Returns:
        List[Tuple[str, str]]: A list of tuples with file path and its unusual permissions.
    """
    unusual_permissions = []
    try:
        file_permissions = oct(os.stat(file_path).st_mode & 0o777)  # Getting file permission in octal form
        if int(file_permissions, 8) not in NORMAL_PERMISSIONS:  # Checking permissions in normal permission list
            unusual_permissions.append((file_path, file_permissions))
    except OSError as e:
        handle_os_error(e, file_path)
    return unusual_permissions


def handle_os_error(e: OSError, file_path: str):
    """
    Handle OSError based on its error code and print a detailed error message.

    Args:
        e (OSError): The OSError exception.
        file_path (str): Path to the file where the error occurred.
    """
    error_messages = {
        2: f"Error: File or directory does not exist: {file_path}",  # ENOENT (No such file or directory)
        13: f"Error: Permission denied for file: {file_path}",  # EACCES (Permission denied)
        9: f"Error: Bad file number for file: {file_path}",  # EBADF (Bad file number)
        21: f"Error: Trying to open a directory as a file: {file_path}",  # EISDIR (Is a directory)
        20: f"Error: Not a directory: {file_path}",  # ENOTDIR (Not a directory)
        25: f"Error: Not a terminal device: {file_path}",  # ENOTTY (Not a typewriter)
        3: f"Error: No such process while accessing: {file_path}",  # ESRCH (No such process)
        5: f"Error: I/O error while accessing file: {file_path}",  # EIO (I/O error)
    }

    # Default error message for unknown error codes
    message = error_messages.get(e.errno, f"Unexpected error ({e.errno}) with file {file_path}: {e.strerror}")
    print(message)


def quick_sort(files: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """
    Quick sort implementation to sort files by their size in descending order.

    Args:
        files (List[Tuple[str, int]]): List of files and their sizes to be sorted.

    Returns:
        List[Tuple[str, int]]: Sorted list of files by size.
    """
    if len(files) <= 1:
        return files
    pivot = files[0]
    smaller = [x for x in files[1:] if x[1] <= pivot[1]]
    larger = [x for x in files[1:] if x[1] > pivot[1]]
    return quick_sort(larger) + [pivot] + quick_sort(smaller)


def get_file_category(filename: str, file_path: str) -> str:
    """
    Get the category of the file based on its extension.
    If the extension is not recognized, classify it as 'other'.

    Args:
        filename (str): The name of the file.
        file_path (str): The path to the file.

    Returns:
        str: The category of the file.
    """
    _, ext = os.path.splitext(filename)
    for category, extensions in FILE_CATEGORIES.items():
        if ext.lower() in extensions:
            return category
    unknown_ext[ext.lower()].append(file_path)
    return "other"


def process_file(file_path: str) -> Tuple[str, int, str, str, List[Tuple[str, str]]]:
    """
    Process a single file: calculate its size, determine its category,
    check its permissions, and identify any unusual permissions.

    Args:
        file_path (str): The path to the file.

    Returns:
        Tuple[str, int, str, str, List[Tuple[str, str]]]: A tuple with file path, size, category, permissions,
        and unusual permissions.
    """
    try:
        size = os.path.getsize(file_path)
        category = get_file_category(file_path, file_path)
        file_permissions = os.stat(file_path).st_mode & 0o777
        unusual_permissions = check_permissions(file_path)
        return file_path, size, category, oct(file_permissions), unusual_permissions
    except OSError as e:
        handle_os_error(e, file_path)
        return file_path, 0, "unknown", "", []


def traverse_directory_mp(directory: str, size_threshold: int):
    """
    Traverse the directory and analyze its files in parallel using multiple processes.
    Categorize files, check for unusual permissions, and identify large files.

    Args:
        directory (str): The directory to traverse.
        size_threshold (int): The size threshold for large files.

    Returns:
        Tuple: A tuple containing categorized files, total sizes, unusual permissions, and large files.
    """
    categorized_files: defaultdict[str, List[Tuple[str, int]]] = defaultdict(list)
    total_sizes: defaultdict[str, int] = defaultdict(int)
    unusual_permissions: List[Tuple[str, str]] = []
    large_files: List[Tuple[str, int]] = []

    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_file, files)

    for file_path, size, category, permissions, unusual_perms in results:
        if size is not None:
            categorized_files[category].append((file_path, size))
            total_sizes[category] += size

            if size > size_threshold:
                large_files.append((file_path, size))

            unusual_permissions.extend(unusual_perms)

    for category in categorized_files:
        categorized_files[category] = quick_sort(categorized_files[category])

    return categorized_files, total_sizes, unusual_permissions, large_files


def display_results(categorized_files: Dict[str, List[Tuple[str, int]]], total_sizes: Dict[str, int],
                    unusual_permissions: List[Tuple[str, str]], large_files: List[Tuple[str, int]]):
    """
    Display the categorized files, files with unusual permissions,
    and files that exceed the size threshold.

    Args:
        categorized_files (Dict[str, List[Tuple[str, int]]]): Categorized files and their sizes.
        total_sizes (Dict[str, int]): Total size of files in each category.
        unusual_permissions (List[Tuple[str, str]]): List of files with unusual permissions.
        large_files (List[Tuple[str, int]]): List of large files exceeding the size threshold.
    """
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

    print("\nOther Extensions:")
    print("=" * 50)
    if unknown_ext:
        for ext, files in unknown_ext.items():
            print(f"Extension: {ext}")
            for file in files:
                print(f"  - {file}")


def get_valid_input() -> Tuple[str, int]:
    """
    Prompt the user to enter a valid directory path and file size threshold.
    If invalid input is provided, the function will keep prompting the user.

    Returns:
        Tuple[str, int]: The directory path and the size threshold.
    """
    while True:
        try:
            directory = input("Enter the directory to analyze: ").strip()

            if not os.path.isdir(directory):
                raise ValueError("Directory does not exist.")

            size_threshold = input(
                "Enter the size threshold for large files in bytes (default 100 MB): ").strip()

            if not size_threshold:
                size_threshold = default_size_threshold
            else:
                size_threshold = int(size_threshold)

            return directory, size_threshold
        except (ValueError, FileNotFoundError) as e:
            print(f"Invalid input: {e}. Please try again.")


if __name__ == "__main__":
    while True:
        start_time: time = time.time()
        print("If you want to exit, press '1'")
        directory, size_threshold = get_valid_input()
        print("Analyzing directory...")
        categorized_files, total_sizes, unusual_permissions, large_files = traverse_directory_mp(directory, size_threshold)
        display_results(categorized_files, total_sizes, unusual_permissions, large_files)
        finish_time: time = time.time()
        print("This iteration took", finish_time - start_time)
        print("*" * 50)

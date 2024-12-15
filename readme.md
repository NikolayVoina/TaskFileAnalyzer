# File System Analyzer

A command-line tool for analyzing file system structure and usage.

---

## Features

- **Directory Traversal**: Recursively lists all files and directories.
- **File Type Categorization**: Classifies files based on their types (e.g., text, image, etc.).
- **Size Analysis**: Provides insights into file sizes and disk usage.
- **File Permissions Report**: Identifies files with unusual permissions (write/execute).
- **Large Files Identification**: Detects files above a specified size threshold.
- **Multithreading Support**: Speeds up directory traversal by using multiple threads.

---

## Requirements

- Python => 3.9
- Standard Python libraries: `time`, `multiprocessing`, `os`, `stat`, `typing`, `collections`, `unittest`

---

## Libraries Used

This project uses the following libraries:

- **time**: Provides various time-related functions, such as measuring the duration of operations (`time.time()`), pausing execution for a specified interval (`time.sleep()`), and formatting time into human-readable strings (`time.strftime()`).

- **multiprocessing**: Enables the creation of multiple processes, allowing parallel execution to take full advantage of multiple CPU cores. This module provides support for process-based concurrency, with tools like `Pool`, `Process`, and `Queue` for inter-process communication.

- **os**: Provides a way to interact with the operating system, including file and directory manipulation (`os.rename()`, `os.remove()`, `os.makedirs()`), environment variable management (`os.getenv()`, `os.environ`), and system-related operations (`os.system()`).

- **stat**: Provides constants and functions to retrieve file status information, such as file permissions, ownership, size, and modification times. This module is used to analyze file properties using `os.stat()`.

- **typing**: Introduces type hints and annotations, helping to specify expected types for variables, function arguments, and return values. It enhances code readability and helps with static type checking, making large codebases easier to maintain.

- **collections**: Offers specialized container datatypes, such as `namedtuple` (a lightweight object type), `deque` (a double-ended queue for fast append and pop operations), `Counter` (a dictionary subclass for counting hashable objects), and `defaultdict` (a dictionary with default values).

- **unittest**: A framework for writing and running unit tests in Python. It provides a way to organize tests, check expected results with assertions, and automate the testing process. Key features include `TestCase` for grouping tests, `assert` methods for verifying correctness, and test runners like `unittest.main()` for executing tests.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/NikolayVoina/TaskFileAnalyzer.git
    ```

2. Navigate to the project directory:

    ```bash
    cd file-system-analyzer
    ```
3. Run analyzer:

   ```bash
   python file_system_analyzer.py
   ```
---

## Test Cases 

   **Test case 1 Run the tool and ensure it categorizes the files and calculates their sizes correctly.**
      
      Enter the directory to analyze: /home/mikalai/TaskFileAnalyzer/test_case_1
      Enter size threshold for large files (in bytes, default 104857600): 
      Analyzing directory...
      
      File Type Categorization
      ==================================================
      Text (1 files): 27 bytes
      Image (2 files): 3145728 bytes
      
      Files with Unusual Permissions
      ==================================================
         1. /home/mikalai/TaskFileAnalyzer/test_case_1/file2.txt (Permissions: 664)
         2. /home/mikalai/TaskFileAnalyzer/test_case_1/image2.png (Permissions: 664)
         3. /home/mikalai/TaskFileAnalyzer/test_case_1/image1.png (Permissions: 664)
      
      Large Files
      ==================================================
      
      Other Extension: 
      ==================================================
      If u want exit press '1'
      Enter the directory to analyze:

   **Test case 2 Verify that the tool correctly identifies and lists files above the threshold.**

         Enter the directory to analyze: /home/mikalai/TaskFileAnalyzer/test_case_2
         Enter size threshold for large files (in bytes, default 104857600): 2
         Analyzing directory...
         
         File Type Categorization
         ==================================================
         Text (3 files): 116391936 bytes
         
         Files with Unusual Permissions
         ==================================================
         1. /home/mikalai/TaskFileAnalyzer/test_case_2/file_1MB.txt (Permissions: 664)
         2. /home/mikalai/TaskFileAnalyzer/test_case_2/file_10MB.txt (Permissions: 664)
         3. /home/mikalai/TaskFileAnalyzer/test_case_2/file_100MB.txt (Permissions: 664)
         
         Large Files
         ==================================================
         1. /home/mikalai/TaskFileAnalyzer/test_case_2/file_1MB.txt (1048576 bytes)
         2. /home/mikalai/TaskFileAnalyzer/test_case_2/file_10MB.txt (10485760 bytes)
         3. /home/mikalai/TaskFileAnalyzer/test_case_2/file_100MB.txt (104857600 bytes)
         
         Other Extension: 
         ==================================================
   
   **Test Case 3 Run the tool and verify that files with permissions that allow write/execute access for others are identified.**

         Enter the directory to analyze: /home/mikalai/TaskFileAnalyzer/test_case_3
         Enter size threshold for large files (in bytes, default 104857600): 
         Analyzing directory...
         
         File Type Categorization
         ==================================================
         Text (1 files): 31 bytes
         
         Files with Unusual Permissions
         ==================================================
         1. /home/mikalai/TaskFileAnalyzer/test_case_3/file_with_permissions.txt (Permissions: 777)
         
         Large Files
         ==================================================
         
         Other Extension: 
         ==================================================
---


## License

**MIT License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
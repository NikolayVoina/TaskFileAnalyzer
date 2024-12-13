#!/bin/bash
mkdir -p test_case_1

echo "Another text file content." > test_case_1/file2.txt
dd if=/dev/urandom of=test_case_1/image1.png bs=1M count=1 &> /dev/null  # Create a 1MB PNG file
dd if=/dev/urandom of=test_case_1/image2.png bs=1M count=2 &> /dev/null  # Create a 2MB PNG file

python3 your_tool.py --directory test_case_1




mkdir -p test_case_2

dd if=/dev/urandom of=test_case_2/file_1MB.txt bs=1M count=1 &> /dev/null
dd if=/dev/urandom of=test_case_2/file_10MB.txt bs=10M count=1 &> /dev/null
dd if=/dev/urandom of=test_case_2/file_100MB.txt bs=100M count=1 &> /dev/null





mkdir -p test_case_3

echo "File with special permissions." > test_case_3/file_with_permissions.txt

chmod 777 test_case_3/file_with_permissions.txt



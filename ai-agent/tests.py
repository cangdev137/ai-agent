from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import * 
from functions.run_python_file import *

test_cases = [
        ("calculator", "main.py"), 
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
        ("calculator", "nonexistent.py")
]

for args in test_cases:
    result =  run_python_file(*args)
    print(f"{result}\n{'-'*100}")


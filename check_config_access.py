import pathlib
import os
import sys

# This script checks if pyproject.toml is accessible from the current working directory.

print(f"Python executable being used (sys.executable): {sys.executable}")

# Get the current working directory as Python sees it
python_cwd = os.getcwd()
print(f"Python's current working directory (os.getcwd()): {python_cwd}")

# Define relative and absolute paths to pyproject.toml
# Relative path is now relative to python_cwd
file_path_relative_to_python_cwd = "pyproject.toml"
file_path_absolute = pathlib.Path(python_cwd) / file_path_relative_to_python_cwd

print(f"Checking for pyproject.toml at relative path (to Python's CWD): '{file_path_relative_to_python_cwd}'")
print(f"Checking for pyproject.toml at absolute path: '{file_path_absolute}'")

# Check existence and type using pathlib
exists_relative = pathlib.Path(file_path_relative_to_python_cwd).exists() # This will be relative to python's CWD
is_file_relative = pathlib.Path(file_path_relative_to_python_cwd).is_file()
exists_absolute = file_path_absolute.exists()
is_file_absolute = file_path_absolute.is_file()

print(f"Using pathlib.Path('{file_path_relative_to_python_cwd}').exists() (relative to Python's CWD): {exists_relative}")
print(f"Using pathlib.Path('{file_path_relative_to_python_cwd}').is_file() (relative to Python's CWD): {is_file_relative}")
print(f"Using pathlib.Path('{file_path_absolute}').exists(): {exists_absolute}")
print(f"Using pathlib.Path('{file_path_absolute}').is_file(): {is_file_absolute}")

# Attempt to open and read the file
if file_path_absolute.is_file():
    try:
        with open(file_path_absolute, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            print(f"Successfully opened '{file_path_absolute}' and read the first line: \"{first_line}\"")
    except Exception as e:
        print(f"Error attempting to open/read '{file_path_absolute}': {e}")
elif exists_absolute:
    print(f"'{file_path_absolute}' exists but is not a file (it's a directory or other type).")
else:
    print(f"'{file_path_absolute}' does not exist or is not accessible based on Python's CWD.")

# Forcing a check from a hardcoded expected CWD if different
expected_cwd = r"C:\Users\Owner\OneDrive\01.Projects\58_Cursor_Projects\05_Browser_Use"
if python_cwd.lower() != expected_cwd.lower():
    print(f"\nPython's CWD ('{python_cwd}') is different from expected CWD ('{expected_cwd}').")
    print(f"Retrying checks assuming files are relative to expected CWD:")
    hardcoded_path_to_pyproject = pathlib.Path(expected_cwd) / "pyproject.toml"
    print(f"Checking for pyproject.toml at hardcoded absolute path: '{hardcoded_path_to_pyproject}'")
    exists_hardcoded = hardcoded_path_to_pyproject.exists()
    is_file_hardcoded = hardcoded_path_to_pyproject.is_file()
    print(f"Using pathlib.Path('{hardcoded_path_to_pyproject}').exists(): {exists_hardcoded}")
    print(f"Using pathlib.Path('{hardcoded_path_to_pyproject}').is_file(): {is_file_hardcoded}")
    if is_file_hardcoded:
        try:
            with open(hardcoded_path_to_pyproject, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                print(f"Successfully opened '{hardcoded_path_to_pyproject}' (hardcoded path) and read the first line: \"{first_line}\"")
        except Exception as e:
            print(f"Error attempting to open/read '{hardcoded_path_to_pyproject}' (hardcoded path): {e}") 
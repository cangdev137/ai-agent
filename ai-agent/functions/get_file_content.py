import os
import sys
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_working_directory = os.path.abspath(working_directory)
    target_filepath = os.path.abspath(os.path.join(working_directory, file_path));

    if not target_filepath.startswith(full_working_directory):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory."
    if os.path.exists(target_filepath) and not os.path.isfile(target_filepath):
        return f"Error: File not found or is not a regular fiel: \"{file_path}\"."

    #truncate file contents if exceeds character limit
    try:
        with open(target_filepath, "r") as f:
            file_content = f.read(MAX_CHARS)

            if len(file_content) == MAX_CHARS:
                file_content += f" [...FILE {file_path} truncated at {MAX_CHARS} characters.]"
        return file_content
    except Exception as e:
        return f"Error: couldn't open file \"{file_path}\""




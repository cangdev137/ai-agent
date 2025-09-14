import sys
import os

def get_files_info(working_directory, directory="."):
    full_working_directory = os.path.abspath(working_directory)
    dir_path = os.path.abspath(os.path.join(working_directory, directory))
    
    #make sure directory is contained within working directory
    if not dir_path.startswith(full_working_directory):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    
    if os.path.exists(dir_path) and not os.path.isdir(dir_path):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

    try:
        dir_info = ""
        entry_size = 0
        for entry in os.listdir(dir_path):
            next_path = os.path.join(dir_path, entry) 
            entry_size = os.path.getsize(next_path)
            is_dir = os.path.isdir(next_path)

            dir_info += f"- {entry}: file_size={entry_size}, is_dir={is_dir}\n"
        return dir_info
    except Exception as e:
        return f"Error listing files: {e}"



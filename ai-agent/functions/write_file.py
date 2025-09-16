import os

def write_file(working_directory, file_path, content):
    full_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    #restrict behavior to working directory
    if not target_file.startswith(full_working_directory):
        return f"Error: Cannot write to {file_path} as it is outside the permitted working directory"
    #create necessary directory entries
    if not os.path.exists(target_file):
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        except Exception as e:
            return f"Error creating directory: {e}"
    #don't write to a directory
    if os.path.exists(full_working_directory) and os.path.isdir(target_file):
        return f"Error: \"{file_path}\" is a directory."
    
    #write to file
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
        return "Error: couldn't write to file: {e}"


        



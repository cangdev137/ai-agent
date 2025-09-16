import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(full_working_directory):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.exists(target_file):
        return f"Error: File \"{file_path}\" not found"
    if not target_file.endswith(".py"):
        return f"Error: \"{file_path}\" is not a Python file."
    
    interpreter_call = ["python3", target_file]
    if args:
        interpreter_call.extend(args)
    completed_process = subprocess.run(interpreter_call, capture_output=True, text=True, cwd=full_working_directory, timeout=30)

    try:
        process_result = ""
        if completed_process.stdout:
            process_result += f"STDOUT:\n{completed_process.stdout}\n"
        if completed_process.stderr:
            process_result += f"STDERR: \n{completed_process.stderr}\n"
        if completed_process.returncode == 0:
            process_result += f"Process exectued with non-zero code.\n"

        if len(completed_process.stdout) == 0:
            return f"No output produced."
        return process_result
    except Exception as e:
        return f"Error: executing Python file: {e}"



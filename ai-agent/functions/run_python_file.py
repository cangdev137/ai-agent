import os
import subprocess
from google import genai

def run_python_file(working_directory, file_path, args=[]):
    full_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(full_working_directory):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.exists(target_file):
        return f"Error: File \"{file_path}\" not found"
    if not target_file.endswith(".py"):
        return f"Error: \"{file_path}\" is not a Python file."


    try:
        interpreter_call = ["python3", target_file]
        if args:
            interpreter_call.extend(args)

        completed_process = subprocess.run(
                interpreter_call, 
                capture_output=True, 
                text=True, 
                cwd=full_working_directory, 
                timeout=30
        )

        process_result_parts = []
        if completed_process.stdout:
            process_result_parts.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            process_result_parts.append(f"STDERR: \n{completed_process.stderr}")
        if completed_process.returncode == 0:
            process_result_parts.append(f"Process exectued with non-zero code.")

        if not process_result_parts:
            return f"No output produced."
        return "\n".join(process_result_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file= genai.types.FunctionDeclaration(
        name = "run_python_file",
        description = "Runs an existing python file based on the provided file path, which is relative to the working directory. The user may optionally provide arguments that can be passed via the command line to the python file. Returns a string containing any STDOUT or STDERR messages, or if no output is produced, a message detailing so. If the file does not exist or is outside the provided working directory, the program returns a string denoting an error.",
        parameters = genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="A path to the python file which should be executed, relative to the working directory. If not provided, the function returns a string denoting an error."
                ),
                "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                description="An array holding any arguments the user wishes to pass to the function. If none are specified or provided, then this argument should be empty",
                items=genai.types.Schema(type=genai.types.Type.STRING)
                ),

            },
            required=["file_path"]
        )
    )



from google import genai
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

#specify functions available to agent for use
available_functions = genai.types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
)

function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
}

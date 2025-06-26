
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):

    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    new_args = dict(function_call_part.args)
    new_args["working_directory"] = "./calculator"

    function_map = {
        "write_file": write_file,
        "run_python_file": run_python_file,
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        }
    if function_call_part.name in function_map:
        chosen_func = function_map[function_call_part.name]
        result= chosen_func(**new_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
            )
        ],
    )
    else:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )


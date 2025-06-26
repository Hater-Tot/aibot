import sys
import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.call_function import call_function



system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, you should proactively use your available tools to gather the information needed to answer their question. You can perform the following operations:

- List files and directories
- Read file contents  
- Execute Python files with optional arguments
- Write or overwrite files

Start by exploring the available files and directories to understand the codebase before answering questions about it.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description = 'AI CLI tool')
    parser.add_argument('prompt', help = 'The prompt to send to the AI')
    parser.add_argument('--verbose', action = 'store_true', help='Enable verbose output')

    args = parser.parse_args()
    user_prompt = args.prompt

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20):
        response = generate_content(client, messages, args.verbose)
        for candidate in response.candidates:
            messages.append(candidate.content)
        if response.function_calls:
            for call in response.function_calls:
                function_call_result = call_function(call, verbose=args.verbose)
                
                if (not function_call_result.parts or 
                    not hasattr(function_call_result.parts[0], 'function_response') or 
                    not hasattr(function_call_result.parts[0].function_response, 'response')):
                    raise Exception("Function call did not produce a response.")
                messages.append(function_call_result)
                response_content = function_call_result.parts[0].function_response.response
            
                if args.verbose:
                    print(f"-> {response_content}")
            
        else:
            print(response.text)
            break



def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    )
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
          
    return response
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file",
    parameters= types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description= "The file path to read content from."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute"
            )
        }
    )
)

schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Writes files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to write a file."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            )
        }
    )
)



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content
    ]
)
if __name__ == "__main__":
    main()

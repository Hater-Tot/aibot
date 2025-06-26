import os
import subprocess

def run_python_file(working_directory, file_path):

    try:
        working_directory_abs = os.path.abspath(working_directory)
        directory_abs = os.path.abspath(os.path.join(working_directory, file_path))
        is_file = os.path.isfile(directory_abs)
        if not directory_abs.startswith(working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not is_file:
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'


        command_to_run =["python3", directory_abs]
        result = subprocess.run(command_to_run, capture_output=True, text=True, check=True, timeout=30, cwd=working_directory)
        
        formatted_output = []
        if result.stdout:
            formatted_output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            formatted_output.append(f"STDERR: {result.stderr}")
        final_string = "\n".join(formatted_output)
        if not final_string:
            final_string = "No output produced."
        return final_string
    
    except subprocess.CalledProcessError as e:
        formatted_output_on_error = []
        if e.stdout:
            formatted_output_on_error.append(f"STDOUT:{e.stdout}")
        if e.stderr:
            formatted_output_on_error.append(f"STDERR: {e.stderr}")

        
        return_code= e.returncode
        error_code = f"Process exited with code {return_code}"
        formatted_output_on_error.append(error_code)
        final_error_string = "\n".join(formatted_output_on_error)
        return final_error_string
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
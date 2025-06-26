import os

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        directory_abs = os.path.abspath(os.path.join(working_directory, file_path))
        is_file = os.path.isfile(directory_abs)
        if not directory_abs.startswith(working_directory_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        MAX_CHARS = 10000
        with open(directory_abs, "r") as f:
        
            file_content_string = f.read(MAX_CHARS)
            if f.read(1) !=  "":
                file_content_string = file_content_string + (f'[...File "{file_path}" truncated at 10000 characters]')
        return file_content_string
    except Exception as e:
        return f'Error {e}'


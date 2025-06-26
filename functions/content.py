import os

def write_file(working_directory, file_path, content):
    try:    
        working_directors_abs = os.path.abspath(working_directory)
        directory_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not directory_abs.startswith(working_directors_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        directory_to_create = os.path.dirname(directory_abs)
        os.makedirs(directory_to_create, exist_ok=True)

        with open(directory_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
        
    except Exception as e:
        return f'Error: {e}'
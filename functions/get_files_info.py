import os

def get_files_info(working_directory, directory=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        if directory:
            directory_abs = os.path.abspath(os.path.join(working_directory, directory))
        else:
            directory_abs = working_directory_abs
        is_directory = os.path.isdir(directory_abs)
        if not directory_abs.startswith(working_directory_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not is_directory:
            return f'Error: "{directory}" is not a directory'
    
        lines = []
        list_dir = os.listdir(directory_abs)
        for file in list_dir:
            names = os.path.join(directory_abs, file)
            file_size = os.path.getsize(names)
            is_dir = os.path.isdir(names)
        
            lines.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
  



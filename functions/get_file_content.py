import os
from .config import MAX_CHARS


def get_file_content(working_directory, file_path):
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_abs = os.path.abspath(working_directory)
    if not target_dir.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(target_dir) > MAX_CHARS:
                file_content_string += (
                    f'[...File "{file_path}" truncated at 10000 charachters]'
                )
            f.close()
        return file_content_string

    except Exception as e:
        print(f"Error reading file content: {e}")

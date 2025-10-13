import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    working_dir_abs = os.path.abspath(working_directory)
    if not target_dir.startswith(working_dir_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            files_info.append(
                f"- {filename}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}"
            )
        return "\n".join(files_info)
    except Exception as e:
        print(f"Error listing files: {e}")


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory",
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

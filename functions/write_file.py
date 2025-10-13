import os
from google.genai import types


def write_file(working_directory, file_path, content):
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_abs = os.path.abspath(working_directory)

    if not target_dir.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    file_name = target_dir.split(f"{os.path.dirname(target_dir)}/")[1]
    try:
        if not os.path.exists(target_dir):
            os.makedirs(os.path.dirname(target_dir))
        with open(file_name, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        print(f"Error writing file: {e}")


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write provided content to file at specified file path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of a file that the provided will be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that will be written to a file with specified file path",
            ),
        },
        required=["file_path", "content"],
    ),
)

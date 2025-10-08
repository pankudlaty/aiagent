import os


def write_file(working_directory, file_path, content):
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_abs = os.path.abspath(working_directory)

    if not target_dir.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the prmitted working directory'
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

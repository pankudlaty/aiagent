import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    working_dir_abs = os.path.abspath(working_directory)
    if directory == ".":
        result = f"Result for current directory:\n"
    else:
        result = f"Result for '{directory}' directory:\n"
    if not full_path.startswith(working_dir_abs):
        return f'{result}Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'{result}Error: "{directory}" is not a directory'

    try:
        files = os.listdir(full_path)
        for f in files:
            file_path = f"{full_path}/{f}"
            result += f"- {f}: file_size={os.path.getsize(file_path)} bytes, is_dir={not os.path.isfile(file_path)}\n"
        return result
    except Exception as e:
        print(f"{result}Error: {e}")

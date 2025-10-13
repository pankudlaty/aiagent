import os, subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_abs = os.path.abspath(working_directory)

    if not target_dir.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_dir):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmds = ["python", target_dir]
        if args:
            cmds.extend(args)
        cmd_result = subprocess.run(
            cmds, capture_output=True, text=True, timeout=30, cwd=working_dir_abs
        )
        output = []
        if cmd_result.stdout:
            output.append(f"STDOUT:\n{cmd_result.stdout}")
        if cmd_result.stderr:
            output.append(f"STDEER:\n{cmd_result.stderr}")
        if cmd_result.returncode != 0:
            output.append(f"Process exited with code {cmd_result.returncode}")
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        print(f"Error: executing Python file: {e}")


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file located at specified file path and with provided arguments, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to a python file that will be run, relative to working directory",
            ),
        },
        required=["file_path"],
    ),
)

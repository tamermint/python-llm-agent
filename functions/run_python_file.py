import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute python with optional arguments supplied(default is None). Returns the output string or errors if any. If its not a valid file, an error is returned",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The python file to run relative to the working directory",
                },
                "args": {
                    "type": {
                        "array": {
                            "items": "strings"
                        }
                    },
                    "description": "Optional array of arguments for the python file. Default value is none"
                }
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str :
    try:
        working_directory_abs_path = os.path.abspath(working_directory)

        target_file_path = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

        valid_file = os.path.commonpath([working_directory_abs_path, target_file_path]) == working_directory_abs_path

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        elif not valid_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", target_file_path]
        if(args):
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}"
            return output_string
        elif completed_process.stdout == "" and completed_process.stderr == "":
            output_string += "No output produced"
            return output_string
        else:
            output_string += f'''STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}'''
            return output_string
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
def main():
    run_python_file("calculator", "lorem.txt")

if __name__ == "__main__":
    main()

    
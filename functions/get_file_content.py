import os
import sys

""" current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir) """

import config

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        
        # Get the path of the working directory
        working_directory_path = os.path.abspath(working_directory)
        
        # Normalize the file path and join working directory with the file path
        target_file_path = os.path.normpath(os.path.join(working_directory_path, file_path))

        # Check whether file_path is within working directory
        valid_file = os.path.commonpath([working_directory_path, target_file_path]) == working_directory_path

        max_chars = config.MAX_CHARS        

        if not valid_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file_path, "r") as f:
                file_content = f.read(max_chars) 
                if f.read(1):
                    file_content += f'[...File "{file_path}" truncated at {max_chars} characters]'
                return file_content
    except Exception as e:
        return f'Error: {e}'

def main():
    get_file_content()

if __name__ == "__main__":
    main()
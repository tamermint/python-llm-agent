import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrite specific file relative to the working directory with arguments supplied in function and return the number of characters written to the file. If file doesn't exist, it is created. If parent directory does not exist, it is created ",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file to be modified with the supplied argument",
                },
                "content": {
                    "type": "string",
                    "description": "The changes required to be written into the file_path"
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str: 
    try:
        # Get the absolute path of the working directory
        working_directory_abspath = os.path.abspath(working_directory)

        # Normalize and join the working directory and the file path
        target_file_path = os.path.normpath(os.path.join(working_directory_abspath, file_path))

        # Check whether the target file path is within the working directory
        valid_file = os.path.commonpath([working_directory_abspath, target_file_path]) == working_directory_abspath

        if not valid_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(target_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

def main():
    write_file()

if __name__ == "__main__":
    main()


    
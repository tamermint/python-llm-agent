import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "List all files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path_work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path_work_dir, directory))

        valid_target_dir = os.path.commonpath([abs_path_work_dir, target_dir]) == abs_path_work_dir
        
        if not valid_target_dir:
            return f'Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'"{directory}" is not a directory'
        files_info: list[str] = []
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            files_info.append(
                f'- {file}: file_size={file_size} bytes, is_dir={is_dir}'
            )
        return "\n".join(files_info)
    except Exception as e:
        return f'Error listing files: {e}'

def main():
    get_files_info("calculator", ".")

if __name__ == "__main__":
    main()
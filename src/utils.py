import os


def clean_file_id(file_id) -> str:
    """Clean file id."""
    return file_id.replace("/", "_").replace("-", "_").replace(".", "_")


def clean_message(message) -> str:
    """Clean message."""
    # skip lines before the first empty line
    message = message[message.find("\n\n") + 2 :]
    return message


def get_files(path, extension=".json") -> list:
    """Get files in a folder."""
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if extension in file:
                files.append(os.path.join(r, file))
    return files


def list_files(folder_path) -> list:
    """List files in a folder."""
    return [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

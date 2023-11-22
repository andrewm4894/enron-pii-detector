import os


def clean_file_id(file_id) -> str:
    return file_id.replace("/", "_").replace("-", "_").replace(".", "_")


def clean_message(message) -> str:
    # skip lines before the first empty line
    message = message[message.find("\n\n") + 2 :]
    return message


def get_files(path, extension=".json"):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if extension in file:
                files.append(os.path.join(r, file))
    return files

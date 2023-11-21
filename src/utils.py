def clean_file_id(file_id) -> str:
    return file_id.replace("/", "_").replace("-", "_").replace(".", "_")


def clean_message(message) -> str:
    # skip lines before the first empty line
    message = message[message.find("\n\n") + 2 :]
    return message

def clean_file_id(file_id) -> str:
    return file_id.replace("/", "_").replace("-", "_").replace(".", "_")


def clean_message(message, n_skip_rows=16) -> str:
    return "\n".join(message.split("\n")[n_skip_rows:])

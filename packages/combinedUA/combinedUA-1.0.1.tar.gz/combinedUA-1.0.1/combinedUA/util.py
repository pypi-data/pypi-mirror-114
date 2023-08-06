import os


def read_file(file) -> str:
    stream = open(file, encoding="utf8")
    text = stream.read()
    stream.close()
    return text


def get_base_dir(file: str, level: int = 0):
    base_dir = os.path.abspath(file)
    for _ in range(level + 1):
        base_dir = os.path.dirname(base_dir)
    return base_dir

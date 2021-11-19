import os


def mkdir_if_not_exists(path: str, multiple_directories=False) -> str:
    if not os.path.exists(path):
        if not multiple_directories:
            os.mkdir(path)
        os.makedirs(path)
    return path

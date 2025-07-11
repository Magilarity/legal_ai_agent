import os


def tree(dir_path: str, prefix: str = "") -> None:
    entries = sorted(os.listdir(dir_path))
    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry)
        new_prefix = prefix + ("    " if index == len(entries) - 1 else "│   ")
        path = os.path.join(dir_path, entry)
        if os.path.isdir(path):
            tree(path, new_prefix)

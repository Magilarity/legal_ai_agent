import os


def tree(dir_path, prefix=""):
    entries = sorted(os.listdir(dir_path))
    for index, name in enumerate(entries):
        path = os.path.join(dir_path, name)
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + name + ("/" if os.path.isdir(path) else ""))
        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            tree(path, prefix + extension)


print(os.path.basename(os.getcwd()) + "/")
tree(".")

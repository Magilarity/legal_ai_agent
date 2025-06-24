def generate_document(path: str) -> bytes:
    with open(path, "rb") as f:
        data = f.read()
    return data

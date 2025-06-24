def load(path: str) -> str:
    try:
        with open(path, "rb") as f:
            data = f.read()
        return data.decode("utf-8")
    except Exception:
        return ""


def extract_text_from_file(path: str) -> str:
    return load(path)

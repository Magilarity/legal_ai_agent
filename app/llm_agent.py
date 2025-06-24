import os

def init_client() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "OPENAI_API_KEY must be set"
    return api_key.strip()
# interface/prozorro_loader.py

from ingest.loader import download_documents


# щоб зберегти старий інтерфейс:
def __getattr__(name):
    if name == "download_documents":
        return download_documents
    raise AttributeError(f"module 'prozorro_loader' has no attribute '{name}'")

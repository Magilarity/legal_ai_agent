# mypy: disable-error-code="attr-defined"
from prozorro_loader import download_documents_with_progress

def analyze_tender(tender_id: str) -> None:
    _path = download_documents_with_progress(tender_id, None, None)  # noqa: F841
    # analysis logic
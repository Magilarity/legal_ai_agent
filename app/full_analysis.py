# app/full_analysis.py
# mypy: disable-error-code="attr-defined"

from interface.prozorro_loader import download_documents
from typing import Any, List


class RAGEngine:
    """
    Retrieval-Augmented Generation engine.
    Працює за схемою: ембединг запиту → пошук релевантних документів → генерація відповіді.
    """

    def __init__(self, embedder: Any, retriever: Any, llm: Any):
        """
        :param embedder: об’єкт із методом embed_text(text: str) -> List[float]
        :param retriever: об’єкт із методом retrieve(query_embedding: List[float], top_k: int) -> List[str]
        :param llm: об’єкт із методом generate(prompt: str) -> str
        """
        self.embedder = embedder
        self.retriever = retriever
        self.llm = llm

    def run(self, query: str) -> str:
        """
        Виконує RAG-пайплайн для вхідного запиту.
        """
        if not query or not query.strip():
            raise ValueError("Query must not be empty")

        embedding = self.embedder.embed_text(query)
        docs = self.retriever.retrieve(embedding, top_k=3)
        prompt = self._build_prompt(query, docs)
        return self.llm.generate(prompt)

    def _build_prompt(self, query: str, docs: List[str]) -> str:
        """
        Складає текст промпту для LLM на основі знайдених документів.
        """
        context = "\n\n".join(docs)
        return f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"


def analyze_tender(tender_id: str) -> None:
    """
    Завантажує документи тендеру та виконує подальший аналіз.
    """
    path = download_documents(tender_id)
    print(f"Documents downloaded to {path}. Додайте вашу логіку аналізу тут.")
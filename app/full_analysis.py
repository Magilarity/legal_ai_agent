# app/full_analysis.py
# mypy: disable-error-code="attr-defined"

from typing import List, Protocol

import faiss
import numpy as np

from app.llm_agent import LLMAgent
from interface.prozorro_loader import download_documents

# Розмір ембеддінгу — замініть на реальний
EMBED_DIM = 2


class EmbedderProtocol(Protocol):
    def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Перетворює текст у вектор.
        """
        ...


class RetrieverProtocol(Protocol):
    def retrieve(
        self,
        query_embedding: List[float],
        top_k: int,
    ) -> List[str]:
        """
        Повертає список релевантних документів.
        """
        ...


class LLMProtocol(Protocol):
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Генерує відповідь на основі промпту.
        """
        ...


class RAGEngine:
    """
    Retrieval-Augmented Generation engine.
    """

    def __init__(
        self,
        embedder: EmbedderProtocol,
        retriever: RetrieverProtocol,
        llm: LLMProtocol,
    ) -> None:
        self.embedder = embedder
        self.retriever = retriever
        self.llm = llm

    def run(self, query: str) -> str:
        """
        Виконує RAG-пайплайн для вхідного запиту.
        """
        if not query or not query.strip():
            raise ValueError("Query must not be empty")

        # 1) Ембединг запиту
        embedding = self.embedder.embed_text(query)

        # 2) Пошук релевантних документів
        docs = self.retriever.retrieve(embedding, top_k=3)

        # 3) Формування промпту
        prompt = self._build_prompt(query, docs)

        # 4) Запит до LLM
        # Викликаємо метод chat якщо є, інакше generate
        if hasattr(self.llm, "chat"):
            answer = self.llm.chat(prompt)
        elif hasattr(self.llm, "generate"):
            answer = self.llm.generate(prompt)
        else:
            raise AttributeError("LLM has no generate or chat method")
        return answer

    def _build_prompt(self, query: str, docs: List[str]) -> str:
        """
        Складає текст промпту для LLM на основі знайдених документів.
        """
        context = "\n\n".join(docs)
        return f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"


def load_faiss_index(path: str = "index.faiss") -> faiss.IndexFlatL2:
    """
    Завантажує FAISS-індекс з диску або створює новий порожній.
    """
    return faiss.IndexFlatL2(EMBED_DIM)


def embed_texts(texts: List[str]) -> List[np.ndarray]:
    """
    Конвертує тексти у вектори (stub для реального embedder).
    """
    return [np.zeros(EMBED_DIM, dtype=np.float32) for _ in texts]


def analyze_tender(tender_id: str) -> str:
    """
    Завантажує документи тендеру та виконує подальший RAG-аналіз.
    :return: згенерована відповідь від LLM
    """
    # Завантаження документів
    path = download_documents(tender_id)
    print(f"Documents downloaded to {path}. Starting RAG analysis...")

    # Підготовка індексу та документів (stub)
    index = load_faiss_index()
    docs = ["Документ 1", "Документ 2", "Документ 3"]
    embeddings = embed_texts(docs)
    for vec in embeddings:
        index.add(vec.reshape(1, -1))

    # Ініціалізація компонентів
    # Простий ретрівер на основі stub-документів
    class Retriever:
        def __init__(self, docs: List[str]):
            self.docs = docs

        def retrieve(self, query_embedding: List[float], top_k: int) -> List[str]:
            return self.docs[:top_k]

    embedder = type(
        "StubEmbedder",
        (),
        {"embed_text": staticmethod(lambda text: list(np.zeros(EMBED_DIM)))},
    )()
    retriever = Retriever(docs)
    llm = LLMAgent(api_key="KEY", model="gpt-4")

    engine = RAGEngine(embedder=embedder, retriever=retriever, llm=llm)
    result = engine.run(query=tender_id)
    print(f"Analysis result: {result}")
    return result

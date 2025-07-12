import pytest

from app.full_analysis import RAGEngine


class DummyEmbedder:
    def embed_text(self, text):
        # повертаємо фіктивний вектор
        return [0.1, 0.2, 0.3]


class DummyRetriever:
    def retrieve(self, query_embedding, top_k=3):
        # імітуємо знайдені документи
        return ["doc1 content", "doc2 content", "doc3 content"]


class DummyLLM:
    def generate(self, prompt):
        # повертаємо фіктивну відповідь, щоб перевірити інтеграцію
        return "ANSWER: " + prompt


@pytest.fixture
def rag_engine():
    emb = DummyEmbedder()
    retr = DummyRetriever()
    llm = DummyLLM()
    return RAGEngine(embedder=emb, retriever=retr, llm=llm)


def test_rag_run_with_valid_query(rag_engine):
    """
    При коректному запиті RAGEngine має повернути рядкову відповідь,
    яка містить згенерований LLM текст.
    """
    query = "Що таке тест?"
    answer = rag_engine.run(query)
    assert isinstance(answer, str)
    assert answer.startswith("ANSWER:"), "Очікуємо, що відповідь починається з ANSWER:"


def test_rag_run_empty_query_raises(rag_engine):
    """
    Якщо запит порожній, має кидатися ValueError (або інша ваша
    власна помилка).
    """
    with pytest.raises(ValueError):
        rag_engine.run("")

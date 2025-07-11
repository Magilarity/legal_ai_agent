import pytest
import numpy as np
import faiss

from app.full_analysis import (
    RAGEngine,
    load_faiss_index,
    embed_texts,
)


class DummyEmbedder:
    def embed_text(self, text: str):
        return [1.0, 2.0]


class DummyRetriever:
    def __init__(self, docs):
        self.docs = docs

    def retrieve(self, embedding, top_k):
        return self.docs[:top_k]


class DummyLLM:
    def __init__(self):
        self.called = False

    def generate(self, prompt: str) -> str:
        self.called = True
        return "DUMMY"


@pytest.fixture
def docs():
    return ["doc1", "doc2", "doc3"]


def test_build_prompt_formats_correctly(docs):
    engine = RAGEngine(DummyEmbedder(), DummyRetriever(docs), DummyLLM())
    prompt = engine._build_prompt("Q", docs)
    assert "Context:" in prompt
    assert "doc1" in prompt
    assert "Question: Q" in prompt
    assert prompt.endswith("Answer:")


def test_run_empty_query_raises():
    engine = RAGEngine(DummyEmbedder(), DummyRetriever([]), DummyLLM())
    with pytest.raises(ValueError):
        engine.run("   ")


def test_engine_end_to_end(docs):
    llm = DummyLLM()
    engine = RAGEngine(DummyEmbedder(), DummyRetriever(docs), llm)
    res = engine.run("hello")
    assert res == "DUMMY"
    assert llm.called


def test_load_faiss_index_creates_correct_dim():
    idx = load_faiss_index()
    assert isinstance(idx, faiss.IndexFlatL2)
    # FAISS attribute .d holds dimension
    assert idx.d == 2


def test_embed_texts_returns_zero_vectors():
    vecs = embed_texts(["a", "b"])
    assert len(vecs) == 2
    for v in vecs:
        assert isinstance(v, np.ndarray)
        assert v.shape == (2,)
        assert np.all(v == 0)


def test_run_prefers_chat_over_generate(docs):
    # Якщо LLM має chat(), воно використовуватиметься замість generate()
    class ChatLLM:
        def __init__(self):
            self.called = False

        def chat(self, prompt: str) -> str:
            self.called = True
            return "CHAT"

    engine = RAGEngine(DummyEmbedder(), DummyRetriever(docs), ChatLLM())
    result = engine.run("hello")
    assert result == "CHAT"
    assert engine.llm.called


def test_run_no_chat_or_generate_raises(docs):
    # Якщо LLM не має ні chat(), ні generate()
    engine = RAGEngine(DummyEmbedder(), DummyRetriever(docs), object())
    with pytest.raises(AttributeError):
        engine.run("hello")

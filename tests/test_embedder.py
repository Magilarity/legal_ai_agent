import pytest

from app.embedder import Embedder


@pytest.fixture
def embedder():
    # Ініціалізуємо клас-обгортку над вашим ембедером
    return Embedder()


def test_embed_single_text(embedder):
    """
    Перевіряємо, що на вхід рядок, а на вихід – список чисел
    довільної, але сталої довжини (>0).
    """
    text = "Це тестовий текст"
    vec = embedder.embed_text(text)
    assert isinstance(vec, list), "Результат має бути списком"
    assert len(vec) > 0, "Вихідний вектор не може бути порожнім"
    assert all(isinstance(x, float) for x in vec), "Усі елементи мають бути float"


def test_embed_batch_texts(embedder):
    """
    Перевіряємо пакетну обробку кількох текстів.
    Маємо отримати список векторів тієї ж довжини, що й вхід.
    """
    texts = ["Перший", "Другий", "Третій"]
    vectors = embedder.embed_texts(texts)
    assert isinstance(vectors, list), "Результат має бути списком списків"
    assert len(vectors) == len(
        texts
    ), "Кількість векторів має співпадати з кількістю текстів"
    for v in vectors:
        assert isinstance(v, list)
        assert len(v) > 0
        assert all(isinstance(x, float) for x in v)

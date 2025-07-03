# app/embedder.py
from typing import List


class Embedder:
    """
    Обгортка для ембедер-моделі, що перетворює текст у вектор.
    """

    def __init__(self):
        # TODO: Ініціалізація реального ембедеру (наприклад OpenAI)
        pass

    def embed_text(self, text: str) -> List[float]:
        """
        Повертає вектор для одного тексту.
        """
        # TODO: Виклик реального ембедеру замість заглушки
        # Поки повертаємо фіктивний вектор базуючись на довжині тексту
        return [float(len(text))]

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Повертає список векторів для кожного тексту.
        """
        return [self.embed_text(t) for t in texts]

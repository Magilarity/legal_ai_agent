import os
import time
import logging

from dotenv import load_dotenv  # <--- Додаємо
import openai

# Завантажуємо .env з кореня проекту
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]
)


def generate_answer(
    context: str,
    question: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> str:
    """
    Генерує відповідь через OpenAI Chat API (v1.0+)
    із автоматичним back-off у разі помилок.
    """
    prompt = (
        f"Контекст:\n{context}\n\n"
        f"Питання:\n{question}\n\n"
        "Відповідь:"
    )

    for attempt in range(1, max_retries + 1):
        try:
            response = openai.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            wait = backoff_factor ** (attempt - 1)
            logging.warning(
                f"[Attempt {attempt}/{max_retries}] Помилка при виклику OpenAI: {e}. "
                f"Чекаю {wait} сек..."
            )
            time.sleep(wait)

    raise RuntimeError("Не вдалося отримати відповідь від OpenAI після кількох спроб.")
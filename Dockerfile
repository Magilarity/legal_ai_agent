# Dockerfile

FROM python:3.13-slim

WORKDIR /app
ENV PYTHONPATH=/app

# (Опціонально) системні утиліти для діагностики та конвертації рядків
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      procps \
      dos2unix && \
    rm -rf /var/lib/apt/lists/*

# Встановлюємо залежності Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Перетворимо start.sh у Unix-формат і зробимо виконуваним
RUN dos2unix start.sh && \
    chmod +x start.sh

# Декларуємо порти для Streamlit та Prometheus метрик
EXPOSE 8501 8000

# Щоб Python виводив логи одразу
ENV PYTHONUNBUFFERED=1

# За замовчуванням запускаємо скрипт, який стартує Prometheus HTTP-сервер і Streamlit UI
ENTRYPOINT ["./start.sh"]
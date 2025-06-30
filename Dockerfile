# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# (Опціонально) системні утиліти для діагностики
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl procps dos2unix && \
    rm -rf /var/lib/apt/lists/*

# Встановлюємо залежності Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Перетворимо стартовий скрипт у Unix-формат і зробимо виконуваним
RUN dos2unix start.sh && \
    chmod +x start.sh

ENV PYTHONUNBUFFERED=1

# За замовчуванням піднімаємо спершу Prometheus HTTP-сервер метрик, а потім Streamlit UI
CMD ["./start.sh"]
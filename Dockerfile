FROM python:3.13-slim

WORKDIR /app

# 1) Встановлюємо залежності
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2) Копіюємо весь код проекту
COPY . .

ENV PYTHONUNBUFFERED=1

# 3) Копіюємо та робимо виконуваним наш скрипт запуску
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 4) За замовчуванням запускаємо саме його
CMD ["/app/start.sh"]
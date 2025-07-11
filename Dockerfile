#############################################
#               Builder stage               #
#############################################
FROM python:3.13-slim AS builder

WORKDIR /app

# Системні залежності (включаючи FAISS headers і SWIG)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl procps dos2unix swig libfaiss-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо метадані і встановлюємо Python-залежності (додаємо fastapi & uvicorn для бекенду)
COPY pyproject.toml setup.py requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt \
    && pip install --no-cache-dir faiss-cpu openai fastapi uvicorn[standard]

#############################################
#               Runtime stage               #
#############################################
FROM python:3.13-slim

WORKDIR /app

# Додаткові утиліти: curl для healthcheck, dos2unix та libfaiss-dev для FAISS
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl dos2unix libfaiss-dev \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо встановлені пакети та CLI-утиліти з builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копіюємо код застосунку
COPY . .

# Робимо start.sh виконуваним
RUN dos2unix start.sh \
    && chmod +x start.sh

# Команда за замовчуванням — запуск бекенду, метрик і Streamlit через start.sh
CMD ["sh", "./start.sh"]
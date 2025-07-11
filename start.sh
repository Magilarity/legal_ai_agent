#!/bin/sh
set -e

# Додаємо корінь проєкту до PYTHONPATH, щоб Python знаходив пакети
export PYTHONPATH=/app

# Коректно завершувати фонові процеси при виході
trap 'kill $(jobs -p)' EXIT

# ─── Запускаємо FastAPI бекенд на порту 8000 ──────────────────────────────────
echo "[API] Starting FastAPI backend on port 8000"
uvicorn services.app:app --host 0.0.0.0 --port 8000 &

# ─── Запускаємо Prometheus HTTP-сервер метрик у фоні ─────────────────────────
echo "[METRICS] Starting Prometheus metrics server in background"
python - << 'PYCODE' &
import time
from prometheus_client import start_http_server
from app.metrics import init_metrics, registry

# Регіструємо лічильники/гістограми
init_metrics()
# Експонуємо їх на 0.0.0.0:8001
start_http_server(8001, registry=registry)

# Тримаємо процес живим
while True:
    time.sleep(60)
PYCODE

# ─── Запускаємо тільки Streamlit UI ────────────────────────────────────────────
echo "[APP] Launching Streamlit UI"
exec python -m streamlit run interface/streamlit_app.py \
     --server.port=8501 --server.address=0.0.0.0
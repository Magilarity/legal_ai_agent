#!/bin/sh
set -e

# ─── Запускаємо Prometheus-сервер метрик у фоні ─────────────────────────────────
echo "[METRICS] Starting Prometheus metrics server in background"
python - << 'PYCODE' &
from prometheus_client import start_http_server
import time
# Запускаємо сервер метрик
start_http_server(8001, addr="0.0.0.0")
# Підтримуємо процес метрик живим
while True:
    time.sleep(60)
PYCODE
# ────────────────────────────────────────────────────────────────────────────────

echo "[APP] Launching Streamlit UI"
exec streamlit run interface/streamlit_app.py \
     --server.port=8501 --server.address=0.0.0.0
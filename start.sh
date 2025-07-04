#!/bin/sh
set -e

# Додаємо корінь проєкту до PYTHONPATH, щоб Python знаходив пакети навіть після зміни робочої директорії
export PYTHONPATH=/app

# ─── Запускаємо Prometheus-сервер метрик у фоні ─────────────────────────────────
echo "[METRICS] Starting Prometheus metrics server in background"
python - << 'PYCODE' &
from app.metrics import init_metrics
import time
# Ініціалізуємо HTTP-сервер метрик на адресі 0.0.0.0:8001
init_metrics(8001)
# Утримуємо процес метрик живим
while True:
    time.sleep(60)
PYCODE
# ────────────────────────────────────────────────────────────────────────────────

echo "[APP] Launching Streamlit UI"
# Запускаємо Streamlit UI на порті 8501, прив'язка на 0.0.0.0 для зовнішнього доступу
exec python -m streamlit run interface/streamlit_app.py \
     --server.port=8501 --server.address=0.0.0.0
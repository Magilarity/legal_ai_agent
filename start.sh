#!/bin/sh
set -e

echo "[METRICS] Starting Prometheus metrics server on 0.0.0.0:8001"
python - << 'PYCODE'
from prometheus_client import start_http_server
start_http_server(8001, addr="0.0.0.0")
PYCODE

echo "[APP] Launching Streamlit UI"
exec streamlit run interface/streamlit_app.py \
     --server.port=8501 --server.address=0.0.0.0
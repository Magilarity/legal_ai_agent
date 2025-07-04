# interface/streamlit_app.py

import os
import sys

# Забезпечуємо, що корінь проєкту (/app) в sys.path навіть після chdir від Streamlit
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

import time
import streamlit as st

# Правильний імпорт функції завантаження тендерів
from interface.prozorro_loader import download_documents

from app.full_analysis import analyze_tender

# Метрики
from app.metrics import registry, REQUEST_COUNT, REQUEST_LATENCY, init_metrics
from prometheus_client import generate_latest

# Запускаємо HTTP-сервер метрик
init_metrics(8001)

# Інтерфейс
st.title("Magilarity Legal AI Agent")

tender_id = st.text_input(
    "Tender ID",
    help="Введіть ідентифікатор тендеру (наприклад UA-2025-06-09-008224-a)"
)

if st.button("Analyze"):
    start_ts = time.time()
    try:
        REQUEST_COUNT.labels(endpoint="analyze").inc()

        path = download_documents(tender_id)
        st.write(f"📂 Документи збережено в: `{path}`")

        analyze_tender(tender_id)
        st.success("✅ Аналіз завершено успішно.")
    except Exception as e:
        st.error(f"❌ Сталася помилка під час аналізу: {e}")
    finally:
        elapsed = time.time() - start_ts
        REQUEST_LATENCY.labels(endpoint="analyze").observe(elapsed)

if st.checkbox("Show Prometheus metrics"):
    metrics_output = generate_latest(registry)
    st.text(metrics_output.decode("utf-8"))
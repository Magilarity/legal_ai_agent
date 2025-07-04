# interface/streamlit_app.py
"""
Streamlit UI для Magilarity Legal AI Agent
"""

import time
import streamlit as st
from interface.prozorro_loader import download_documents
from app.full_analysis import analyze_tender
from app.metrics import init_metrics, REQUEST_COUNT, REQUEST_LATENCY, registry
from prometheus_client import generate_latest

# Ініціалізуємо HTTP-сервер метрик
init_metrics(8001)


def main():
    """
    Основна функція Streamlit-додатку.
    """
    st.title("Magilarity Legal AI Agent")

    tender_id = st.text_input(
        "Tender ID",
        help="Введіть ідентифікатор тендеру (наприклад UA-2025-06-09-008224-a)",
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


if __name__ == "__main__":
    main()

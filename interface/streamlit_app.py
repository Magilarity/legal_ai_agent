import os
import time
import streamlit as st
from prometheus_client import start_http_server, Counter, Histogram
import prozorro_loader

# Налаштування сторінки Streamlit (UI)
st.set_page_config(page_title="Magilarity Legal Agent", layout="wide")

# ─── Prometheus метрики ─────────────────────────────────────────────────────────
REQUEST_COUNT = Counter(
    "legal_ai_agent_requests_total",
    "Кількість запитів до Legal AI Agent через Streamlit UI",
    ["action"]
)

REQUEST_LATENCY = Histogram(
    "legal_ai_agent_request_latency_seconds",
    "Час обробки запиту до Legal AI Agent через Streamlit UI",
    ["action"]
)
# ───────────────────────────────────────────────────────────────────────────────

# ─── Старт HTTP-сервера метрик ───────────────────────────────────────────────────
print("[METRICS] Starting Prometheus metrics server on 0.0.0.0:8001")
start_http_server(8001, addr="0.0.0.0")
# Відобразити посилання у UI
st.write("📊 Prometheus metrics available at http://localhost:8001/metrics")
# ───────────────────────────────────────────────────────────────────────────────

# ─── Інтерфейс Streamlit (UI) ────────────────────────────────────────────────────
st.title("Legal AI Agent")

# Введення Tender ID
with st.sidebar:
    st.header("Тендер для аналізу")
    tender_id = st.text_input("Enter Tender ID:")
    analyze = st.button("Analyze Tender")

if analyze:
    if tender_id:
        action = "analyze_tender"
        REQUEST_COUNT.labels(action=action).inc()
        start_ts = time.time()

        st.info(f"Analyzing tender: {tender_id}...")
        try:
            result = prozorro_loader.download_and_analyze(tender_id)
            elapsed = time.time() - start_ts
            REQUEST_LATENCY.labels(action=action).observe(elapsed)
            st.success("Analysis complete!")
            st.write(result)
        except Exception as e:
            st.error(f"Error during analysis: {e}")
    else:
        st.warning("Please enter a valid Tender ID before analyzing.")

# Footer with metrics link
st.markdown("---")
st.write("Metrics endpoint available at: http://localhost:8001/metrics")
# ───────────────────────────────────────────────────────────────────────────────
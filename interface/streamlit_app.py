import os
import sys
import time

# Додаємо кореневу директорію проєкту в sys.path, щоб імпорт prozorro_loader працював
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st  # noqa: E402
from prometheus_client import Counter, Histogram  # noqa: E402
import prozorro_loader  # noqa: E402

# Налаштування сторінки Streamlit (UI)
st.set_page_config(page_title="Magilarity Legal Agent", layout="wide")

# ─── Prometheus метрики ─────────────────────────────────────────────────────────
REQUEST_COUNT = Counter(
    "legal_ai_agent_requests_total",
    "Кількість запитів до Legal AI Agent через Streamlit UI",
    ["action"],
)

REQUEST_LATENCY = Histogram(
    "legal_ai_agent_request_latency_seconds",
    "Час обробки запиту до Legal AI Agent через Streamlit UI",
    ["action"],
)
# ────────────────────────────────────────────────────────────────────────────────

st.title("🔎 Magilarity Legal AI Agent")

# Бічна панель для введення параметрів
def load_sidebar():
    with st.sidebar:
        st.header("Тендер для аналізу")
        tid = st.text_input("Enter Tender ID:")
        run = st.button("Analyze Tender")
    return tid, run

tender_id, analyze = load_sidebar()

# Основна панель — результати
if analyze:
    if not tender_id:
        st.warning("Будь ласка, введіть дійсний Tender ID перед аналізом.")
    else:
        action = "analyze_tender"
        REQUEST_COUNT.labels(action=action).inc()
        start_ts = time.time()

        st.info(f"🔄 Аналіз тендеру: `{tender_id}`…")
        try:
            result = prozorro_loader.download_and_analyze(tender_id)
            elapsed = time.time() - start_ts
            REQUEST_LATENCY.labels(action=action).observe(elapsed)

            st.success("✅ Аналіз завершено!")
            st.write(result)
        except Exception as e:
            st.error(f"❌ Помилка під час аналізу: {e}")

# Футер із посиланням на метрики (HTTP-сервер метрик запускається через start.sh)
st.markdown("---")
st.write("📊 **Metrics endpoint:** [http://localhost:8001/metrics](http://localhost:8001/metrics)")
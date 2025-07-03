# interface/streamlit_app.py
import time
import streamlit as st
from interface.prozorro_loader import download_documents_with_progress
from app.full_analysis import analyze_tender

# Імпортуємо метрики з єдиного модуля app/metrics.py
from app.metrics import registry, REQUEST_COUNT, REQUEST_LATENCY, init_metrics
from prometheus_client import generate_latest

# Запускаємо HTTP-сервер для експонування метрик (працює у фоновому потоці)
init_metrics()  # за замовчуванням на порті 8000

# Інтерфейс Streamlit
st.title("Magilarity Legal AI Agent")

tender_id = st.text_input(
    "Tender ID", help="Введіть ідентифікатор тендеру (наприклад UA-2025-06-09-008224-a)"
)

if st.button("Analyze"):
    # Вимірюємо час виконання для гістограми
    start_ts = time.time()
    try:
        # Лічильник запитів
        REQUEST_COUNT.labels(endpoint="analyze").inc()

        # Завантаження документів та аналіз
        path = download_documents_with_progress(tender_id, None, None)
        st.write(f"📂 Документи збережено в: `{path}`")

        analyze_tender(tender_id)
        st.success("✅ Аналіз завершено успішно.")
    except Exception as e:
        st.error(f"❌ Сталася помилка під час аналізу: {e}")
    finally:
        # Фіксуємо латентність запиту
        elapsed = time.time() - start_ts
        REQUEST_LATENCY.labels(endpoint="analyze").observe(elapsed)

# Опціонально: показ Prometheus метрик у UI
if st.checkbox("Show Prometheus metrics"):
    metrics_output = generate_latest(registry)
    st.text(metrics_output.decode("utf-8"))

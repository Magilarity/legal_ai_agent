import os
import time

import streamlit as st

from prozorro_loader import download_documents_with_progress

try:
    from prozorro_loader import analyze_p7s_signatures
except ImportError:
    analyze_p7s_signatures = None

st.set_page_config(page_title="Magilarity Legal Agent", layout="wide")
st.title("🧠 Magilarity Legal Agent")

st.markdown(
    """
### Інструкції:
- **Завантажити тендер** — ввести номер тендеру або ID та отримати документ–стрім
- **Аналіз** — можливий функціонал
- **Перевірка підписів** — читає `.p7s` та створює звіт `Підписи.xlsx`
- **Відкрити документи тендеру** — відкриває останній завантажений тендер у файловій системі
"""
)

input_id = st.text_input("Введіть публічний номер або ID тендеру")

col1, col2, col3, col4 = st.columns(4)

download_triggered = col1.button("⏳ Завантажити тендер")
verify_triggered = col3.button("✅ Перевірка підписів")
open_docs_triggered = col4.button("📂 Відкрити документи тендеру")

if download_triggered and input_id:
    with st.spinner("Завантаження даних з Prozorro..."):
        progress_bar = st.progress(0)
        log_area = st.empty()

        def streamlit_logger(msg):
            log_area.text(msg)

        start_time = time.time()
        count = download_documents_with_progress(
            input_id, progress_bar, streamlit_logger
        )
        end_time = time.time()
        if count > 0:
            st.success(
                f"✅ Завантажено {count} файлів за {end_time - start_time:.2f} сек"
            )
        else:
            st.error("❌ Не вдалось завантажити документи")

if verify_triggered:
    if analyze_p7s_signatures is None:
        st.warning("Функціонал перевірки підписів не реалізований.")
    else:
        folder_root = "downloads"
        dirs = [
            d
            for d in os.listdir(folder_root)
            if os.path.isdir(os.path.join(folder_root, d))
        ]
        if not dirs:
            st.warning("Спочатку завантажте тендер")
        else:
            last_folder = os.path.join(folder_root, sorted(dirs)[-1])
            with st.spinner("Перевірка цифрових підписів..."):
                analyze_p7s_signatures(last_folder)
            st.success(f"✅ Готово! Перевірено: {last_folder}")

if open_docs_triggered:
    folder_root = "downloads"
    dirs = [
        d
        for d in os.listdir(folder_root)
        if os.path.isdir(os.path.join(folder_root, d))
    ]
    if not dirs:
        st.warning("Немає завантажених тендерів")
    else:
        last_folder = sorted(dirs)[-1]
        full_path = os.path.join(folder_root, last_folder)
        st.write(f"📑 Останній завантажений тендер: `{last_folder}`")
        st.write(f"Шлях до папки: `{full_path}`")
        st.success("Документи готові для перегляду.")

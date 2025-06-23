import os
import sys
import time

import streamlit as st

# Додаємо кореневу директорію до шляху імпорту
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prozorro_loader import download_documents_with_progress

# Якщо реалізована перевірка підписів — імпортуйте її, або закоментуйте цей рядок
try:
    from prozorro_loader import analyze_p7s_signatures
except ImportError:
    analyze_p7s_signatures = None

st.set_page_config(page_title="Magilarity Legal Agent", layout="wide")
st.title("🤖 Magilarity Legal Agent")

st.markdown(
    """
### Інструменти:
- **Завантажити тендер** — введіть номер тендеру або ID та отримаєте структуру документів
- **Аналіз** — (майбутній функціонал)
- **Перевірка підписів** — зчитує `.p7s` та створює звіт `Підписи.xlsx`
- **Відкрити документи тендеру** — відкриває останній завантажений тендер у файловій системі
"""
)

# Введення
input_id = st.text_input("Введіть публічний номер або ID тендеру")

col1, col2, col3, col4 = st.columns(4)

download_triggered = col1.button("📥 Завантажити тендер")
analyze_triggered = col2.button("📊 Аналіз (у розробці)")
verify_triggered = col3.button("🧾 Перевірка підписів")
open_docs_triggered = col4.button("📂 Відкрити документи тендеру")

# Завантаження
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
            st.error("❌ Не вдалося завантажити документи")

# Перевірка підписів
if verify_triggered:
    if analyze_p7s_signatures is None:
        st.warning("Функціонал перевірки підписів не реалізовано.")
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
            st.success("✅ Готово! Перевірено: " + last_folder)

# Відкрити документи
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
        st.write(f"📁 Останній завантажений тендер: `{last_folder}`")
        st.write(f"Шлях до папки: `{full_path}`")
        st.success("Документи готові для перегляду.")

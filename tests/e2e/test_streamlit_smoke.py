import time
import pytest
from playwright.sync_api import sync_playwright
import subprocess
import os
import signal
import sys

STREAMLIT_CMD = [
    sys.executable,
    "-m",
    "streamlit",
    "run",
    "interface/streamlit_app.py",
    "--server.port=8501",
    "--logger.level=error",
]


@pytest.fixture(scope="module")
def streamlit_server():
    popen_kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
    if hasattr(os, "setsid"):
        popen_kwargs["preexec_fn"] = os.setsid

    proc = subprocess.Popen(STREAMLIT_CMD, cwd=os.getcwd(), **popen_kwargs)

    # Чекаємо, поки стартує Streamlit
    import requests

    start = time.time()
    timeout = 20
    while True:
        try:
            requests.get("http://localhost:8501", timeout=1)
            break
        except Exception:
            if time.time() - start > timeout:
                pytest.skip("Streamlit did not start in time")
            time.sleep(1)
    yield

    # Завершуємо процес
    if hasattr(os, "killpg"):
        os.killpg(proc.pid, signal.SIGTERM)
    else:
        proc.terminate()


def test_streamlit_homepage_loads(streamlit_server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        # Завантажуємо сторінку і чекаємо, поки Streamlit відрендерить UI
        page.goto("http://localhost:8501", timeout=10000)
        # Чекаємо на h1, щоб бути впевненими, що клієнтський JS вже спрацював
        page.wait_for_selector("h1", timeout=10000)
        # Дочекаємося, поки не завершаться фонові запити
        page.wait_for_load_state("networkidle")
        # Перевіряємо заголовок вкладки
        assert "Legal AI Agent" in page.title()
        # Перевіряємо, що є <h1> з текстом
        heading = page.locator("h1").first
        assert heading.inner_text() != ""
        browser.close()

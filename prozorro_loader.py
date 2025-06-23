import os
import re
import time
from typing import Callable, List, Tuple

import openpyxl
import requests

BASE_URL = "https://public.api.openprocurement.org/api/2.5/tenders"
SEARCH_API = "https://api.prozorro.gov.ua/tenders.json"

# Сесія для повторного використання TCP-з’єднань
session = requests.Session()


def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name)


def resolve_tender_id_by_public_number(public_id: str) -> str:
    """Шукаємо внутрішній ID тендеру через SEARCH_API."""
    try:
        resp = session.get(SEARCH_API, params={"tenderID": public_id}, timeout=10)
        resp.raise_for_status()
        arr = resp.json().get("data", [])
        if arr:
            return arr[0]["id"]
    except Exception:
        pass
    print(f"[err] Тендер {public_id} не знайдено через SEARCH_API.")
    return None


def fetch_with_retry(url: str) -> requests.Response:
    """GET з експоненціальним бек-офом у разі 429."""
    backoffs = [1, 2, 4]
    for b in backoffs:
        r = session.get(url, timeout=30)
        if r.status_code == 429:
            time.sleep(b)
            continue
        r.raise_for_status()
        return r
    # фінальна спроба
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r


def save_doc(doc: dict, folder: str, logger: Callable[[str], None] = print) -> int:
    """Зберігає один документ, повертає 1 якщо успішно, інакше 0."""
    title = doc.get("title") or f"doc_{int(time.time())}"
    filename = sanitize_filename(title)
    url = doc.get("url")
    if not url:
        logger(f"[warn] Пропущено – немає URL: {filename}")
        return 0

    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        logger(f"[skip] вже існує: {filename}")
        return 0

    try:
        r = fetch_with_retry(url)
        with open(path, "wb") as f:
            f.write(r.content)
        logger(f"[v] завантажено: {filename}")
        return 1
    except Exception as e:
        logger(f"[err] не вдалося завантажити {filename}: {e}")
        return 0


def save_participants_to_excel(participants: list, folder_path: str):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Учасники"
    ws.append(["Назва", "ЄДРПОУ/Ідентифікатор", "Країна", "Регіон"])
    for p in participants:
        ws.append([p["name"], p["id"], p["country"], p["region"]])
    wb.save(os.path.join(folder_path, "Учасники.xlsx"))


def extract_all_docs(item):
    """Рекурсивно знаходить усі dict із 'url' і 'title'."""
    if isinstance(item, dict):
        if "url" in item and "title" in item:
            yield item
        for v in item.values():
            yield from extract_all_docs(v)
    elif isinstance(item, list):
        for elem in item:
            yield from extract_all_docs(elem)


def download_documents_with_progress(
    user_input: str, progress_bar=None, logger: Callable[[str], None] = print
) -> int:
    # 1) Розпізнавання публічного номера
    if user_input.upper().startswith("UA-"):
        logger(f"[i] Шукаємо внутрішній ID за пуб. номером: {user_input}")
        tid = resolve_tender_id_by_public_number(user_input)
        if not tid:
            logger("[err] Тендер не знайдено.")
            return 0
        user_input = tid

    # 2) Отримуємо JSON тендеру
    logger(f"[i] Отримуємо тендер: {user_input}")
    try:
        resp = session.get(f"{BASE_URL}/{user_input}", timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logger(f"[err] Не вдалося отримати тендер: {e}")
        return 0

    data = resp.json().get("data", {})
    public_id = data.get("tenderID", user_input)

    # 3) Створюємо папки
    base_dir = os.path.join("downloads", sanitize_filename(public_id))
    tend_docs = os.path.join(base_dir, "Документи тендера")
    proc_docs = os.path.join(base_dir, "Процесуальні документи та аналіз")
    os.makedirs(tend_docs, exist_ok=True)
    os.makedirs(proc_docs, exist_ok=True)

    # Зберігаємо tender.json
    with open(os.path.join(base_dir, "tender.json"), "w", encoding="utf-8") as f:
        f.write(resp.text)

    # 4) Збираємо всі документи у список завдань
    tasks: List[Tuple[dict, str]] = []
    seen_urls = set()
    participants = []

    def add_docs(docs_list, folder):
        os.makedirs(folder, exist_ok=True)
        for d in docs_list:
            url = d.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                tasks.append((d, folder))

    # 4.1) Загальні документи тендеру
    add_docs(
        list(extract_all_docs(data.get("documents", []))),
        os.path.join(tend_docs, "Загальні документи"),
    )

    # 4.2) Документи учасників (bids)
    for bid in data.get("bids", []):
        tenderer = bid.get("tenderers", [{}])[0]
        name = tenderer.get("name", "Учасник без назви")
        ident = tenderer.get("identifier", {}).get("id", "—")
        part_base = os.path.join(tend_docs, sanitize_filename(f"{name}_{ident}"))
        # створюємо всі підпапки учасника
        for sub in (
            "documents",
            "selfEligibleDocuments",
            "selfQualifiedDocuments",
            "requirementResponses",
            "lotValues",
        ):
            os.makedirs(os.path.join(part_base, sub), exist_ok=True)
        # додаємо всі документи учасника у відповідні підпапки
        for doc in extract_all_docs(bid):
            url = doc.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                tasks.append((doc, part_base))
        participants.append(
            {
                "name": name,
                "id": ident,
                "country": tenderer.get("address", {}).get("countryName", "—"),
                "region": tenderer.get("address", {}).get("region", "—"),
            }
        )

    # 4.3) Інші секції тендеру
    sections = [
        ("awards", "Нагороди"),
        ("contracts", "Контракти"),
        ("qualifications", "Кваліфікації"),
        ("complaints", "Скарги"),
        ("cancellations", "Скасування"),
        ("clarifications", "Роз’яснення"),
        ("questions", "Питання"),
    ]
    for key, folder_name in sections:
        objs = data.get(key, [])
        target = os.path.join(tend_docs, folder_name)
        os.makedirs(target, exist_ok=True)
        add_docs(list(extract_all_docs(objs)), target)
        # complaints всередині awards/contracts/qualifications
        if key in ("awards", "contracts", "qualifications"):
            for o in objs:
                add_docs(list(extract_all_docs(o.get("complaints", []))), target)

    # 5) Зберігаємо список учасників
    if participants:
        save_participants_to_excel(participants, base_dir)

    # 6) Створюємо папки для процесуальних документів
    for sub in ("вимоги", "подання про попередні висновки", "проект рішення", "Аналіз"):
        os.makedirs(os.path.join(proc_docs, sub), exist_ok=True)

    # 7) Послідовне завантаження з прогрес-баром
    total = len(tasks)
    logger(f"[i] Завантаження {total} файлів по черзі…")
    count = 0
    for i, (doc, folder) in enumerate(tasks, start=1):
        count += save_doc(doc, folder, logger)
        if progress_bar:
            progress_bar.progress(i / max(total, 1))
    logger(f"[done] Завершено. '{public_id}' — {count} файлів завантажено.")
    return count

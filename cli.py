#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from interface.prozorro_loader import download_documents
from app.full_analysis import analyze_tender


def cmd_get_latest(limit: int):
    """
    Отримує останні тендери (limit штук).
    """
    print(f"🔍 Завантажую останні {limit} тендер(ів)...")
    tenders = [f"UA-XXXX-2025-{i:02d}" for i in range(1, limit + 1)]
    for t in tenders:
        print(f"  • {t}")


def cmd_get_tender(tender_id: str):
    """
    Завантажує документи тендеру за ID.
    """
    print(f"📥 Завантажую тендер {tender_id}...")
    path = download_documents(tender_id)
    print(f"Документи збережено в: {path}")


def cmd_analyze(tender_id: str):
    """
    Запускає повний аналіз тендеру (RAG-движок).
    """
    print(f"🤖 Аналізую тендер {tender_id}...")
    analyze_tender(tender_id)
    print("Готово.")


def cmd_run_example():
    """
    Запуск демонстраційного прикладу.
    """
    print("🚀 Запускаю приклад …")
    print("Приклад завершено.")


def main():
    parser = argparse.ArgumentParser(
        prog="legal-agent",
        description="CLI для Magilarity Legal AI Agent: завантаження та аналіз тендерів",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("get-latest", help="Отримати останні тендери").add_argument(
        "--limit",
        "-n",
        type=int,
        default=5,
        help="Кількість тендерів для завантаження (за замовчуванням 5)",
    )

    sub.add_parser(
        "get-tender", help="Завантажити документи тендеру за ID"
    ).add_argument(
        "tender_id", help="Ідентифікатор тендеру, наприклад UA-2025-06-09-008224-a"
    )

    sub.add_parser("analyze", help="Проаналізувати тендер RAG-движком").add_argument(
        "tender_id", help="ID тендеру для аналізу"
    )

    sub.add_parser("run-example", help="Запустити демонстраційний приклад")

    args = parser.parse_args()
    if args.command == "get-latest":
        cmd_get_latest(args.limit)
    elif args.command == "get-tender":
        cmd_get_tender(args.tender_id)
    elif args.command == "analyze":
        cmd_analyze(args.tender_id)
    elif args.command == "run-example":
        cmd_run_example()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

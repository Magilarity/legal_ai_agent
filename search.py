import sys
from sqlalchemy import text
from db.schema import Session

def ft_search(section_name: str, fts_table: str, data_table: str, title_col: str, query: str, limit: int):
    print(f"\n=== {section_name} ===")
    session = Session()
    sql = text(f"""
      SELECT d.id AS id,
             d.{title_col} AS title,
             snippet({fts_table}, -1, '<b>','</b>','...',10) AS snippet
      FROM {fts_table}
      JOIN {data_table} AS d ON {fts_table}.rowid = d.id
      WHERE {fts_table} MATCH :q
      LIMIT :lim
    """)
    rows = session.execute(sql, {"q": query, "lim": limit})
    found = False
    for r in rows:
        found = True
        print(f"{r.id}\t{r.title}\n  …{r.snippet}\n")
    if not found:
        print("Нічого не знайдено.")

def main():
    if len(sys.argv) < 2:
        print('Usage: python search.py "query" [limit]')
        sys.exit(1)

    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    # 1. Тендери (documents/documents_fts)
    ft_search(
        section_name="Tenders",
        fts_table="documents_fts",
        data_table="documents",
        title_col="title",
        query=query,
        limit=limit
    )

    # 2. Законодавчі акти (legal_acts/legal_acts_fts)
    ft_search(
        section_name="Legal Acts",
        fts_table="legal_acts_fts",
        data_table="legal_acts",
        title_col="title",
        query=query,
        limit=limit
    )

    # 3. Рішення (decisions/decisions_fts)
    ft_search(
        section_name="Decisions",
        fts_table="decisions_fts",
        data_table="decisions",
        title_col="decision_id",
        query=query,
        limit=limit
    )

    # 4. Консультації (consultations/consultations_fts)
    ft_search(
        section_name="Consultations",
        fts_table="consultations_fts",
        data_table="consultations",
        title_col="consult_id",
        query=query,
        limit=limit
    )

if __name__ == "__main__":
    main()
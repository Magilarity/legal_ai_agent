from db.schema import Base, ENGINE

from .schema import Base, ENGINE

def init_db():
    Base.metadata.create_all(ENGINE)
    print("✅ Database & FTS5 table created.")

if __name__ == "__main__":
    init_db()
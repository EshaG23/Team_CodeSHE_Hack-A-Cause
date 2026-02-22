import sqlite3
from pathlib import Path

# All files are in the same folder (flat structure)
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "krishijalmitra.db"
SCHEMA_PATH = ROOT / "schema.sql"


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

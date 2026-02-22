"""
Create/initialize SQLite DB for KrishiJalMitra.
Run from your folder:  python init_db.py
"""
from db import init_db

if __name__ == "__main__":
    init_db()
    print("Database initialized: krishijalmitra.db")

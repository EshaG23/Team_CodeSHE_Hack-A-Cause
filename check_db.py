import sqlite3

conn = sqlite3.connect('krishijalmitra.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('Tables:', tables)

if tables:
    cursor.execute('SELECT * FROM farmers LIMIT 5')
    rows = cursor.fetchall()
    print('Sample data:', rows)

conn.close()

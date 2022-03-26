import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute(f"select url from blocks")
alls = [''.join(i) for i in cursor.fetchall()]

print(alls)
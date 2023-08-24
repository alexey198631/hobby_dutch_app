import sqlite3
import datetime

conn = sqlite3.connect('utils/dehet.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dehet (
        trial INTEGER PRIMARY KEY,
        date TEXT,
        de_points INTEGER,
        de_total INTEGER,
        het_points INTEGER,
        het_total INTEGER,
        points INTEGER,
        total INTEGER,
        rate REAL,
        total_time INTEGER
    )
''')

conn.close()
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('data_files/words.db')
cursor = conn.cursor()

cursor.execute("ALTER TABLE words ADD COLUMN word_index INTEGER")

cursor.execute("SELECT rowid FROM words")
rows = cursor.fetchall()

for i, row in enumerate(rows, start=1):
    cursor.execute("UPDATE words SET word_index = ? WHERE rowid = ?", (i, row[0]))
conn.commit()

# Сохранение изменений и закрытие соединения
conn.close()

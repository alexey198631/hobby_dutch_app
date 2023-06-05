import sqlite3
from translate import Translator

# Connect to the SQLite database
db_path = 'data_files/spanish/words.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Retrieve the values from the 'translation' column where 'russian' column is 0
cursor.execute("SELECT translation FROM words WHERE russian = 0")
translations = cursor.fetchall()

# Translate each value from English to Russian and update the 'russian' column
translator = Translator(from_lang='en', to_lang='ru')

for translation in translations:
    english_translation = translation[0]
    russian_translation = translator.translate(english_translation)

    # Update the 'russian' column with the translated value
    cursor.execute("UPDATE words SET russian = ? WHERE translation = ?", (russian_translation, english_translation))
    conn.commit()

# Close the database connection
conn.close()
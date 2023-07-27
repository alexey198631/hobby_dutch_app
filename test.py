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


def help_for_guess(word, r):  # r - number of letters
    list_of_word = list(word)
    copy = list_of_word.copy()
    for j in range(len(list_of_word)):
        if list_of_word[j] == ' ':
            copy.remove(list_of_word[j])

    ls = random.sample(copy, k=r)

    for i in range(len(list_of_word)):
        if list_of_word[i] in ls:
            list_of_word[i] = list_of_word[i]
        else:
            list_of_word[i] = '_'
    back = ' '.join(list_of_word)

    return back


def nine_nine_nine(sample, sample_weights):
    print('\n')
    count = 0
    for w in sample:
        if round(sample_weights[w.getWord()], 1) > round(w.getWeight(), 1):
            count += 1
        print(w.getWord(), '=', round(sample_weights[w.getWord()], 1), '->', round(w.getWeight(), 1))
    print(f'Progress for {count} words from {len(sample)}. Good job!')


def xlstosql(df):
    df_name = df.name
    # connect to the SQLite database
    conn = sqlite3.connect(f'data_files/{df_name}.db')
    # insert the data from the dataframe into the database table
    df.to_sql(f'{df_name}', conn, if_exists='replace', index=False)
    # close the database connection
    conn.close()


def word_list_to_print(sample):
    temp = []
    final = []
    for w in sample:
        if w.getTyp() is None:
            temp.append(w)
        else:
            try:
                math.isnan(w.getTyp())
                temp.append(w)
            except:
                if re.search(r'de', w.getTyp()) and not re.search(r'het', w.getTyp()):
                    final.append('de ' + str(w.getWord()) + ": " + str(w.getTranslation()))
                elif re.search(r'het', w.getTyp()) and not re.search(r'de', w.getTyp()):
                    final.append('het ' + str(w.getWord()) + ": " + str(w.getTranslation()))
                elif re.search(r'het', w.getTyp()) and re.search(r'de', w.getTyp()):
                    final.append('de/het ' + str(w.getWord()) + ": " + str(w.getTranslation()))
                else:
                    final.append(str(w.getWord()) + ": " + str(w.getTranslation()))
    for t in temp:
        final.append(str(t.getWord()) + ": " + str(t.getTranslation()))
    return final
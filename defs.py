# all app logic is here
import pandas as pd
import math
import re
import sqlite3
from cls import *
from word_plot import *
from global_language import GlobalLanguage, Difficulty


def sql_text(dffty, limit, wl=100, exm='no'):
    if exm != 'no':
        wd = 'difficulty'
    else:
        wd = 'wd'
    text = f"""
    SELECT word, type, translation, russian, example, example_translation, appear, trial_d, trial_r, success, weight, word_index, difficulty, wd
    FROM words
    WHERE {wd} = {dffty} AND weight <= {wl}
    ORDER BY weight DESC, RANDOM()
    LIMIT {limit};
    """
    return text


def loadData(source, final='no', exam='no'):
    # connect to the SQLite database and read the data into a pandas dataframe
    conn = sqlite3.connect(GlobalLanguage.file_path + f'/{source}s.db')

    if source == 'word' and final == 'no' and exam == 'no':
        cursor = conn.cursor()
        # Sample words from each difficulty level based on difficulty and weight
        selected_words = []
        for difficulty, count in Difficulty.difficulty_distribution.items():
            # Retrieve 5 easy words
            words_query = sql_text(difficulty, count)
            cursor.execute(words_query)
            selected_words = selected_words + cursor.fetchall()
        # close the database connection
        conn.close()
        return selected_words
    elif source == 'word' and exam == 'yes':
        cursor = conn.cursor()
        length, weight = Difficulty.difficulty_distribution
        # Execute the SQL query
        cursor.execute(f"SELECT * FROM words WHERE weight <= {weight}")
        # Fetch all the rows
        rows = cursor.fetchall()
        # Extract values from the 'word_index' column and store in a list
        word_index_list = [row[11] for row in rows]
        # Choose 'n' = length random indexes from the list
        random_indexes = random.sample(range(len(word_index_list)), length)
        # Retrieve the corresponding rows using the random indexes
        selected_words = [rows[index] for index in random_indexes]
        # close the database connection
        cursor.close()
        conn.close()
        return selected_words
    if source == 'lesson':
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT r FROM {source}s")
        results = cursor.fetchall()
        list_of_lessons = []
        for row in results:
            if row[0] != 999:
                list_of_lessons.append(row[0])
        # close the database connection
        conn.close()
        return list_of_lessons,  max(list_of_lessons) + 1


def sql_verbs_text():
    text = f"""
    SELECT verb, translation, past_singular, past_participle, appear, trial_d, trial_r, success, weight, time_spent
    FROM verbs
    ORDER BY weight DESC, RANDOM()
    LIMIT 25;
    """
    return text


def loadVerbsData(source): # data frame from xlsx file with verbs, it creates list of class Verbs
    # connect to the SQLite database and read the data into a pandas dataframe
    conn = sqlite3.connect(GlobalLanguage.file_path + f'/{source}s.db')
    cursor = conn.cursor()
    selected_words = []
    words_query = sql_verbs_text()
    cursor.execute(words_query)
    selected_words = selected_words + cursor.fetchall()
    # close the database connection
    conn.close()
    return selected_words


def loadWords(words_data):  # data frame from xlsx file with words, it creates list of class Words
    list_of_words = []
    for row in words_data:
        word = Words(*row)
        list_of_words.append(word)
    return list_of_words


def loadVerbs(words_data):
    list_of_words = []
    for row in words_data:
        word = Verbs(*row)
        list_of_words.append(word)
    return list_of_words


def no_space(word):
    lst = []
    for w in word:
        lst.append(w.strip())
    return lst


def translation_with_comma(translation):
    try:
        translation = translation.split(',')
        translation = no_space(translation)
        return translation

    except:
        return [translation]


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


def list_to_list(lst):
    st = ''
    for w in lst:
        st = st + w + '; '
    st.strip()
    st = st[0:(len(st) - 2)]
    return st


def lesson_length(list_of_words):
    lesson_length_ = 0
    for w in list_of_words:
        temp = w.getWord()
        temp = temp.replace(' ', '')
        lesson_length_ += len(temp)
    return lesson_length_


def next_lesson(lesson_df):
    s_l = set(lesson_df.r)
    s_l = list(s_l)
    for i in s_l:
        if i == 999:
            s_l.remove(i)
    return s_l, max(s_l) + 1


def random_sample(list_of_words, n):
    sample = random.choices(list_of_words, weights=[w.getWeight() for w in list_of_words], k=n)
    ln = n
    st = len(set([x.getWord() for x in sample]))
    count = 0
    while ln != st:
        #print('count = ', count, 'len = ', ln, 'set = ', st)
        sample = random.choices(list_of_words, weights=[w.getWeight() for w in list_of_words], k=n)
        st = len(set([x.getWord() for x in sample]))
        count += 1
    return sample


def get_lesson_words(lesson_number):

    if lesson_number != 999:

        conn = sqlite3.connect(GlobalLanguage.file_path + 'lessons.db')
        cursor = conn.cursor()

        conn2 = sqlite3.connect(GlobalLanguage.file_path + 'words.db')
        cursor2 = conn2.cursor()

        cursor.execute(f"SELECT r, list_of_words FROM lessons WHERE r = {lesson_number}")
        results = cursor.fetchall()[0]

        result_list = []

        r, list_of_words = results
        number_list = list_of_words.split(';')
        for number in number_list:
            word_index = int(number)
            cursor2.execute("SELECT word, type, translation, russian, example, example_translation, appear, trial_d, trial_r, success, weight, word_index, difficulty, wd FROM words WHERE word_index = ?", (word_index,))
            word_result = cursor2.fetchone()
            if word_result is not None:
                result_list.append(word_result)

        conn.close()
        conn2.close()

    else:

        conn = sqlite3.connect(GlobalLanguage.file_path + 'lessons.db')
        cursor = conn.cursor()

        conn2 = sqlite3.connect(GlobalLanguage.file_path + 'words.db')
        cursor2 = conn2.cursor()

        cursor.execute(f"SELECT list_of_words FROM lessons")
        results = cursor.fetchall()

        index_list = []

        for list_of_words in results:
            list_of_words = str(list_of_words[0])
            number_list = list_of_words.split(';')
            for number in number_list:
                number = int(number)
                index_list.append(number)
        index_list = list(set(index_list))

        #index_list = random.sample(index_list, k=25)

        result_list = []

        text = """
                SELECT word, type, translation, russian, example, example_translation, appear, trial_d, trial_r, success, weight, word_index, difficulty, wd
                FROM words
                WHERE word_index = ?;
                """
        cnt = 0
        for index in index_list:
            word_index = int(index)
            cursor2.execute(text, (word_index,))
            word_result = cursor2.fetchone()
            if word_result[-4] > 60.0 and cnt != 25:
                result_list.append(word_result)
                cnt += 1

    conn.close()
    conn2.close()
    return result_list


def reps(repeat, lesson_df, wordList):
    s_repeat = []
    check_existence = []
    words_from_lesson = lesson_df.list_of_words
    lesson_to_repeat = lesson_df[lesson_df['r'] == repeat].index[0]

    lesson_words = words_from_lesson[lesson_to_repeat].split(";")
    for cw in lesson_words:
        cw = cw.strip()
        for w in wordList:
            if w.getWord() == cw and w.getWord() not in check_existence:
                s_repeat.append(w)
                check_existence.append(w.getWord())
    return s_repeat


def all_learned(lesson_df, wordList):
    allwords = []
    s_repeat = []
    words_from_lesson = lesson_df.list_of_words

    for i in range(len(words_from_lesson)):
        allwords = allwords + words_from_lesson[i].split(";")
    for j in range(len(words_from_lesson)):
        allwords[j] = allwords[j].strip()

    for cw in allwords:
        cw = cw.strip()
        for w in wordList:
            if w.getWord() == cw:
                s_repeat.append(w)

    s_repeat = set(s_repeat)
    s_repeat = list(s_repeat)

    return s_repeat


def for_inter_time(df, lessonNumber, known):
    ln = lessonNumber.getNumber()
    kt = lessonNumber.getInterTime()
    lessn = df.copy()
    lessn = lessn.assign(inter_pts=lambda x: ((lessn['inter'] - lessn['start'])))
    lessn['points'] = lessn['inter_pts'].apply(lambda x: x.seconds)

    row = lessn.index.values[-1] + 1

    lessn.loc[row, 'lesson'] = ln
    lessn.loc[row, 'start'] = 0
    lessn.loc[row, 'inter'] = 0
    lessn.loc[row, 'finish'] = 0
    lessn.loc[row, 'known'] = known
    lessn.loc[row, 'points'] = kt
    lessn.loc[row, 'length'] = 0
    lessn.loc[row, 'time'] = 0
    lessn.loc[row, 'list_of_words'] = 0
    lessn.loc[row, 'r'] = ln

    return lessn


def place(t=0, cond=0):

    conn = sqlite3.connect(GlobalLanguage.file_path + 'lessons.db')
    cursor = conn.cursor()

    # Get the known value of the last row
    cursor.execute("SELECT known, level FROM lessons ORDER BY rowid DESC LIMIT 1")
    result = cursor.fetchone()
    if result is not None:
        rep = result[0]
        dif = result[1]


    # Prepare the base SQL query
    if rep != 25:
        sql = f"SELECT * FROM lessons WHERE known != 25 AND level == '{dif}'"
    else:
        sql = f"SELECT * FROM lessons WHERE known == 25 AND level == '{dif}'"

    # Execute the SQL query
    cursor.execute(sql)

    # Fetch all the rows
    data = cursor.fetchall()

    last_lesson = data[-1][-2]

    # Sort the data by points in descending order and enumerate to assign places
    data.sort(key=lambda row: row[5], reverse=True)
    data = [(index + 1, row[9], row[7], row[5]) for index, row in enumerate(data)]

    # Find the place of the last row
    last_row = next((row for row in data if row[1] == last_lesson), None)
    last_place = last_row[0]
    current_index = last_place - 1

    # Get the best lessons and ensure the last lesson is included if not already in the top 10
    best_lessons = data[:10]
    if last_place > 10:
        best_lessons.append(last_row)
        # index for making bold
        current_index = 10

    # Format the data for output
    best_lessons = [('Lesson ' + str(row[1]), row[2], row[3], row[0]) for row in best_lessons]
    columns_names = ['Lesson', 'Time', 'Points', 'Place']

    # Close the connection
    conn.close()

    return best_lessons, columns_names, dif, current_index


def initial_weight(sample):
    sample_weights = {}
    for w in sample:
        sample_weights[w.getWord()] = w.getWeight()
    print('\n')
    for w in sample:
        print(w.getWord(), '=', round(w.getWeight(), 1))
    print('\n')
    return sample_weights


def nine_nine_nine(sample, sample_weights):
    print('\n')
    count = 0
    for w in sample:
        if round(sample_weights[w.getWord()], 1) > round(w.getWeight(), 1):
            count += 1
        print(w.getWord(), '=', round(sample_weights[w.getWord()], 1), '->', round(w.getWeight(), 1))
    print(f'Progress for {count} words from {len(sample)}. Good job!')


def bottom_not_repeated():
    difficulty = Difficulty.difficulty
    conn = sqlite3.connect(GlobalLanguage.file_path + f'/lessons.db')
    cursor = conn.cursor()

    # Prepare the SQL query
    sql = f"""
    SELECT r AS Lesson, time AS Time, points AS Points
    FROM (
        SELECT r, time, points
        FROM (
            SELECT r, time, points, 
            ROW_NUMBER() OVER(PARTITION BY r ORDER BY points DESC) rn
            FROM lessons
            WHERE level = '{difficulty}' -- Additional condition
        )
        WHERE rn = 1
        ORDER BY points ASC
        LIMIT 10
    )
    """

    # Execute the SQL query
    cursor.execute(sql)

    # Fetch all the rows
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert the data into the required format
    data = [('Lesson ' + str(lesson), time, pts) for lesson, time, pts in data]
    column_names = ['Lesson', 'Time', 'Pts']

    return data, column_names


def topbottom(top=1):
    difficulty = Difficulty.difficulty
    conn = sqlite3.connect(GlobalLanguage.file_path + f'/lessons.db')
    cursor = conn.cursor()
    # Prepare the basic SQL query
    sql = "SELECT r AS Lesson, time AS Time, points AS Pts, level as Difficulty FROM lessons"

    # Add conditions to the SQL query based on the top parameter
    if top != 'overall':
        sql += f" WHERE known != 25 AND level = '{difficulty}'"
    if top == 0:
        sql += " ORDER BY Pts ASC, Time DESC LIMIT 10"
    elif top == 'all' or top == 'overall':
        pass
    else:
        sql += " ORDER BY Pts DESC, Time ASC LIMIT 10"

    # Execute the SQL query
    cursor.execute(sql)
    # Fetch all the rows
    data = cursor.fetchall()
    # Close the connection
    conn.close()
    # Convert the data into the required format
    data = [('Lesson ' + str(lesson), time, pts, level) for lesson, time, pts, level in data]
    column_names = ['Lesson', 'Time', 'Pts', 'Difficulty']

    return data, column_names


def xlstosql(df):
    df_name = df.name
    # connect to the SQLite database
    conn = sqlite3.connect(f'data_files/{df_name}.db')
    # insert the data from the dataframe into the database table
    df.to_sql(f'{df_name}', conn, if_exists='replace', index=False)
    # close the database connection
    conn.close()


def final_creation_sql(wordList, lessonNumber):

    # Connect to the SQLite database
    conn = sqlite3.connect(GlobalLanguage.file_path + 'words.db')
    cursor = conn.cursor()
    indexes = [word.getWordIndex() for word in wordList]

    for k, i in enumerate(indexes):
        v1 = wordList[k].getAppear()
        v2 = wordList[k].getTrials_d()
        v3 = wordList[k].getTrials_r()
        v4 = wordList[k].getSuccess()
        v5 = wordList[k].getWeight()
        wordList[k].updateWeight()
        v6 = wordList[k].getWD()

        cursor.execute(
            "UPDATE words SET appear = ?, trial_d = ?, trial_r = ?, success = ?, weight = ?,  wd = ?  WHERE word_index = ?",
            (v1, v2, v3, v4, v5, v6, i))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    conn = sqlite3.connect(GlobalLanguage.file_path + 'lessons.db')
    cursor = conn.cursor()

    cursor.execute("SELECT lesson FROM lessons WHERE lesson IS NOT NULL ORDER BY lesson DESC LIMIT 1")
    try:
        last_lesson = cursor.fetchone()[0]
    except:
        last_lesson = 0
    l1 = last_lesson + 1
    l2 = lessonNumber.getStart()
    l3 = lessonNumber.getInter()
    l4 = lessonNumber.getFinish()
    l5 = lessonNumber.getNumber_of_easy()
    l6 = lessonNumber.getPoints()
    l7 = lessonNumber.getLength_of_lesson()
    l8 = lessonNumber.getTime()
    l9 = list_to_list(lessonNumber.getList())
    l10 = lessonNumber.getNumber()
    l11 = lessonNumber.getLevel()

    cols = 'lesson, start, inter, finish, known, points, length, time, list_of_words, r, level'
    cursor.execute(f"INSERT INTO lessons ({cols}) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11))
    conn.commit()
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


def example_list_to_print(sample):
    final = []
    for w in sample:
        if w.getExample_nl() is None:
            pass
        else:
            final.append(str(w.getWord()) + ' -> ' + str(w.getExample_nl()) + ' -> ' + str(w.getExample_en()) + '\n')
    return final


def todefault():

    # connect to the SQLite database
    conn = sqlite3.connect(GlobalLanguage.file_path + 'words.db')
    cursor = conn.cursor()

    columns = ['appear', 'trial_d', 'trial_r', 'success', 'weight']

    # Generate and execute the UPDATE statements
    for column in columns:
        if column != 'weight':
            update_query = f"UPDATE words SET {column} = 0;"
            cursor.execute(update_query)
        else:
            update_query = f"UPDATE words SET {column} = 100.0;"
            cursor.execute(update_query)

    text = """

        UPDATE words
            SET wd = CASE
                WHEN difficulty = 0 THEN 1
                ELSE difficulty + ABS(RANDOM()) % 3 + 1
            END;

        """
    cursor.execute(text)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # connect to the SQLite database
    conn2 = sqlite3.connect(GlobalLanguage.file_path + 'lessons.db')
    cursor2 = conn2.cursor()
    delete_query = "DELETE FROM lessons;"
    cursor2.execute(delete_query)
    # Commit the changes and close the connection
    conn2.commit()
    conn2.close()


def repeat_difficulty(words):
    total_sum = sum(w.getWD() for w in words)

    if total_sum < 124:
        return 'easy'
    elif total_sum < 148:
        return 'standard'
    elif total_sum < 171:
        return 'hard'
    else:
        return 'very hard'

def exam_sql(exam_date, size, prcnt, words, lang, total_weight):
    # Connect to the database
    conn = sqlite3.connect(GlobalLanguage.file_path + 'exams.db')
    cursor = conn.cursor()
    # Determine the values for the new row
    next_n = cursor.execute('SELECT MAX(n) FROM exams').fetchone()[0] + 1

    # Insert the new row into the 'exams' table
    cursor.execute("INSERT INTO exams (n, date, size, prcnt, words, lang, total_weight) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (next_n, exam_date, size, prcnt, words, lang, total_weight))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def total_exam_words():
    # Connect to the SQLite database
    conn = sqlite3.connect(GlobalLanguage.file_path + 'words.db')
    cursor = conn.cursor()

    # Execute the SQL query to count rows where weight >= 50
    cursor.execute('SELECT COUNT(*) FROM words WHERE weight <= 50')

    # Fetch the count value from the cursor
    row_count = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    return row_count

    print(f"Number of rows where weight >= 50: {row_count}")


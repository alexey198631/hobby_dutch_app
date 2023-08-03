from datetime import datetime
import re
import math
from utils.database_connection import DatabaseConnection
from utils.global_cls import *



def sql_text(dffty, limit, wl=100, exm='no'):

    if exm != 'no':
        wd = 'difficulty'
    else:
        wd = 'wd'

    # Check if wd has a specific value or should include all values
    if dffty != 'ANY':
        condition = f"{wd} = {dffty}"
    else:
        condition = "1=1"  # This will always evaluate to true and include all rows


    text = f"""
    SELECT word, type, translation, russian, example, example_translation, appear, trial_d, trial_r, success, weight, word_index, difficulty, wd
    FROM words
    WHERE {condition} AND weight <= {wl}
    ORDER BY weight DESC, RANDOM()
    LIMIT {limit};
    """
    return text


def loadData(source, final='no', exam='no'):
    with DatabaseConnection(f'{source}s.db') as conn:

        if source == 'word' and final == 'no' and exam == 'no':
            cursor = conn.cursor()
            # Sample words from each difficulty level based on difficulty and weight
            selected_words = []
            for difficulty, count in Difficulty.difficulty_distribution.items():
                # Retrieve 5 words
                words_query = sql_text(difficulty, count)
                cursor.execute(words_query)
                selected_words = selected_words + cursor.fetchall()

            # sometimes words with some level of difficulty can come to 0, so it is necessary to add other random words
            qty = len(selected_words)
            if qty != 25:
                lim = 25 - qty
                words_query = sql_text('ANY', lim)
                cursor.execute(words_query)
                selected_words = selected_words + cursor.fetchall()
            return selected_words

        elif source == 'word' and exam == 'yes':
            cursor = conn.cursor()
            length, weight = Difficulty.difficulty_distribution

            # Execute the SQL query
            cursor.execute(f"SELECT * FROM words WHERE weight <= {weight}")
            # Fetch all the rows
            rows = cursor.fetchall()
            if len(rows) == 0:
                weight = 100.0
                cursor.execute(f"SELECT * FROM words WHERE weight <= {weight}")
                rows = cursor.fetchall()
            # Extract values from the 'word_index' column and store in a list
            word_index_list = [row[11] for row in rows]
            # Choose 'n' = length random indexes from the list
            random_indexes = random.sample(range(len(word_index_list)), length)
            # Retrieve the corresponding rows using the random indexes
            selected_words = [rows[index] for index in random_indexes]
            return selected_words
        if source == 'lesson':
            cursor = conn.cursor()
            cursor.execute(f"SELECT DISTINCT r FROM {source}s")
            results = cursor.fetchall()
            list_of_lessons = []
            for row in results:
                if row[0] != 999:
                    list_of_lessons.append(row[0])
    return list_of_lessons,  max(list_of_lessons) + 1


def sql_verbs_text():
    text = f"""
    SELECT verb_index, verb, translation, past_singular, past_participle, appear, trial_d, trial_r, success, weight
    FROM verbs
    ORDER BY weight DESC, RANDOM()
    LIMIT 5;
    """
    return text


def loadVerbsData(source): # data frame from xlsx file with verbs, it creates list of class Verbs
    with DatabaseConnection(f'/{source}s.db') as conn:
        cursor = conn.cursor()
        selected_words = []
        words_query = sql_verbs_text()
        cursor.execute(words_query)
        selected_words = selected_words + cursor.fetchall()
        list_of_verbs = []
        for row in selected_words:
            verb = Verbs(*row)
            list_of_verbs.append(verb)
    return list_of_verbs


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


def get_lesson_words(lesson_number):

    with DatabaseConnection('lessons.db') as conn:
        cursor = conn.cursor()
        if lesson_number != 999:
            cursor.execute(f"SELECT r, list_of_words FROM lessons WHERE r = {lesson_number}")
            results = cursor.fetchall()[0]
            result_list = []
            r, list_of_words = results
            number_list = list_of_words.split(';')
            with DatabaseConnection('words.db') as conn2:
                for number in number_list:
                    cursor2 = conn2.cursor()
                    word_index = int(number)
                    cursor2.execute("SELECT word, type, translation, russian, example, example_translation, appear, "
                                    "trial_d, trial_r, success, weight, word_index, difficulty, wd FROM words WHERE word_index = ?", (word_index,))
                    word_result = cursor2.fetchone()
                    if word_result is not None:
                        result_list.append(word_result)
        else:
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
            result_list = []
            text = """
                           SELECT word, type, translation, russian, example, example_translation, appear, trial_d, trial_r, success, weight, word_index, difficulty, wd
                           FROM words
                           WHERE word_index = ?;
                           """
            cnt = 0
            with DatabaseConnection('words.db') as conn2:
                cursor2 = conn2.cursor()
                for index in index_list:
                    word_index = int(index)
                    cursor2.execute(text, (word_index,))
                    word_result = cursor2.fetchone()
                    if word_result[-4] > 60.0 and cnt != 25:
                        result_list.append(word_result)
                        cnt += 1

    return result_list


def hardestVerbs():
    with DatabaseConnection('verbs.db') as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM verbs WHERE weight != 100.0"
        # Execute the SQL query
        cursor.execute(sql)
        # Fetch all the rows
        data = cursor.fetchall()
        # Sort the data by points in descending order and enumerate to assign places
        data.sort(key=lambda row: row[9], reverse=True)
        data = [(row[2], row[1], row[5], row[9]) for row in data]
        worst_verbs = data[:10]
        columns_names = ['Verb', 'Translation', 'Appearance', 'Weight']

    return worst_verbs, columns_names


def place(t=0, cond=0):
    with DatabaseConnection('lessons.db') as conn:
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
        if last_place == 0:
            current_index = 1
        else:
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

    return best_lessons, columns_names, dif, current_index


def bottom_not_repeated():
    difficulty = Difficulty.difficulty
    with DatabaseConnection('/lessons.db') as conn:
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
        # Convert the data into the required format
        data = [('Lesson ' + str(lesson), time, pts) for lesson, time, pts in data]
        column_names = ['Lesson', 'Time', 'Pts']
        if len(data) == 0:
            data = [('None', 0, 0)]

    return data, column_names


def topbottom(top=1):
    difficulty = Difficulty.difficulty
    with DatabaseConnection('/lessons.db') as conn:
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
        # Convert the data into the required format
        data = [('Lesson ' + str(lesson), time, pts, level) for lesson, time, pts, level in data]
        column_names = ['Lesson', 'Time', 'Pts', 'Difficulty']
        if len(data) == 0:
            data = [('None', 0, 0)]

    return data, column_names


def final_creation_sql(wordList, lessonNumber):
    with DatabaseConnection('words.db') as conn:
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

    with DatabaseConnection('lessons.db') as conn:
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


def example_list_to_print(sample):
    final = []
    for w in sample:
        if w.getExample_nl() is None:
            pass
        else:
            final.append(str(w.getWord()) + ' -> ' + str(w.getExample_nl()) + ' -> ' + str(w.getExample_en()) + '\n')
    return final


def todefault():
    with DatabaseConnection('words.db') as conn:

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

    with DatabaseConnection('lessons.db') as conn2:
        cursor2 = conn2.cursor()
        delete_query = "DELETE FROM lessons;"
        cursor2.execute(delete_query)

    with DatabaseConnection('exams.db') as conn4:
        cursor4 = conn4.cursor()
        delete_query = "DELETE FROM exams;"
        cursor4.execute(delete_query)

    with DatabaseConnection('verbs.db') as conn3:
        cursor = conn3.cursor()
        columns = ['appear', 'trial_d', 'trial_r', 'success', 'weight']

        # Generate and execute the UPDATE statements
        for column in columns:
            if column != 'weight':
                update_query = f"UPDATE verbs SET {column} = 0;"
                cursor.execute(update_query)
            else:
                update_query = f"UPDATE verbs SET {column} = 100.0;"
                cursor.execute(update_query)


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
    with DatabaseConnection('exams.db') as conn:
        cursor = conn.cursor()
        # Determine the values for the new row
        if cursor.execute('SELECT MAX(n) FROM exams').fetchone()[0] is None:
            next_n = 1
        else:
            next_n = cursor.execute('SELECT MAX(n) FROM exams').fetchone()[0] + 1

        # Insert the new row into the 'exams' table
        cursor.execute("INSERT INTO exams (n, date, size, prcnt, words, lang, total_weight) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (next_n, exam_date, size, prcnt, words, lang, total_weight))


def verbs_sql(verbList):
    with DatabaseConnection('verbs.db') as conn:
        cursor = conn.cursor()
        indexes = [verb.getVerbIndex() for verb in verbList]
        for k, i in enumerate(indexes):
            v1 = verbList[k].getAppear()
            v2 = verbList[k].getTrials_d()
            v3 = verbList[k].getTrials_r()
            v4 = verbList[k].getSuccess()
            v5 = verbList[k].getWeight()
            verbList[k].updateWeight()

            cursor.execute(
                "UPDATE verbs SET appear = ?, trial_d = ?, trial_r = ?, success = ?, weight = ? WHERE verb_index = ?",
                (v1, v2, v3, v4, v5, i))


def total_exam_words():
    with DatabaseConnection('words.db') as conn:
        cursor = conn.cursor()
        # Execute the SQL query to count rows where weight >= 50
        cursor.execute('SELECT COUNT(*) FROM words WHERE weight <= 50')
        # Fetch the count value from the cursor
        row_count = cursor.fetchone()[0]

    return row_count


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


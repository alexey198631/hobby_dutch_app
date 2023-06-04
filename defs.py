# all app logic is here
import pandas as pd
import math
import re
import sqlite3
from cls import *
from word_plot import *
from global_language import GlobalLanguage, Difficulty


def initial_load() -> object:  # load data from init file - xlsx with words
    """

    :rtype: object
    """
    words = pd.read_excel('data_files/init_words.xlsx', sheet_name='words')
    lesson_df = pd.DataFrame()
    exist = 'no'

    return words, lesson_df, exist


def next_load():  # load data from existing file
    words = pd.read_excel('data_files/dutch.xlsx', sheet_name='update')
    words = words.loc[:, 'word':]
    lesson_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='lesson')
    lesson_df = lesson_df.loc[:, 'lesson':]
    verbs_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='verbs')
    verbs_df = verbs_df.loc[:, 'translation':]
    try:
        exam_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='exams')
        exam_df = exam_df.loc[:, 'n#':]

    except:
        exam_df = pd.DataFrame()
        exam_df['n#'] = 0
        exam_df['date'] = 0
        exam_df['size'] = 0
        exam_df['%'] = 0
        exam_df['words'] = 0
        exam_df['lang'] = 0

    exist = 'yes'

    return words, lesson_df, exist, exam_df, verbs_df


def sql_text(dffty, limit, wl=100):
    text = f"""
    SELECT word, type, translation, russian, example, example_translation, appear, trial_d, trial_r, success, weight, word_index, difficulty, wd
    FROM words
    WHERE wd = {dffty} AND weight <= {wl}
    ORDER BY weight DESC, RANDOM()
    LIMIT {limit};
    """
    return text


def loadData(source, final='no', exam='no'):
    # connect to the SQLite database and read the data into a pandas dataframe
    conn = sqlite3.connect(GlobalLanguage.file_path + f'/{source}s.db')

    if source == 'word' and final == 'no':
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
        # Sample words from each difficulty level based on difficulty and weight
        selected_words = []
        for difficulty, count in Difficulty.difficulty_distribution.items():
            # Retrieve 5 easy words
            words_query = sql_text(difficulty, count, wl=50)
            cursor.execute(words_query)
            selected_words = selected_words + cursor.fetchall()
        # close the database connection
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




def loadWords(words_data):  # data frame from xlsx file with words, it creates list of class Words
    list_of_words = []
    for row in words_data:
        word = Words(*row)
        list_of_words.append(word)
    return list_of_words


def loadVerbs(df_words):  # data frame from xlsx file with verbs, it creates list of class Verbs
    list_of_words = []
    for i in range(len(df_words)):
        list_of_words.append(
            Verbs(df_words.iloc[i, 1], df_words.iloc[i, 2], df_words.iloc[i, 3], df_words.iloc[i, 0],
                  df_words.iloc[i, 4],
                  df_words.iloc[i, 5], df_words.iloc[i, 6], df_words.iloc[i, 7], df_words.iloc[i, 8], df_words.iloc[i, 9]))
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


def right_word(word, translation, rever=0):
    point_counter = 0
    if rever == 1:
        while True:
            x = input(f'\nPress "1","2","3" to open 1, 2, 3 letters in the word\n\n {translation}: ')
            if x == word:
                return [True, point_counter]
            elif x == '1' or x == '2' or x == '3':
                print(help_for_guess(word, int(x)))
                point_counter += int(x)
            else:
                return [False, point_counter]

    elif rever == 0:
        translation = translation_with_comma(translation)
        while True:
            x = input(f'\nPress "1","2","3" to open 1, 2, 3 letters in the word\n\n {word}: ')
            if x in translation:
                return [True, point_counter]
            elif x == '1' or x == '2' or x == '3':
                print(help_for_guess(translation[0], int(x)))
                point_counter += int(x)
            else:
                return [False, point_counter]


def cycle(sample_of_words, rever):
    p = 250
    s = sample_of_words.copy()
    while len(s) > 0:
        random.shuffle(s)
        lst_to_delete = []
        for i in s:
            temp = right_word(i.getWord(), i.getTranslation(), rever)
            if temp[0]:
                print("\nRIGHT!")
                p = p - temp[1]
                i.addSuccess()
                if rever == 0:
                    i.addTrials_d()
                else:
                    i.addTrials_r()
                lst_to_delete.append(i)
            else:
                print("\nWRONG!")
                p = p - temp[1]
                p -= 1
                if rever == 0:
                    i.addTrials_d()
                else:
                    i.addTrials_r()
        if len(lst_to_delete) > 0:
            for w in lst_to_delete:
                s.remove(w)
            if len(s) != 0:
                plotting(s)
        else:
            if len(s) != 0:
                plotting(s)
    print(p,'\n')
    return p


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
    cursor.execute("SELECT known FROM lessons ORDER BY rowid DESC LIMIT 1")
    rep = cursor.fetchone()[0]

    # Prepare the base SQL query
    if rep != 25:
        sql = "SELECT * FROM lessons WHERE known != 25"
    else:
        sql = "SELECT * FROM lessons WHERE known == 25"

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

    # Get the best lessons and ensure the last lesson is included if not already in the top 10
    best_lessons = data[:10]
    if last_place > 10:
        best_lessons.append(last_row)

    # Format the data for output
    best_lessons = [('Lesson ' + str(row[1]), row[2], row[3], row[0]) for row in best_lessons]
    columns_names = ['Lesson', 'Time', 'Points', 'Place']

    # Close the connection
    conn.close()

    return best_lessons, columns_names


"""
def place(df, t=0, cond=0):
    lesson = df.copy()
    rep = int(lesson.loc[:, "known"][-1:].values[0])
    if rep != 25:
        mod_lesson = lesson[lesson.known != 25]
    else:
        mod_lesson = lesson[lesson.known == 25]

    if cond == 0:

        last = mod_lesson.loc[:, "r"][-1:].values[0]
        last_points = mod_lesson.loc[:, "points"][-1:].values[0]
        last_lesson = mod_lesson.tail(1)  # Extract the last row

        mod_lesson = mod_lesson.sort_values(by='points', ascending=False, ignore_index=True)
        place = mod_lesson[mod_lesson['points'] == last_points].index[0] + 1
        last_lesson['Place'] = place

        best_lessons = mod_lesson.head(10)
        best_lessons = best_lessons.reset_index()
        best_lessons = best_lessons.rename(columns={'index': 'Place'})
        best_lessons['Place'] = best_lessons['Place'] + 1

        if last not in best_lessons['r'].values:
            final_result = pd.concat([best_lessons, last_lesson], ignore_index=True)
        else:
            final_result = best_lessons

        final_result = final_result.loc[:, ['r', 'time', 'points', 'Place']]
        final_result = final_result.rename(columns={'r': 'Lesson', 'time': 'Time', 'points': 'Pts'})
        final_result['Place'] = final_result['Place'].astype(int)
        final_result['Lesson'] = final_result['Lesson'].astype(str)
        final_result['Lesson'] = 'Lesson ' + final_result['Lesson']

        return final_result

    elif cond != 0:
        last_points = mod_lesson.loc[:, "points"][-1:].values[0]
        mod_lesson = mod_lesson.sort_values(by='points', ascending=True, ignore_index=True)
        place = mod_lesson[mod_lesson['points'] == last_points].index[0]


        print(f'1. Lesson {mod_lesson.loc[0, "r"]:.0f} - {mod_lesson.loc[0, "points"]:.0f} sec \
                      \n2. Lesson {mod_lesson.loc[1, "r"]:.0f} - {mod_lesson.loc[1, "points"]:.0f} sec \
                      \n3. Lesson {mod_lesson.loc[2, "r"]:.0f} - {mod_lesson.loc[2, "points"]:.0f} sec \
                      \n------------------------ \
                      \n{t} sec, place {(place + 1):.0f}, difference {- int(mod_lesson.loc[0, "points"]) + int(t)} \
                      ')
"""

def final_creation(exist, words, wordList, lessonNumber, lesson_df, sample, exam_df, verbs_df):

    if exist == 'yes':
        dutch = words.copy()

        for i in range(len(dutch)):
            dutch.loc[i, 'appear'] = wordList[i].getAppear()
            dutch.loc[i, 'trial_d'] = wordList[i].getTrials_d()
            dutch.loc[i, 'trial_r'] = wordList[i].getTrials_r()
            dutch.loc[i, 'success'] = wordList[i].getSuccess()
            dutch.loc[i, 'weight'] = wordList[i].getWeight()
            dutch.loc[i, 'word_index'] = wordList[i].getWordIndex()
            dutch.loc[i, 'difficulty'] = wordList[i].getDifficulty()
            dutch.loc[i, 'wd'] = wordList[i].getWD()


        row = lesson_df.loc[:, 'lesson'][-1:].values[0]
        lesson_df.loc[row, 'lesson'] = lesson_df.loc[:, 'lesson'][-1:].values[0] + 1
        lesson_df.loc[row, 'start'] = lessonNumber.getStart()
        lesson_df.loc[row, 'inter'] = lessonNumber.getInter()
        lesson_df.loc[row, 'finish'] = lessonNumber.getFinish()
        lesson_df.loc[row, 'known'] = lessonNumber.getNumber_of_easy()
        lesson_df.loc[row, 'points'] = lessonNumber.getPoints()
        lesson_df.loc[row, 'length'] = lessonNumber.getLength_of_lesson()
        lesson_df.loc[row, 'time'] = lessonNumber.getTime()
        lesson_df.loc[row, 'list_of_words'] = list_to_list(lessonNumber.getList())
        lesson_df.loc[row, 'r'] = lessonNumber.getNumber()

    else:

        dutch = words.copy()

        dutch['appear'] = 0
        dutch['trial_d'] = 0
        dutch['trial_r'] = 0
        dutch['success'] = 0
        dutch['weight'] = 100

        for i in range(len(dutch)):
            dutch.loc[i, 'appear'] = wordList[i].getAppear()
            dutch.loc[i, 'trial_d'] = wordList[i].getTrials_d()
            dutch.loc[i, 'trial_r'] = wordList[i].getTrials_r()
            dutch.loc[i, 'success'] = wordList[i].getSuccess()
            dutch.loc[i, 'weight'] = wordList[i].getWeight()
            dutch.loc[i, 'word_index'] = wordList[i].getWordIndex()
            dutch.loc[i, 'difficulty'] = wordList[i].getDifficulty()
            dutch.loc[i, 'wd'] = wordList[i].getWD()

        lesson_df['lesson'] = 0
        lesson_df['start'] = 0
        lesson_df['inter'] = 0
        lesson_df['finish'] = 0
        lesson_df['known'] = 0
        lesson_df['points'] = 0
        lesson_df['length'] = 0
        lesson_df['time'] = 0
        lesson_df['list_of_words'] = []

        lesson_df.loc[0, 'lesson'] = lessonNumber.getNumber()
        lesson_df.loc[0, 'start'] = lessonNumber.getStart()
        lesson_df.loc[0, 'inter'] = lessonNumber.getInter()
        lesson_df.loc[0, 'finish'] = lessonNumber.getFinish()
        lesson_df.loc[0, 'known'] = lessonNumber.getNumber_of_easy()
        lesson_df.loc[0, 'points'] = lessonNumber.getPoints()
        lesson_df.loc[0, 'length'] = lessonNumber.getLength_of_lesson()
        lesson_df.loc[0, 'time'] = lessonNumber.getTime()
        lesson_df.loc[0, 'list_of_words'] = list_to_list(lessonNumber.getList())
        lesson_df.loc[0, 'r'] = lessonNumber.getNumber()

    writer = pd.ExcelWriter('data_files/dutch.xlsx', engine='xlsxwriter')
    dutch.to_excel(writer, sheet_name='update')
    lesson_df.to_excel(writer, sheet_name='lesson')
    exam_df.to_excel(writer, sheet_name='exams')
    verbs_df.to_excel(writer, sheet_name='verbs')
    writer.save()

    temp = []
    for w in sample:
        try:
            math.isnan(w.getTyp())
            temp.append(w)
        except:
            if re.search(r'de', w.getTyp()) and not re.search(r'het', w.getTyp()):
                print('de', w)
            elif re.search(r'het', w.getTyp()) and not re.search(r'de', w.getTyp()):
                print('het', w)
            elif re.search(r'het', w.getTyp()) and re.search(r'de', w.getTyp()):
                print('de/het', w)
            else:
                print(w)
    for t in temp:
        print(t)

    print('\n', 'EXAMPLES', '\n')

    for w in sample:
        try:
            math.isnan(w.getExample_nl())
        except:
            print(w.getWord(), '->', w.getExample_nl(), '->', w.getExample_en(), '\n')

    print('Lesson #:', lessonNumber.getNumber(), 'time spent:', lessonNumber.getTime(), 'points: ',
          lessonNumber.getPoints(), '\n')


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
    conn = sqlite3.connect(GlobalLanguage.file_path + f'/lessons.db')
    cursor = conn.cursor()

    # Prepare the SQL query
    sql = """
    SELECT r AS Lesson, time AS Time, points AS Points
    FROM (
        SELECT r, time, points
        FROM (
            SELECT r, time, points, 
            ROW_NUMBER() OVER(PARTITION BY r ORDER BY points DESC) rn
            FROM lessons
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
    conn = sqlite3.connect(GlobalLanguage.file_path + f'/lessons.db')
    cursor = conn.cursor()
    # Prepare the basic SQL query
    sql = "SELECT r AS Lesson, time AS Time, points AS Pts FROM lessons"

    # Add conditions to the SQL query based on the top parameter
    if top != 'overall':
        sql += " WHERE known != 25"
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
    data = [('Lesson ' + str(lesson), time, pts) for lesson, time, pts in data]
    column_names = ['Lesson', 'Time', 'Pts']

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



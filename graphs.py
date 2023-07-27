"""
This code determines quantity of learned words to dates.
Then it creates graph x-axis: Date, y-axes: Number of learned words

"""
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

conn = sqlite3.connect('data_files/lessons.db')
# Replace 'your_table_name' with the name of the table containing the data you want to export
query = "SELECT * FROM lessons"
df = pd.read_sql_query(query, conn)

# Replace 'output_file.xlsx' with the desired name for the Excel file
output_file = 'data_files/dutch.xlsx'

# Replace 'dutch' with the desired name for the sheet
sheet_name = 'lesson'

# Save the DataFrame to Excel
df.to_excel(output_file, sheet_name=sheet_name, index=False)

conn.close()

# import data from existing leaning file with lesson sheet
lesson_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='lesson')


def words_progress(df):
    lesson = df.copy()
    # extraction necessary information only - date of lesson finish and list of words
    data_words_lesson_df = lesson.loc[:, ['finish', 'list_of_words']]
    data_words_lesson_df['finish'] = pd.to_datetime(data_words_lesson_df['finish'], format="%Y-%m-%d %H:%M:%S.%f")
    data_words_lesson_df.reset_index(inplace=True)
    data_words_lesson_df['date'] = data_words_lesson_df['finish'].apply(lambda x: x.strftime("%d.%m.%Y"))
    data_words_lesson_df = data_words_lesson_df.loc[:, ['date', 'list_of_words']]
    data_words_lesson_df['date'] = pd.to_datetime(data_words_lesson_df['date'], format='%d.%m.%Y')

    start_date = data_words_lesson_df.loc[0, 'date']
    end_date = data_words_lesson_df['date'].iloc[-1]

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    df_dates = pd.DataFrame(date_range, columns=['date'])
    data_words_lesson_df = pd.merge(df_dates, data_words_lesson_df, on='date', how='left')
    data_words_lesson_df['list_of_words'].fillna(0, inplace=True)

    data_words_lesson_df['total_words'] = 0

    # list for unique learned words
    new_learned_words = list()

    # determination quantity of unique words learned up to date
    for i in range(len(data_words_lesson_df)):
        if data_words_lesson_df.loc[i, 'list_of_words'] != 0:
            temp = data_words_lesson_df.loc[i, 'list_of_words'].split(";")
            for cw in temp:
                if cw.strip() not in new_learned_words:
                    new_learned_words.append(cw.strip())
            data_words_lesson_df.loc[i, 'total_words'] = len(new_learned_words)
        else:
            data_words_lesson_df.loc[i, 'total_words'] = len(new_learned_words)

    # extraction necessary information only - date and quantity of unique words, keeping only final number per day
    data_words_lesson_df = data_words_lesson_df.loc[:, ['date', 'total_words']]
    mask = data_words_lesson_df.duplicated(subset='date', keep='last')
    df = data_words_lesson_df[~mask]
    df = df.reset_index()

    df['date'] = df['date'].dt.strftime('%d.%m.%Y')

    # plotting results on a graph
    plt.figure(figsize=(16, 10), dpi=80)
    plt.get_current_fig_manager().set_window_title('Words per Date')
    plt.bar(df['date'], df['total_words'], color='orange')
    plt.grid(linestyle='--', color='blue', alpha=.3)
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Words Total')

    # addition values to bars, I add quantity of new words learned day by day
    for i in range(len(df)):
        if i == 0:
            plt.text(x=i, y=df.loc[i, 'total_words'], s=df.loc[i, 'total_words'], ha='center', va='bottom',
                     color='black', size=8)
        else:
            plt.text(x=i, y=df.loc[i, 'total_words'], s=df.loc[i, 'total_words'] - df.loc[i - 1, 'total_words'],
                     ha='center', va='bottom', color='black', size=8)

    current_time = datetime.now().strftime("%d_%m_%Y")

    plt.savefig(f'data_files/words_graph_{current_time}.png', dpi=300, bbox_inches='tight')
    plt.show()


#words_progress(lesson_df)


def lesson_progress(df):

    data_words_lesson_df = df.copy()
    data_words_lesson_df['relative_known'] = data_words_lesson_df['known'] / 25 * data_words_lesson_df['points']
    data_words_lesson_df = data_words_lesson_df.loc[:, ['finish', 'points', 'known', 'r', 'relative_known']]
    data_words_lesson_df['finish'] = pd.to_datetime(data_words_lesson_df['finish'], format="%Y-%m-%d %H:%M:%S.%f")
    data_words_lesson_df['date'] = data_words_lesson_df['finish'].apply(lambda x: x.strftime("%d.%m.%Y"))
    conseq = data_words_lesson_df[data_words_lesson_df['known'] != 25]
    conseq = conseq.reset_index()
    sort = conseq.sort_values(by='points', ascending=True)
    sort = sort.reset_index()

    # index of the last lesson
    last = int(conseq['r'].values[-1])
    last_sort = int(sort.index[sort['r'] == last].tolist()[0])

    # determine max points lesson
    sort_max_pts = sort['points'].values[-1]
    sort_min_pts = sort['points'].values[0]
    max_pts_ind = int(sort.index[sort['points'] == sort_max_pts].tolist()[0])
    min_pts_ind = int(sort.index[sort['points'] == sort_min_pts].tolist()[0])
    # for conseq dataframe
    max_pts_ind_con = int(conseq.index[conseq['points'] == sort_max_pts].tolist()[0])
    min_pts_ind_con = int(conseq.index[conseq['points'] == sort_min_pts].tolist()[0])

    # plotting results on a graph
    plt.figure(figsize=(16, 10), dpi=80)
    plt.get_current_fig_manager().set_window_title('Points graphs')

    # create the first subplot
    ax = plt.subplot(2, 1, 1)

    # plot the first bar graph
    for i, d in enumerate(conseq['points']):
        color = 'lightgrey'
        if i == last - 1:  # highlight the last bar
            color = 'plum'
        elif i == max_pts_ind_con:
            color = 'gold'
        ax.bar(i, d, color=color)

    for i, d in enumerate(conseq['relative_known']):
        color = 'darkgrey'
        ax.bar(i, d, color=color)

    for i in range(len(conseq)):
        if i == max_pts_ind_con or i == min_pts_ind_con or i == (len(conseq) - 1):
            plt.text(x=i, y=conseq.loc[i, 'points'] + 10, s=conseq.loc[i, 'points'], ha='center', va='bottom',
                     color='black', size=7, rotation=90)

    plt.grid(linestyle='--', color='lightgrey', alpha=.2)
    plt.legend(['Consequent'], loc="upper left")
    plt.xlabel('lesson#')
    plt.ylabel('points')

    # adding the average
    plt.axhline(y=np.nanmean(conseq['points']), color='blue', linewidth=0.2, label='Avg')
    # trend line
    x = np.array(range(len(conseq)))
    y = np.poly1d(np.polyfit(x, conseq['points'], 1))(x)
    ax.plot(x, y, color='black', alpha=.2)  # linestyle='--'

    # create the second subplot
    ax2 = plt.subplot(2, 1, 2)
    # plot the second bar graph
    for i, d in enumerate(sort['points']):
        color = 'lightblue'
        if i == last_sort:  # highlight the last lesson bar
            color = 'blue'
        ax2.bar(i, d, color=color)

    for i in range(len(sort)):
        if i == max_pts_ind or i == min_pts_ind or i == last_sort:
            plt.text(x=i, y=sort.loc[i, 'points'] + 10, s=sort.loc[i, 'points'], ha='center', va='bottom',
                     color='black', size=7, rotation=90)

    plt.legend(['Sorted'], loc="upper left")
    plt.grid(linestyle='--', color='lightgrey', alpha=.2)
    plt.xticks(rotation=90)
    plt.ylabel('points')

    # show the plot
    current_time = datetime.now().strftime("%d_%m_%Y")
    plt.savefig(f'data_files/graph_{current_time}_lesson_{last}.png', dpi=300, bbox_inches='tight')
    plt.show()


#lesson_progress(lesson_df)
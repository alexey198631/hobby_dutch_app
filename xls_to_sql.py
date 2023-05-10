"""
This script is for transfering database of my app from xlsx format to sqllite db
"""

import pandas as pd
import sqlite3

# read the Excel file into a pandas dataframe
df = pd.read_excel('data_files/dutch.xlsx', sheet_name='lesson')
df = df.loc[:, 'lesson':]
df.name = 'lessons'

words = pd.read_excel('data_files/dutch.xlsx', sheet_name='update')
words = words.loc[:, 'word':]
words.name = 'words'
lesson_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='lesson')
lesson_df = lesson_df.loc[:, 'lesson':]
lesson_df.name = 'lessons'
verbs_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='verbs')
verbs_df = verbs_df.loc[:, 'translation':]
verbs_df.name = 'verbs'
exam_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='exams')
exam_df = exam_df.loc[:, 'n':]
exam_df.name = 'exams'

list_of_df = [words, lesson_df, verbs_df, exam_df]



def xlstosql(df):
    df_name = df.name

    # connect to the SQLite database
    conn = sqlite3.connect(f'data_files/{df_name}.db')

    # create a dictionary of column names and data types
    column_types = {}
    for col in df.columns:
        col_type = str(df[col].dtype)
        if col_type == 'object':
            col_type = 'TEXT'
        elif col_type.startswith('float'):
            col_type = 'REAL'
        elif col_type.startswith('int'):
            col_type = 'INTEGER'
        column_types[col] = col_type

    # create the table schema string
    table_schema = ', '.join([f'{col} {column_types[col]}' for col in df.columns])

    # create the table in the database
    conn.execute(f'CREATE TABLE {df_name} ({table_schema})')

    # insert the data from the dataframe into the database table
    df.to_sql(f'{df_name}', conn, if_exists='append', index=False)

    # close the database connection
    conn.close()

#for df in list_of_df:
 #   xlstosql(df)

spanish = pd.read_excel('data_files/init_words_spanish.xlsx', sheet_name='update')
spanish = spanish.loc[:, 'word':]
spanish.name = 'spanish'
xlstosql(spanish)
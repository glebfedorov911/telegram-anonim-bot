import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print('Connection successful')
    except Error as e:
        print('Error connect')
        print(e)

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query executed successfully!')
    except Error as e:
        print('Error query')
        print(e)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print('Successfully!')
        return result
    except Error as e:
        print('Error read')
        print(e)

connection = create_connection("user.db")

# create_user_table = '''CREATE TABLE IF NOT EXISTS user_data(
#     id INTEGER PRIMARY KEY,
#     username TEXT UNIQUE NOT NULL,
#     id_user_who_get_message INTEGER DEFAULT 0,
#     find TEXT NOT NULL
# );'''
#
# execute_query(connection, create_user_table)
#
# cr = """REPLACE  INTO user_data (id, username, id_user_who_get_message, find) VALUES
# (43859289532, 'sdshfjsd', 0, 'True'),
# (1233421, 'asdsd', 0, 'True')"""
#
# execute_query(connection, cr)
#
# cr = """REPLACE  INTO user_data (id, username, id_user_who_get_message, find) VALUES
# (5378343, 'sfhkjsdhfjkdsf', 0, "True")"""
#
# execute_query(connection, cr)


select_all = 'SELECT * FROM user_data'
read = execute_read_query(connection, select_all)
for r in read:
    print(r)

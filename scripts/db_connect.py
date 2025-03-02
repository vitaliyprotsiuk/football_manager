import sqlite3

def connect_db():
    database_path = 'database\db'

    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    return cursor
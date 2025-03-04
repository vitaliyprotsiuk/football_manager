import sqlite3

from data.config import DB_PATH

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)

    def get_cursor(self):
        cursor = self.connection.cursor() # create cursor to make requests

        return cursor
    
    def close_connection(self):
        return self.connection.close()
    
    def commit(self):
        return self.connection.commit()


def create_connection():
    return Database()
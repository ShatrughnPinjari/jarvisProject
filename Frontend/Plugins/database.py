# Import module
import sqlite3
import os
from django.conf import settings


# Function to get SQLite connection
def get_connection():
    return sqlite3.connect(os.path.join(settings.BASE_DIR, 'Frontend\Data', 'chats.db'))


def add_data(query):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        table = "INSERT INTO ASSISTANT(QUERY, DATE_TIME) VALUES (?, datetime('now', 'localtime'))"
        cursor.execute(table, (query,))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def get_data():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        data = cursor.execute('SELECT * FROM ASSISTANT')
        table_head = [column[0] for column in data.description]
        print("{:<14} {:<79} {:<20}".format(*table_head))
        print()
        for row in data:
            print("{:<14} {:<79} {:<20}".format(*row))
    finally:
        cursor.close()
        conn.close()
import sqlite3
import os

def select_db_file():
    if os.path.exists("bot_data/bot_sch.db"):
        return "bot_data/bot_sch.db"
    else:
        os.makedirs("bot_data")
        db_path = "bot_data/bot_sch.db"
    return db_path

# Устанавливаем переменную для базы данных
database_path = select_db_file()
conn, cursor = None, None

def execute_query(query, params=()):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()

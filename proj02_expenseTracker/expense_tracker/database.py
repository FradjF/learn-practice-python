import sqlite3

DATABASE_PATH = "expenses.db"

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_PATH)
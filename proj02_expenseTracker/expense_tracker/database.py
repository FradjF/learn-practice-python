import sqlite3
from expense_tracker.configuration import DATABASE_PATH

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_PATH)

def initialize_database() -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY,
            amount INTEGER NOT NULL CHECK(amount>0),
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        );
    """)

    connection.commit()
    connection.close()

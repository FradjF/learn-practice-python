import sqlite3
from expense_tracker.configuration import DATABASE_PATH
from contextlib import contextmanager


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

@contextmanager
def database_connection(connection=None):
    """
        Manage the database connection lifecycle with context manager
        success: open → yield → SQL → commit → close
        failure: open → yield → exception → rollback → re-raise → close
    """
    owns_connection = connection is None
    if connection is None:
        connection = get_connection()

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if owns_connection:
            connection.close()
import sqlite3
from contextlib import contextmanager
from expense_tracker.db_config import load_config

def get_connection() -> sqlite3.Connection:
        return sqlite3.connect(load_config())

def initialize_database() -> None:

    with get_connection() as connection:
        cursor = connection.cursor()
        version = cursor.execute("""
            PRAGMA user_version
        """).fetchone()[0]

        if version < 1:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY,
                    amount INTEGER NOT NULL CHECK(amount>0),
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL
                );
            """)
            cursor.execute("""
                PRAGMA user_version = 1;
            """)

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
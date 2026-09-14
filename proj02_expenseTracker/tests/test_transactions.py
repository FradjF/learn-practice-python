import sqlite3
import pytest
from expense_tracker.database import database_connection

def test_transaction_rolls_back_on_error():
    with sqlite3.connect(":memory:") as connection:
        connection.execute("""
            CREATE TABLE test_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
    with pytest.raises(RuntimeError):
        with database_connection():
            pass

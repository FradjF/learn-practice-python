import pytest
import sqlite3

@pytest.fixture
def connection():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE expenses(
            id INTEGER PRIMARY KEY,
            amount INTEGER NOT NULL CHECK(amount>0),
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        );
    """)
    yield connection
    connection.close()
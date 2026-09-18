import sqlite3
from expense_tracker.service import get_total_spending

import pytest


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


def test_get_total_spending(connection):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO expenses(amount, category, description, date)
        VALUES(3000,'Groceries','Leclerc','2026-07-25')
    """)
    cursor.execute("""
            INSERT INTO expenses(amount, category, description, date)
            VALUES(6699,'Food','Restaurant','2026-08-02')
        """)
    cursor.execute("""
            INSERT INTO expenses(amount, category, description, date)
            VALUES(2500,'Food','Restaurant','2026-08-04')
        """)
    result = get_total_spending(connection)
    assert result == 12199


def test_get_total_spending_zero(connection):
    result = get_total_spending(connection)
    assert result == 0
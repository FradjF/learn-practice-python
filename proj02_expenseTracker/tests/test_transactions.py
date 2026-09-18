import pytest
from expense_tracker.database import database_connection
from expense_tracker.service import delete_expense

def test_transaction_rolls_back_on_error(connection):

    with pytest.raises(RuntimeError):
        with database_connection(connection) as dbc:
            dbc.execute("""
                INSERT INTO expenses(amount, category, description, date)
                VALUES(3000,'Groceries','Leclerc','2026-07-25')
            """)
            raise RuntimeError("Simulated failure")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")

    assert cursor.fetchall() == []

def test_service_delete_expense_true(connection):

    connection.execute("""
        INSERT INTO expenses(amount, category, description, date)
        VALUES(3000,'Groceries','Leclerc','2026-07-25')
    """)
    connection.commit()

    result = delete_expense(1, connection)
    assert result is True

def test_service_delete_expense_false(connection):

    connection.execute("""
        INSERT INTO expenses(amount, category, description, date)
        VALUES(3000,'Groceries','Leclerc','2026-07-25')
    """)
    connection.commit()
    result  = delete_expense(0, connection)
    assert result is False
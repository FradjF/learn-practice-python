import pytest

from expense_tracker.exceptions import PersistenceError
from expense_tracker.models import Expense
from expense_tracker.service import create_expense, delete_expense, update_expense
from expense_tracker.cli import add_expense, menu

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

def test_service_update_expense_true(connection):

    connection.execute("""
        INSERT INTO expenses(amount, category, description, date)
        VALUES(3000,'Groceries','Leclerc','2026-07-25')
    """)
    connection.commit()
    expense =  Expense(
        id = 1,
        amount= 9990,
        category="Groceries",
        description="Leclerc",
        date="2026-07-29"
    )
    result = update_expense(expense, connection)
    assert result is True

    row = connection.execute("""
            SELECT amount, category, description, date
            FROM expenses
            WHERE id = 1
        """).fetchone()

    assert row == (9990, "Groceries", "Leclerc", "2026-07-29")

def test_service_update_expense_false(connection):

    connection.execute("""
        INSERT INTO expenses(amount, category, description, date)
        VALUES(3000,'Groceries','Leclerc','2026-07-25')
    """)
    connection.commit()
    expense =  Expense(
        id = 0,
        amount= 9990,
        category="Groceries",
        description="Leclerc",
        date="2026-07-29"
    )
    result = update_expense(expense, connection)
    assert result is False

def test_service_persistence_error(monkeypatch):
    expense = Expense(
        id=0,
        amount=10000,
        category="Groceries",
        description="Cactus",
        date="2026-09-19"
    )
    def fake_create_expense(_expense:Expense, _connection):
        raise RuntimeError("Database exploded")

    monkeypatch.setattr("expense_tracker.service.repository.create_expense",
                        fake_create_expense)

    with pytest.raises(PersistenceError) as exc_info:
        create_expense(expense)

    assert isinstance(exc_info.value.__cause__, RuntimeError)
    assert str(exc_info.value.__cause__) == "Database exploded"

def test_cli_persistence_error(monkeypatch, capsys):

    inputs = iter(["1","0"])

    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    def fake_add_expense():
        raise PersistenceError("Unable to create expense. Please try again.")

    monkeypatch.setattr("expense_tracker.cli.add_expense",
                        fake_add_expense)

    menu()

    captured = capsys.readouterr()
    assert "Unable to create expense. Please try again." in captured.out
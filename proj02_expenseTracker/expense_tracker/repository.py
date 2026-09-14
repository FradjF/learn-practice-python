import sqlite3

from expense_tracker.models import Expense
from expense_tracker.database import database_connection, get_connection


def create_expense(expense: Expense, connection: sqlite3.Connection) -> None:
    """
        Add an expense to the expenses database
    """
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO expenses(amount, category, description, date)
        VALUES (?,?,?,?)
    """, (
        expense.amount,
        expense.category,
        expense.description,
        expense.date
    ))

def get_expenses() -> list[Expense]:
    """
        Get all expenses
    """
    with database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
        """)
        expenses = []
        for row in cursor.fetchall():
            expense = Expense(
                id=row[0],
                amount=row[1],
                category=row[2],
                description=row[3],
                date=row[4],
            )
            expenses.append(expense)

    return expenses

def get_expense(expense_id: int) -> Expense | None:
    """
        Get an expense by ID
    """
    with database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
            where id = ?
        """, (expense_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        expense = Expense(
            id=row[0],
            amount=row[1],
            category=row[2],
            description=row[3],
            date=row[4],
        )

    return expense

def update_expense(expense:Expense) -> None:
    """
        Updates an expense
    """
    with database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE expenses
            SET 
                amount = ?,
                category = ?,
                description = ?,
                date = ?
            WHERE id = ?
        """, (
            expense.amount,
            expense.category,
            expense.description,
            expense.date,
            expense.id
        ))

def delete_expense(expense_id: int, connection:sqlite3.Connection) -> None:
    """
        Delete an expense by ID
    """
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM expenses
        where id = ?
    """, (expense_id,))
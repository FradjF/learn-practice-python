import sqlite3
from expense_tracker.models import Expense
from expense_tracker.database import database_connection


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
    expense.id = cursor.lastrowid

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

def update_expense(expense:Expense, connection:sqlite3.Connection) -> bool:
    """
        Updates an expense
    """
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

    return cursor.rowcount > 0

def delete_expense(expense_id: int, connection:sqlite3.Connection) -> bool:
    """
        Delete an expense by ID
    """
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM expenses
        where id = ?
    """, (expense_id,))

    return cursor.rowcount > 0

def get_spending_by_category() -> list[tuple[str,int]]:
    with database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

        return cursor.fetchall()[0]

def get_total_spending(connection: sqlite3.Connection) -> int:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
    """)
    return cursor.fetchone()[0]

def get_total_spending_between(start_date: str, end_date:str) -> int:
    with database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """, (start_date, end_date))
        return cursor.fetchone()[0]

def get_total_spending_per_month() -> list[tuple[str, int]]:
    with database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', date) AS month,
                SUM(amount)
            FROM expenses
            GROUP BY month
            ORDER BY month
        """)
        return cursor.fetchall()

def get_top_categories_between(
    start_date: str,
    end_date: str,
    limit: int
) -> list[tuple[str, int]]:
    with database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT category, SUM(amount) as total_amount
        FROM expenses
        WHERE date >= ? AND date <= ?
        GROUP BY category
        ORDER BY total_amount DESC
        LIMIT ?
        
        """, (start_date, end_date, limit))

        return cursor.fetchall()

def get_sql_db_schema_version():
    conn = sqlite3.connect("expenses.db")
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    print(version)

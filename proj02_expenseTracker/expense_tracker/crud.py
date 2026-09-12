from expense_tracker.database import get_connection
from expense_tracker.models import Expense

def create_expense(expense: Expense) -> None:
    """
        Add an expense to the expenses database
    """
    connection = get_connection()
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

    connection.commit()
    connection.close()

def get_expenses() -> list[Expense]:
    """
        Get all expenses
    """
    connection = get_connection()
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

    connection.close()
    return expenses

def get_expense(expense_id: int) -> Expense | None:
    """
        Get an expense by ID
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
        where id = ?
    """, (expense_id,))
    row = cursor.fetchone()
    if row is None:
        connection.close()
        return None
    expense = Expense(
        id=row[0],
        amount=row[1],
        category=row[2],
        description=row[3],
        date=row[4],
    )
    connection.close()
    return expense

def update_expense(
        expense_id:int,
        amount:int,
        category:str,
        description: str,
        date:str
) -> None:
    """
        Updates an expense
    """
    connection = get_connection()
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
        amount,
        category,
        description,
        date,
        expense_id
    ))
    print(cursor.rowcount)
    connection.commit()
    connection.close()

def delete_expense(expense_id: int) -> None:
    """
        Delete an expense by ID
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM expenses
        where id = ?
    """, (expense_id,))
    connection.commit()
    connection.close()
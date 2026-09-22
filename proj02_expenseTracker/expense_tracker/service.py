import sqlite3
import logging
from expense_tracker.exceptions import ValidationError
from expense_tracker.models import Expense
from expense_tracker.validations import validate_amount, validate_category, validate_description, validate_date
from expense_tracker import repository
from expense_tracker.database import database_connection
from expense_tracker.exceptions import PersistenceError

logger = logging.getLogger(__name__)

def create_expense(expense: Expense) -> None:
    validate_amount(expense.amount)
    validate_category(expense.category)
    validate_description(expense.description)
    validate_date(expense.date)
    with database_connection() as connection:
        try:
            repository.create_expense(expense, connection)
            logger.info("Expense created successfully: ID: %s - amount: %s - category: %s - description: %s - date: %s",
                        expense.id,expense.amount, expense.category, expense.description, expense.date)
        except Exception as exc:
            logger.exception("Database error while creating the new expense.")
            raise PersistenceError("Unable to create expense.") from exc

def update_expense(expense: Expense, connection: sqlite3.Connection | None = None) -> bool:
    validate_amount(expense.amount)
    validate_category(expense.category)
    validate_description(expense.description)
    validate_date(expense.date)

    with database_connection(connection) as dbc:
        return repository.update_expense(expense, dbc)

def get_expenses() -> list[Expense]:
    return repository.get_expenses()

def get_expense(expense_id: int) -> Expense | None:
    return repository.get_expense(expense_id)

def delete_expense(expense_id: int, connection: sqlite3.Connection | None = None) -> bool:
    with database_connection(connection) as dbc:
        return repository.delete_expense(expense_id, dbc)

def replace_expense(old_expense_id: int, new_expense:Expense) -> None:
    validate_amount(new_expense.amount)
    validate_category(new_expense.category)
    validate_description(new_expense.description)
    validate_date(new_expense.date)

    with database_connection() as connection:
        repository.delete_expense(old_expense_id, connection)
        repository.create_expense(new_expense, connection)

def get_spending_by_category() -> list[tuple[str,int]]:
    return repository.get_spending_by_category()

def get_total_spending(connection: sqlite3.Connection) -> int:
    result = repository.get_total_spending(connection)
    if result is None:
        return 0
    return result

def get_total_spending_between(start_date: str, end_date:str) -> int|None:
    validate_date(start_date)
    validate_date(end_date)

    if start_date > end_date:
        raise ValidationError("Start date must be before or equal to end date.")
    result = repository.get_total_spending_between(start_date, end_date)
    if result is None:
        return 0
    return result

def get_total_spending_per_month() -> list[tuple[str, int]]:
    return repository.get_total_spending_per_month()

def get_top_categories_between(
    start_date: str,
    end_date: str,
    limit: int
) -> list[tuple[str, int]] | None:

    validate_date(start_date)
    validate_date(end_date)
    if start_date > end_date:
        raise ValidationError("Start date must be before or equal to end date.")

    if limit < 1:
        raise ValidationError("List limit must be at least 1.")

    return repository.get_top_categories_between(start_date, end_date, limit)

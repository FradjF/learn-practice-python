from expense_tracker.models import Expense
from expense_tracker.validations import validate_amount, validate_category, validate_description, validate_date
from expense_tracker import repository
from expense_tracker.database import database_connection

def create_expense(expense: Expense) -> None:
    validate_amount(expense.amount)
    validate_category(expense.category)
    validate_description(expense.description)
    validate_date(expense.date)

    repository.create_expense(expense)

def update_expense(expense: Expense) -> None:
    validate_amount(expense.amount)
    validate_category(expense.category)
    validate_description(expense.description)
    validate_date(expense.date)

    repository.update_expense(expense)

def get_expenses() -> list[Expense]:
    return repository.get_expenses()

def get_expense(expense_id: int) -> Expense | None:
    return repository.get_expense(expense_id)

def delete_expense(expense_id: int) -> None:
    repository.delete_expense(expense_id)


def replace_expense(old_expense_id, new_expense):
    validate_amount(new_expense.amount)
    validate_category(new_expense.category)
    validate_description(new_expense.description)
    validate_date(new_expense.date)

    with database_connection() as connection:
        repository.delete_expense(old_expense_id, connection)
        raise RuntimeError("Simulation failure.")
        repository.create_expense(new_expense, connection)
from expense_tracker.exceptions import ValidationError
from expense_tracker.models import Expense
from expense_tracker.database import initialize_database
from expense_tracker.service import replace_expense, create_expense


def main():
    initialize_database()
    try:
        expense = Expense(
            id=0,
            amount=100,
            category="Food",
            description="",
            date="2026-08-44"
        )
        replace_expense(2, expense)
    except ValidationError as error:
        print(f"Error: {error}")



if __name__ == "__main__":
    main()
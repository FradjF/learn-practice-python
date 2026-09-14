from expense_tracker.models import Expense
from expense_tracker.database import initialize_database
from expense_tracker.service import replace_expense


def main():
    initialize_database()
    expense = Expense(
        id=0,
        amount=7799,
        category="Food",
        description="Restaurant",
        date="2026-08-02"
    )
    replace_expense(1, expense)



if __name__ == "__main__":
    main()
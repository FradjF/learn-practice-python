from expense_tracker.database import initialize_database
from expense_tracker.cli import list_expenses, display_expense, remove_expense


def main():
    initialize_database()
    print("\n******************** Welcome to Expense Tracker ********************\n")
    list_expenses()
    remove_expense()



if __name__ == "__main__":
    main()
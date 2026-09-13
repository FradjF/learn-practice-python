from expense_tracker.crud import create_expense, get_expense
from expense_tracker.database import initialize_database
from expense_tracker.models import Expense

def main():
    initialize_database()
    #expense = Expense(0, 1750, "Rent", "Apartment", "2024-08-01")
    #create_expense(expense)
    print(get_expense(1))


if __name__ == "__main__":
    main()
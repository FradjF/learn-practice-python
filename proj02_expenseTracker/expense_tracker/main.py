#from expense_tracker.models import Expense
from expense_tracker.crud import create_expense, get_expense, update_expense, delete_expense

def main() -> int:
    #expense = Expense(0,2400, "Rent", "Apartment rent", "2026-09-01")
    #create_expense(expense)
    delete_expense(999)
    print(get_expense(999))

if __name__ == "__main__":
    main()
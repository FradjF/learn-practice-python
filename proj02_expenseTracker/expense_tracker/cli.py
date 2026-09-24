from expense_tracker.exceptions import ValidationError, PersistenceError
from expense_tracker.models import Expense
from expense_tracker.service import create_expense, update_expense, get_expenses, get_expense, delete_expense

def add_expense() -> None:
    while True:
        try:
            amount = int(input("Enter a new expense amount: "))
            break
        except ValueError:
            print("The expense amount must be an integer.")

    category = input("Enter the category: ")
    description = input("Enter the description: ")
    date = input("Enter the date: ")

    expense = Expense(0, amount, category, description, date)

    try:
        create_expense(expense)
    except ValidationError as exc:
        print(f"Error: {exc}")
        return

    print("New expense successfully created.")

def modify_expense() -> None:

    while True:
        try:
            expense_id = int(input("Enter the ID of the expense to be updated: "))
            break
        except ValueError:
            print("The ID must be a positive integer.")

    while True:
        try:
            amount = int(input("Enter a new expense amount: "))
            break
        except ValueError:
            print("The expense amount must be an integer.")

    category = input("Enter the category: ")
    description = input("Enter the description: ")
    date = input("Enter the date: ")

    expense = Expense(expense_id, amount, category, description, date)

    try:
        update = update_expense(expense)
    except ValidationError as exc:
        print(f"Error: {exc}")
        return
    if update:
        print(f"Expense number {expense_id} updated successfully.")
    else:
        print(f"Expense number {expense_id} could not be found.")

def list_expenses() -> None:
    expenses = get_expenses()
    if not expenses:
        print("No expenses found.")
        return

    print(" ID | Amount |  Category  |   Description   |     Date    |")
    print("-" * 59)
    for expense in expenses:
        print(
            f"{expense.id:<2}  | "
            f"{expense.amount:<6} | "
            f"{expense.category:<10} | "
            f"{expense.description:<15} | "
            f"{expense.date:<11} |"
        )

def display_expense() -> None:
    while True:
        try:
            expense_id = int(input("Enter the ID of the expense to be displayed: "))
            break
        except ValueError:
            print("The ID must be an integer.")

    expense = get_expense(expense_id)
    if expense is None:
        print("This ID does not exist.")
        return

    print(" ID | Amount |  Category  |   Description   |    Date    |")
    print("-" * 58)
    print(
        f"{expense.id:<2}  | "
        f"{expense.amount:<6} | "
        f"{expense.category:<10} | "
        f"{expense.description:<15} | "
        f"{expense.date:<11}|"
    )

def remove_expense() -> None:
    while True:
        try:
            expense_id = int(input("Enter the ID of the expense to be deleted: "))
            break
        except ValueError:
            print("The ID must be an integer.")

    deleted = delete_expense(expense_id)
    if deleted:
        print(f"Expense ID:{expense_id} successfully deleted.")
    else:
        print(f"Expense ID:{expense_id} does not exist.")

def menu():
    print("\n******************** Welcome to Expense Tracker ********************\n")
    print("""
        Expense Tracker

        1. Add expense
        2. List expenses
        3. View expense
        4. Update expense
        5. Delete expense
        6. Reports
        0. Exit\n
        """)

    while True:
        try:
            option = int(input("Choose an option: "))
        except ValueError:
            print("Wrong number. Please try again.")
            continue

        if option == 1:
            try:
                add_expense()
            except PersistenceError:
                print("Unable to create expense. Please try again.")
        elif option == 2:
            list_expenses()
        elif option == 3:
            display_expense()
        elif option == 4:
            modify_expense()
        elif option == 5:
            remove_expense()
        elif option == 6:
            print("reports")
        elif option == 0:
            print("Exit confirmed. See you next time.")
            break
        else:
            print("Please choose an option between 0 and 6.")
        print("\n")
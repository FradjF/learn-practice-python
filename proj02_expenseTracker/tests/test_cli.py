from expense_tracker.models import Expense
from expense_tracker.cli import add_expense, menu




def test_add_expense(monkeypatch):
    inputs = iter([
        "10000",
        "Groceries",
        "Cactus",
        "2026-09-19"
    ])
    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    received_expense: Expense | None = None

    def fake_create_expense(expense: Expense):
        nonlocal received_expense
        received_expense = expense

    monkeypatch.setattr(
        "expense_tracker.cli.create_expense",
        fake_create_expense
    )

    add_expense()
    assert received_expense is not None
    assert received_expense.amount == 10000
    assert received_expense.category == "Groceries"
    assert received_expense.description == "Cactus"
    assert received_expense.date == "2026-09-19"

def test_add_expense_invalid_amount(monkeypatch):

    inputs = iter([
        "abc",
        "10000",
        "Groceries",
        "Cactus",
        "2026-09-19"
    ])
    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    received_expense = []

    def fake_create_expense(expense:Expense):
        nonlocal received_expense
        received_expense.append(expense)
    monkeypatch.setattr(
        "expense_tracker.cli.create_expense",
        fake_create_expense
    )
    add_expense()

    assert len(received_expense) == 1
    expense = received_expense[0]
    assert expense.amount == 10000
    assert expense.category =="Groceries"
    assert expense.description =="Cactus"
    assert expense.date =="2026-09-19"

"""
    Testing menu options with Separate tests give precise failure messages
"""
def test_menu_exit(monkeypatch):
    inputs = iter(["0"])

    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    menu()

def test_menu_add_expense(monkeypatch):
    inputs = iter(["1","0"]) #Adding the second input option '0'
                             #to stop the menu loop

    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    called = False

    def fake_add_expense():
        nonlocal called
        called = True

    monkeypatch.setattr("expense_tracker.cli.add_expense",
                        fake_add_expense
                        )

    menu()

    assert called is True

def test_menu_list_expenses(monkeypatch):
    inputs = iter(["2","0"]) #Adding the second input option '0'
                             #to stop the menu loop

    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    called = False

    def fake_list_expenses():
        nonlocal called
        called = True

    monkeypatch.setattr("expense_tracker.cli.list_expenses",
                        fake_list_expenses
                        )
    menu()

    assert called is True

def test_menu_display_expense(monkeypatch):

    inputs = iter(["3", "0"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _:next(inputs))

    called = False

    def fake_display_expense():
        nonlocal called
        called = True

    monkeypatch.setattr("expense_tracker.cli.display_expense",
                        fake_display_expense)

    menu()
    assert called is True

def test_menu_modify_expense(monkeypatch):
    inputs = iter(["4", "0"])
    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    called = False

    def fake_modify_expense():
        nonlocal called
        called = True

    monkeypatch.setattr("expense_tracker.cli.modify_expense",
                        fake_modify_expense)
    menu()
    assert called is True

def test_menu_remove_expense(monkeypatch):
    inputs = iter(["5", "0"])
    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    called = False

    def fake_remove_expense():
        nonlocal called
        called = True

    monkeypatch.setattr("expense_tracker.cli.remove_expense",
                        fake_remove_expense)
    menu()
    assert called is True

def test_menu_invalid_options(monkeypatch):
    inputs = iter(["9", "abc", "0"])
    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    called = False

    def fake_add_expense():
        nonlocal called
        called = True

    monkeypatch.setattr("expense_tracker.cli.add_expense",
                        fake_add_expense)

    menu()
    assert called is False

"""
    Testing menu options with one test is shorter and tests 
    the whole dispatch behavior together.
"""
def test_menu_first_suggestion(monkeypatch):
    inputs = iter(["1", "2", "3", "4", "5", "0"])
    monkeypatch.setattr("builtins.input", lambda _:next(inputs))

    called_options = {
        "add":False,
        "list":False,
        "display": False,
        "modify": False,
        "remove": False
    }

    def fake_add_expense():
        nonlocal called_options
        called_options["add"] = True

    def fake_list_expenses():
        nonlocal called_options
        called_options["list"] = True

    def fake_display_expense():
        nonlocal called_options
        called_options["display"] = True

    def fake_modify_expense():
        nonlocal called_options
        called_options["modify"] = True

    def fake_remove_expense():
        nonlocal called_options
        called_options["remove"] = True

    monkeypatch.setattr("expense_tracker.cli.add_expense",
                        fake_add_expense)
    monkeypatch.setattr("expense_tracker.cli.list_expenses",
                        fake_list_expenses)
    monkeypatch.setattr("expense_tracker.cli.display_expense",
                        fake_display_expense)
    monkeypatch.setattr("expense_tracker.cli.modify_expense",
                        fake_modify_expense)
    monkeypatch.setattr("expense_tracker.cli.remove_expense",
                        fake_remove_expense)
    menu()

    assert called_options["add"] is True
    assert called_options["list"] is True
    assert called_options["display"] is True
    assert called_options["modify"] is True
    assert called_options["remove"] is True

def test_menu_second_suggestion(monkeypatch):
    inputs = iter(["1", "2", "3", "4", "5", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    called_options = []

    def fake_add_expense():
        nonlocal called_options
        called_options.append("add")

    def fake_list_expenses():
        nonlocal called_options
        called_options.append("list")

    def fake_display_expense():
        nonlocal called_options
        called_options.append("display")

    def fake_modify_expense():
        nonlocal called_options
        called_options.append("modify")

    def fake_remove_expense():
        nonlocal called_options
        called_options.append("remove")

    monkeypatch.setattr("expense_tracker.cli.add_expense",
                        fake_add_expense)
    monkeypatch.setattr("expense_tracker.cli.list_expenses",
                        fake_list_expenses)
    monkeypatch.setattr("expense_tracker.cli.display_expense",
                        fake_display_expense)
    monkeypatch.setattr("expense_tracker.cli.modify_expense",
                        fake_modify_expense)
    monkeypatch.setattr("expense_tracker.cli.remove_expense",
                        fake_remove_expense)
    menu()

    assert called_options == ["add", "list", "display", "modify", "remove"]
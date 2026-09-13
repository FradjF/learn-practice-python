from expense_tracker.configuration import CATEGORIES
from datetime import datetime

def validate_amount(amount:int) -> None:
    if amount <= 0:
        raise ValueError("Amount must be greater than 0.")

def validate_category(category:str) -> None:
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

def validate_description(description:str) -> None:
    if description.strip() == "":
        raise ValueError(f"Invalid description: {description}")

def validate_date(date:str) -> None:
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Incorrect date format: {date}")


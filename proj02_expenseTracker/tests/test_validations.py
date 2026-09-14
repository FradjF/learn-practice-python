import pytest

from expense_tracker.exceptions import ValidationError
from expense_tracker.validations import (
    validate_date,
    validate_amount,
    validate_category,
    validate_description
)

def test_validate_amount_rejects_negative_amount():
    with pytest.raises(ValidationError):
        validate_amount(-100)

def test_validate_category_rejects_invalid_category():
    with pytest.raises(ValidationError):
        validate_category("Netflix")

def test_validate_description_reject_empty_description():
    with pytest.raises(ValidationError):
        validate_description("")

def test_validate_date_reject_invalid_date():
    with pytest.raises(ValidationError):
        validate_date("2026-02-31")
"""RASD FastAPI Organisations Model Unit Tests."""


# Third-Party
import pytest

# Local
from rasd_fastapi.models import organisations

# Typing
from typing import Any


@pytest.mark.parametrize(
    (
        "data",
        "valid",
    ),
    [
        # Valid
        ({"name": "A", "abn": "94 119 508 824", "email": "hello@example.com"},        True),   # Properly formatted ABN
        ({"name": "A", "abn": "50110219460", "email": "hello@example.com"},           True),   # No spaces in ABN
        ({"name": "A", "abn": " 5  1 82 4 75  3 556 ", "email": "hello@example.com"}, True),   # Too many spaces in ABN
        # Invalid
        ({"name": "A", "abn": "12345678910", "email": "hello@example.com"},          False),  # Wrong type for ABN
        ({"name": "A", "abn": "abc123", "email": "hello@example.com"},               False),  # Garbage ABN
        ({"name": "A", "abn": "12345678901", "email": "hello@example.com"},          False),  # Correct length, not ABN
        ({"name": "A"*201, "abn": "94 119 508 824", "email": "hello@example.com"},   False),  # Name too long
        ({"name": "A", "abn": "94 119 508 824", "email": "hello.example.com"},       False),  # Bad Email
        ({"name": "A", "abn": "94 119 508 824"},                                     False),  # Missing email
        ({"name": "A", "email": "hello@example.com"},                                False),  # Missing ABN
        ({"abn": "94 119 508 824", "email": "hello@example.com"},                    False),  # Missing name
    ]
)
def test_organisation_validation(data: dict[str, Any], valid: bool) -> None:
    """Tests the Organisation model validation.

    Args:
        data (dict[str, Any]): Data to to test validation of.
        valid (bool): Whether this organisation should be valid or not
    """
    # Handle Errors
    try:
        # Validate
        organisations.Organisation.validate(data)

    except (TypeError, ValueError):
        result = False

    else:
        result = True

    # Check result
    assert result is valid

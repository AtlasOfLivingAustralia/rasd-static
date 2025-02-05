"""RASD FastAPI ISO8601 Date Custom Data Type."""


# Standard
import datetime

# Typing
from typing import Any, Callable, Iterator


class ISO8601Date(datetime.date):
    """ISO8601 Date."""

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], "ISO8601Date"]]:
        """Yields the validators for the ISO8601Date.

        Yields:
            Callable[[Any], "ISO8601Date"]: Validator functions for an
                ISO8601Date.
        """
        # Yield the ISO8601 Format Validator
        yield cls.validate_format

    @classmethod
    def validate_format(cls, v: Any) -> "ISO8601Date":
        """Validates an ISO8601 Date.

        Args:
            v (Any): Value to be validated

        Raises:
            TypeError: Raised if the supplied value is the wrong type.
            ValueError: Raised if the supplied value is invalid.

        Returns:
            ISO8601Date: Validated date if applicable.
        """
        # Check if value is already an `ISO8601Date`
        if isinstance(v, cls):
            return v

        # Check that the supplied value is a string
        if not isinstance(v, str):
            raise TypeError("ISO8601Date must be parsed from string")

        # Parse and return ISO8601 date
        return cls.fromisoformat(v)

    def __repr__(self) -> str:
        """Provides a representation of the validated ISO8601Date.

        Returns:
            str: String representation of the validated ISO8601Date.
        """
        return f"ISO8601Date({super().__repr__()})"

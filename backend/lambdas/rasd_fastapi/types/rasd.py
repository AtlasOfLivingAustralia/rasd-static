"""RASD FastAPI RASD ID Custom Data Type."""


# Standard
import datetime
import re
import uuid

# Typing
from typing import Any, Callable, Iterator


class RASDIdentifier(str):
    """RASD Identifier."""

    # RASD Identifier Regex
    RASD_IDENTIFIER_PATTERN = r"^RASD-\d{8}-[0-9a-f]{6}(?:-\d{2})?$"
    RASD_IDENTIFIER_REGEX = re.compile(RASD_IDENTIFIER_PATTERN)

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], "RASDIdentifier"]]:
        """Yields the validators for the RASD Identifier.

        Yields:
            Callable[[Any], "RASDIdentifier"]: Validator functions for a RASD
                Identifier.
        """
        # Yield the RASD Identifier Local Validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        """Modifies the field schema for a RASD Identifier string.

        Args:
            field_schema (dict[str, Any]): Field schema to modify in place.
        """
        # Mutate the Field Schema Dictionary in Place
        field_schema.update(
            pattern=cls.RASD_IDENTIFIER_PATTERN,
            examples=["RASD-20230122-8d18cc", "RASD-20230204-73df14", "RASD-20230204-73df14-03"],
        )

    @classmethod
    def validate(cls, v: Any) -> "RASDIdentifier":
        """Validates a RASD Identifier locally.

        Args:
            v (Any): Value to be validated

        Raises:
            TypeError: Raised if the supplied value is the wrong type.
            ValueError: Raised if the supplied value is invalid.

        Returns:
            RASDIdentifier: Locally validated RASD Identifier if applicable.
        """
        # Check that the supplied value is a string
        if not isinstance(v, str):
            raise TypeError("RASD Identifier must be a string")

        # Match RASD Identifier format using Regex
        if not cls.RASD_IDENTIFIER_REGEX.fullmatch(v):
            raise ValueError("RASD Identifier is not in a valid format")

        # Return the RASD Identifier
        return cls(v)

    @classmethod
    def generate(cls) -> "RASDIdentifier":
        """Generates a new unique RASD Identifier.

        RASD Identifiers are generated in the following form:
            `RASD-{YYYYmmdd}-{First 6 characters of a UUID}`

        For example:
            * RASD-20230122-8d18cc
            * RASD-20230128-d5481d
            * RASD-20230204-734538
            * RASD-20230315-7fc9dd
            * RASD-20230327-68aa42

        Returns:
            RASDIdentifier: New RASD Identifier.
        """
        # Generate and Return RASD Identifier
        return cls.validate(
            f"RASD-{datetime.date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
        )

    def generate_sub(self, number: int) -> "RASDIdentifier":
        """Generates a new RASD Identifier with the supplied numeric suffix.

        Args:
            number (int): Numeric suffix for the new RASD Identifier.

        Returns:
            RASDIdentifier: Generated RASD Identifier with numeric suffix.
        """
        # Generate and Validate
        return self.validate(f"{self}-{number:02}")

    def __repr__(self) -> str:
        """Provides a representation of the validated RASD Identifier.

        Returns:
            str: String representation of the validated RASD Identifier.
        """
        return f"RASDIdentifier({super().__repr__()})"

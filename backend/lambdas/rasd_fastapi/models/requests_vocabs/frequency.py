"""RASD FastAPI Frequency Restricted Vocabulary."""


# Standard
import enum


class Frequency(str, enum.Enum):
    """Frequency Restricted Vocabulary Enumeration."""
    SINGLE_ONCE_OFF = "Single once off"
    DEFINED_PERIOD = "Defined period"
    ONGOING = "Ongoing"

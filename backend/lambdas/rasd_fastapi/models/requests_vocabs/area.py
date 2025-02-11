"""RASD FastAPI Area Restricted Vocabulary."""


# Standard
import enum


class Area(str, enum.Enum):
    """Area Restricted Vocabulary Enumeration."""
    WHOLE_DATASET = "Whole Dataset"
    SPECIFIC_AREA = "Specific Area"

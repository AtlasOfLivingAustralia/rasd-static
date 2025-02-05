"""RASD FastAPI Collection Method Restricted Vocabulary."""


# Standard
import enum


class CollectionMethod(str, enum.Enum):
    """Collection Method Restricted Vocabulary Enumeration."""
    INCIDENTAL_OBSERVATION = "Incidental Observation"
    SPECIMEN_COLLECTION = "Specimen Collection"
    SYSTEMATIC_SURVEY = "Systematic Survey"
    UNKNOWN = "Unknown"
    MIXED = "Mixed"
    OTHER_MEDIA = "Other Media (e.g. sound / images)"

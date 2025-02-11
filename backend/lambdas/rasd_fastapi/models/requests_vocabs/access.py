"""RASD FastAPI Access Restricted Vocabulary."""


# Standard
import enum


class Access(str, enum.Enum):
    """Access Restricted Vocabulary Enumeration."""
    JUST_ME = "Just me"
    SELECT_GROUP = "A select group within my organisation / institution"
    ENTIRE_ORGANISATION = "My entire organisation / institution"
    OTHER = "Other"

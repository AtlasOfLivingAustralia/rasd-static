"""RASD FastAPI Security Classification Restricted Vocabulary."""


# Standard
import enum


class SecurityClassification(str, enum.Enum):
    """Security Classification Restricted Vocabulary Enumeration."""
    UNCLASSIFIED = "Unclassified"
    RESTRICTED = "Restricted"
    CONFIDENTIAL = "Confidential"
    SENSITIVE_BUT_UNCLASSIFIED = "Sensitive But Unclassified"
    FOR_OFFICIAL_USE_ONLY = "For Official Use Only"
    LIMITED_DISTRIBUTION = "Limited Distribution"

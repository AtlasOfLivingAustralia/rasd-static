"""RASD FastAPI Security Classification Restricted Vocabulary."""


# Standard
import enum


class SecurityClassification(str, enum.Enum):
    """Security Classification Restricted Vocabulary Enumeration."""
    UNOFFICIAL = "Unofficial"
    OFFICIAL = "Official"
    OFFICIAL_SENSITIVE = "Official: sensitive"
    OFFICIAL_SENSITIVE_PERSONAL_PRIVACY = "Official: Sensitive: Personal - Privacy"
    OFFICIAL_SENSITIVE_LEGAL_PRIVILEGE = "Official: Sensitive: Legal - Privilege"
    OFFICIAL_SENSITIVE_LEGISLATIVE_SECRECY = "Official: Sensitive: Legislative - Secrecy"

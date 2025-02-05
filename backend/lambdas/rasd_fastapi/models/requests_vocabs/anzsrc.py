"""RASD FastAPI ANZSRC Restricted Vocabulary."""


# Standard
import enum


class ResearchClassification(str, enum.Enum):
    """ANZSRC Restricted Vocabulary Enumeration."""
    EDUCATION = "Education"
    ENGINEERING = "Engineering"
    ENVIRONMENTAL_SCIENCES = "Environmental Sciences"
    HEALTH_SCIENCES = "Health Sciences"
    HISTORY_HERITAGE_AND_ARCHAEOLOGY = "History, Heritage and Archaeology"
    HUMAN_SOCIETY = "Human Society"
    INDIGENOUS_STUDIES = "Indigenous Studies"
    INFORMATION_AND_COMPUTING_SCIENCES = "Information and Computing Sciences"
    LANGUAGE_COMMUNICATIONS_AND_CULTURE = "Language, Communications and Culture"
    LAW_AND_LEGAL_STUDIES = "Law and Legal Studies"
    MATHEMATICAL_SCIENCES = "Mathematical Sciences"
    PHILOSOPHY_AND_RELIGIOUS_STUDIES = "Philosophy and Religious Studies"
    PHYSICAL_SCIENCES = "Physical Sciences"
    PSYCHOLOGY = "Psychology"

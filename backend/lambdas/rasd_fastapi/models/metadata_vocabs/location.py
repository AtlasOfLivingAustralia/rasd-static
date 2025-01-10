"""RASD FastAPI Location Restricted Vocabulary."""


# Standard
import enum


class Location(str, enum.Enum):
    """Location Restricted Vocabulary Enumeration."""
    AUSTRALIA = "Australia"
    NEW_SOUTH_WALES = "New South Wales"
    AUSTRALIAN_CAPITAL_TERRITORY = "Australian Capital Territory"
    SOUTH_AUSTRALIA = "South Australia"
    WESTERN_AUSTRALIA = "Western Australia"
    VICTORIA = "Victoria"
    QUEENSLAND = "Queensland"
    TASMANIA = "Tasmania"
    NORTHERN_TERRITORY = "Northern Territory"
    AUSTRALIAN_OTHER_TERRITORIES = "Australian Other Territories"

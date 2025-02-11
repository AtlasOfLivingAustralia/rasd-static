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
    ASHMORE_AND_CARTIER_ISLANDS = "Ashmore and Cartier Islands"
    AUSTRALIAN_ANTARCTIC_TERRITORY = "Australian Antarctic Territory"
    CHRISTMAS_ISLAND = "Christmas Island"
    COCOS_KEELING_ISLAND = "Cocos (Keeling) Island"
    CORAL_SEA_ISLANDS = "Coral Sea Islands"
    HEARD_AND_MCDONALD_ISLANDS = "Heard and McDonald Islands"
    NORFOLK_ISLAND = "Norfolk Island"
    LORD_HOWE_ISLAND = "Lord Howe Island"
    MACQUARIE_ISLAND = "Macquarie Island"
    OUTSIDE_AUSTRALIA_GLOBAL = "Outside Australia (Global)"
    COMMONWEALTH_WATERS = "Commonwealth Waters"

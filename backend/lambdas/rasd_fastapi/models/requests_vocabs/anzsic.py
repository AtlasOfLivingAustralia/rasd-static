"""RASD FastAPI ANZSIC Restricted Vocabulary."""


# Standard
import enum


class IndustryClassification(str, enum.Enum):
    """ANZSIC Restricted Vocabulary Enumeration."""
    AGRICULTURE_FORESTRY_AND_FISHING = "Agriculture, Forestry and Fishing"
    MINING = "Mining"
    MANUFACTURING = "Manufacturing"
    ELECTRICITY_GAS_WATER_AND_WASTE_SERVICES = "Electricity, Gas, Water and Waste Services"
    CONSTRUCTION = "Construction"
    WHOLESALE_TRADE = "Wholesale Trade"
    RETAIL_TRADE = "Retail Trade"
    ACCOMMODATION_AND_FOOD_SERVICES = "Accommodation and Food Services"
    TRANSPORT_POSTAL_AND_WAREHOUSING = "Transport, Postal and Warehousing"
    INFORMATION_MEDIA_AND_TELECOMMUNICATIONS = "Information, Media and Telecommunications"
    FINANCIAL_AND_INSURANCE_SERVICES = "Financial and Insurance Services"
    RENTAL_HIRING_AND_REAL_ESTATE_SERVICES = "Rental, Hiring and Real Estate Services"
    PROFESSIONAL_SCIENTIFIC_AND_TECHNICAL_SERVICES = "Professional, Scientific and Technical Services"
    ADMINISTRATIVE_AND_SUPPORT_SERVICES = "Administrative and Support Services"
    PUBLIC_ADMINISTRATION_AND_SAFETY = "Public Administration and Safety"
    EDUCATION_AND_TRAINING = "Education and Training"
    HEALTH_CARE_AND_SOCIAL_ASSISTANCE = "Health Care and Social Assistance"
    ARTS_AND_RECREATIONAL_SERVICES = "Arts and Recreational Services"
    OTHER_SERVICES = "Other Services"

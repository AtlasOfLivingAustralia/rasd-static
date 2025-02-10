"""RASD FastAPI Format Restricted Vocabulary."""


# Standard
import enum


class Format(str, enum.Enum):
    """Format Restricted Vocabulary Enumeration."""
    XML = "Xml"
    CSV = "Csv"
    JSON = "Json"
    WMS = "Wms"
    WFS = "Wfs"
    SHP = "Shp"
    SDE = "Sde"
    REST_MAPSERVER = "REST MapServer"
    ALL_MAJOR_FORMATS = "All Major Formats"
    OTHER = "Other"

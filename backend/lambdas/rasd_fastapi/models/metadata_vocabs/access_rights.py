"""RASD FastAPI Access Rights Restricted Vocabulary."""


# Standard
import enum


class AccessRights(str, enum.Enum):
    """Access Rights Restricted Vocabulary Enumeration."""
    COPYRIGHT = "Copyright"
    LICENCE = "Licence"
    INTELLECTUAL_PROPERTY_RIGHTS = "Intellectual Property Rights"
    RESTRICTED = "Restricted"
    OTHER_RESTRICTIONS = "Other Restrictions"
    UNRESTRICTED = "Unrestricted"
    LICENCE_UNRESTRICTED = "Licence Unrestricted"
    LICENCE_END_USER = "Licence End User"
    LICENCE_DISTRIBUTOR = "Licence Distributor"
    PRIVATE = "Private"
    STATUTORY = "Statutory"
    SENSITIVE_BUT_UNCLASSIFIED = "Sensitive But Unclassified"

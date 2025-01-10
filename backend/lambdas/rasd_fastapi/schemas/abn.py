"""RASD FastAPI ABN REST API Schemas."""


# Third-Party
import pydantic

# Typing
from typing import Optional


class AbnLookup(pydantic.BaseModel):
    """ABN Lookup Schema.

    This schema is copied directly from the ABN Lookup API, and as such
    contains some "un-pythonic" properties such as *PascalCase* fields.

    This schema deliberately inherits from `pydantic.BaseModel` rather than
    `schemas.base.BaseSchema` because we can't control any aspect of its
    behaviour (i.e., field types, field validation, etc.).
    """
    Abn: str
    AbnStatus: str
    AbnStatusEffectiveFrom: str
    Acn: str
    AddressDate: Optional[str]
    AddressPostcode: str
    AddressState: str
    BusinessName: list[str]
    EntityName: str
    EntityTypeCode: str
    EntityTypeName: str
    Gst: Optional[str]
    Message: str
    Email: pydantic.EmailStr

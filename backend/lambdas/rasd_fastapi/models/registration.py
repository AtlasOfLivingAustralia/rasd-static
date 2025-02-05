"""RASD FastAPI Registration Models."""


# Standard
import datetime
import enum
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi import utils
from rasd_fastapi.models import base
from rasd_fastapi.schemas import auth as auth_schemas
from rasd_fastapi.schemas import organisations as org_schemas

# Typing
from typing import Optional, Union


# Shortcuts
ExistingOrNewOrganisation = Union[uuid.UUID, org_schemas.OrganisationCreate]


class Status(str, enum.Enum):
    """Status Enumeration."""
    NEW = "New"
    APPROVED = "Approved"
    DECLINED = "Declined"


class Registration(base.BaseModel):
    """Registration Model."""
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    username: pydantic.EmailStr
    given_name: str
    family_name: str
    group: auth_schemas.Group
    organisation: ExistingOrNewOrganisation
    agreements: list[str]

    # The attributes below are not provided by the user
    # These are used to keep track of the submission and its status
    status: Status = Status.NEW
    reason: Optional[str] = None
    organisation_override: Optional[uuid.UUID]
    actioned_by: Optional[pydantic.EmailStr]
    created_at: datetime.datetime = pydantic.Field(default_factory=utils.utcnow)

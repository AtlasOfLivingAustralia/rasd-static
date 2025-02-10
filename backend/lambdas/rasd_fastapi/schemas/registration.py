"""RASD FastAPI Registration Schemas."""


# Standard
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi.schemas import base
from rasd_fastapi.schemas import auth as auth_schemas
from rasd_fastapi.schemas import organisations as org_schemas

# Typing
from typing import Union


# Shortcuts
ExistingOrNewOrganisation = Union[uuid.UUID, org_schemas.OrganisationCreate]


class RegistrationCreate(base.BaseSchema):
    """Registration Create Schema."""
    username: pydantic.EmailStr
    given_name: str
    family_name: str
    group: auth_schemas.Group
    organisation: ExistingOrNewOrganisation
    agreements: list[str]


class RegistrationUpdate(base.BaseSchema):
    """Registration Update Schema."""
    # This has intentionally been left blank.
    # A Registration currently cannot be updated once submitted.

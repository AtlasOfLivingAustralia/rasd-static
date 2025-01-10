"""RASD FastAPI Organisations REST API Schemas."""


# Third-Party
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi.schemas import base

# Typing
from typing import Optional


class OrganisationCreate(base.BaseSchema):
    """Organisation Create Schema."""
    name: str = pydantic.Field(max_length=200)
    abn: types.abn.Abn
    email: pydantic.EmailStr


class OrganisationUpdate(base.BaseSchema):
    """Organisation Update Schema."""
    email: Optional[pydantic.EmailStr]

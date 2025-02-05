"""RASD FastAPI Organisations Data Model."""


# Standard
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi.models import base


class Organisation(base.BaseModel):
    """Organisation Data Model."""
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    name: str = pydantic.Field(max_length=200)
    abn: types.abn.Abn
    email: pydantic.EmailStr

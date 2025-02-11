"""RASD FastAPI Pagination Schemas."""


# Third-Party
import pydantic.generics

# Local
from rasd_fastapi.models import base as base_models
from rasd_fastapi.schemas import base as base_schemas

# Typing
from typing import Generic, Optional, TypeVar, Union


# Constants
ModelT = TypeVar("ModelT", bound=Union[base_models.BaseModel, base_schemas.BaseSchema])


class PaginatedResult(pydantic.generics.GenericModel, Generic[ModelT]):
    """Generic Paginated Result Schema."""
    count: int
    cursor: Optional[str]
    results: list[ModelT]

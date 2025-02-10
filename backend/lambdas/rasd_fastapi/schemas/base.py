"""RASD FastAPI Base REST API Schemas."""


# Third-Party
import pydantic


class BaseSchema(pydantic.BaseModel):
    """Base Schema."""
    # Functionality that is common to all schemas should be implemented here

    class Config:
        """Base Schema Configuration."""
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 500

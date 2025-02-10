"""RASD FastAPI Base Data Model."""


# Third-Party
import pydantic


class BaseModel(pydantic.BaseModel):
    """Base Data Model."""
    # Functionality that is common to all models should be implemented here
    active: bool = True

    class Config:
        """Base Model Configuration."""
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 500

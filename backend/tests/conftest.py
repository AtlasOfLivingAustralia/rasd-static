"""RASD Unit Tests Configuration and Utilities."""


# Standard
import json
import pathlib

# Third-Party
import fastapi.encoders
import pydantic

# Typing
from typing import Dict, Any, Union


# Shortcuts
DictOrModel = Union[dict[str, Any], pydantic.BaseModel]

# Constants
TEST_DATA_DIRECTORY = pathlib.Path(__file__).parent / "data"


def load_data_json(name: str) -> Dict[str, Any]:
    """Loads unit test data as a `.json`.

    Args:
        name (str): Name of the unit test data to load.

    Returns:
        Dict[str, Any]: `.json` dictionary of the loaded data.
    """
    # Load, Parse and Return
    return json.loads((TEST_DATA_DIRECTORY / name).read_bytes())  # type: ignore[no-any-return]


def matches(a: DictOrModel, b: DictOrModel) -> bool:
    """Checks whether one dict or model is a subset of another dict or model.

    This utility function allows for easier assertions in unit tests.

    Args:
        a (DictOrModel): Child to be checked.
        b (DictOrModel): Parent to be checked.

    Returns:
        bool: Whether dict/model `a` is a subset of dict/model `b`.
    """
    # Encode to Dictionaries and Retrieve Items
    a_items = a.items() if isinstance(a, dict) else fastapi.encoders.jsonable_encoder(a).items()
    b_items = b.items() if isinstance(b, dict) else fastapi.encoders.jsonable_encoder(b).items()

    # Check and Return
    return all(x in b_items for x in a_items)

"""RASD FastAPI ABN Lookup Service."""


# Standard
import functools
import re

# Third-Party
import httpx

# Local
from rasd_fastapi.core import settings
from rasd_fastapi.schemas import abn as abn_schemas


# Constants
CALLBACK_REGEX = re.compile(r"^rasd\((.*)\)$")


@functools.lru_cache()
def lookup_abn(abn: str) -> abn_schemas.AbnLookup:
    """Validates an ABN with an external service.

    The lookup results are cached, so sequential calls should not be expensive.

    Args:
        abn (str): ABN string to validate.

    Returns:
        abn_schemas.AbnLookup: ABN lookup response if applicable.
    """
    # Handle API and Network Errors
    try:
        # Perform API Call
        response = httpx.get(
            url=settings.SETTINGS.ABN_LOOKUP_URL,
            params={
                "guid": settings.SETTINGS.ABN_LOOKUP_GUID,
                "abn": abn,
                "callback": "rasd",  # We use Regex to remove this callback later
            }
        )

        # Raise for Status Error
        response.raise_for_status()

    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        # Re-raise as ValueError
        raise ValueError(exc) from exc

    # Strip the response
    # The response is an old-style callback response. We have to strip the
    # `rasd(...)` callback string wrapping the response JSON using Regex. This
    # allows us to decode it as a `json` and parse it using `pydantic` after.
    stripped_text = CALLBACK_REGEX.sub(r"\1", response.text)

    # Parse and Return
    return abn_schemas.AbnLookup.parse_raw(stripped_text)


def verify_registered(abn: str) -> bool:
    """Verifies an ABN is registered using the ABN lookup service.

    Args:
        abn (str): ABN to verify.

    Returns:
        bool: Whether the ABN is registered.
    """
    # Lookup ABN
    results = lookup_abn(abn)

    # Parse Results for Validity
    # To be registered, the "Message" field must be empty
    return not results.Message


def verify_active(abn: str) -> bool:
    """Verifies an ABN is active using the ABN lookup service.

    Args:
        abn (str): ABN to verify.

    Returns:
        bool: Whether the ABN is active.
    """
    # Lookup ABN
    results = lookup_abn(abn)

    # Parse Results for Validity
    # To be active, the "AbnStatus" field must be "Active"
    return results.AbnStatus == "Active"


def verify_name(abn: str, name: str) -> bool:
    """Verifies an ABN's entity name using the ABN lookup service.

    Args:
        abn (str): ABN to verify.
        name (str): Entity name to match against.

    Returns:
        bool: Whether the ABN is registered.
    """
    # Lookup ABN
    results = lookup_abn(abn)

    # Parse Results for Validity
    # To be valid, the "EntityName" field must match the provided `name`
    return results.EntityName == name

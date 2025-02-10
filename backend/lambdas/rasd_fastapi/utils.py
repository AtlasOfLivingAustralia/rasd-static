"""RASD FastAPI Utilities."""


# Standard
import datetime

# Third-Party
import fastapi

# Typing
from typing import Optional, TypeVar, Union


# Constants
T = TypeVar("T")
ApiOrRouter = Union[fastapi.FastAPI, fastapi.APIRouter]


def add_redirect(app: ApiOrRouter, path: str, url: Optional[str]) -> None:
    """Adds a redirect for a given path to a given URL.

    Args:
        app (ApiOrRouter): API or router to add the redirect to.
        path (str): API path for the redirect.
        url (Optional[str]): URL to redirect to
    """
    # Construct Redirect Function
    def redirect(request: fastapi.Request) -> fastapi.Response:
        # Retrieve the `root_path` from the request scope
        # This is required in case we are behind a proxy (e.g., API Gateway)
        root_path = request.scope.get("root_path", "")

        # Perform Redirect
        return fastapi.responses.RedirectResponse(url=f"{root_path}{url}")

    # Add Redirect to App
    app.get(path, include_in_schema=False)(redirect)


def unwrap_or_404(value: Optional[T]) -> T:
    """Unwraps the supplied optional value, raising a 404 error if applicable.

    Args:
        value (Optional[T]): The optional value to unwrap.

    Raises:
        fastapi.HTTPException: Raised if the value is `None`.

    Returns:
        T: The unwrapped value if applicable.
    """
    # Check Value
    if not value:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Return
    return value


def utcnow() -> datetime.datetime:
    """Generates timezone aware current datetime in UTC.

    Returns:
        datetime.datetime: Current timestamp in UTC.
    """
    # Generate and Return
    return datetime.datetime.now(tz=datetime.timezone.utc)

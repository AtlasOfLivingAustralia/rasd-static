"""RASD FastAPI Security Functionality."""


# Standard
import contextlib

# Third-Party
import fastapi
import fastapi.security
import fastapi_cloudauth

# Local
from rasd_fastapi.core import settings
from rasd_fastapi.schemas import auth as auth_schemas

# Typing
from typing import Awaitable, Callable, Optional, TypeVar


# Constants
T = TypeVar("T")
AsyncAuthDependency = Callable[[fastapi.security.HTTPAuthorizationCredentials], Awaitable[T]]


# Authentication
auth = fastapi_cloudauth.CognitoCurrentUser(
    region=settings.SETTINGS.AWS_DEFAULT_REGION,
    userPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
    client_id=settings.SETTINGS.AWS_COGNITO_CLIENT_ID,
    auto_error=True,
)


def require(*groups: auth_schemas.Group) -> AsyncAuthDependency[auth_schemas.User]:
    """Constructs a `fastapi` dependency that requires user groups for access.

    This dependency raises an exception if the caller is not authenticated,
    meaning it "requires" the caller to be logged in.

    Args:
        *groups (auth_schemas.Group): Groups that the user must belong to.

    Raises:
        fastapi.HTTPException: Raised if permission is not allowed.

    Returns:
        AsyncAuthDependency[auth_schemas.User]: Constructed `fastapi` auth
            dependency that requires a user to be logged in as one of the
            supplied groups.
    """
    # Construct bearer dependency
    # Here we set `auto_error=True` so that unauthenticated requests are
    # automatically handled and raise a `401` HTTP error.
    bearer = fastapi.Depends(fastapi.security.HTTPBearer(auto_error=True))

    # Construct the inner dependency function
    async def inner(
        http_auth: fastapi.security.HTTPAuthorizationCredentials = bearer,
    ) -> auth_schemas.User:
        # Decode JWT to User Schema
        user: auth_schemas.User = await auth.claim(auth_schemas.User)(http_auth)

        # Check Groups
        # 1. If no groups are supplied then any user is allowed
        # 2. Otherwise, at least 1 group supplied must match
        if not groups or any(g in user.groups for g in groups):
            # Return
            return user

        # Raise a `403` error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail=f"User must be logged in as one of {[g.value for g in groups]}",
        )


    # Return inner dependency function
    return inner


def maybe(*groups: auth_schemas.Group) -> AsyncAuthDependency[Optional[auth_schemas.User]]:
    """Constructs a `fastapi` dependency that allows user groups access.

    This dependency returns `None` if the caller is not authenticated, meaning
    the caller is "maybe" authenticated. This dependency allows for more
    complex authentication flows for endpoints such as extra or alternative
    behaviour for authenticated/unauthenticated users.

    Args:
        *groups (auth_schemas.Group): Groups that the user may belong to.

    Returns:
        AsyncAuthDependency[Optional[auth_schemas.User]]: Constructed `fastapi`
            auth dependency that allows a user to be logged in as one of the
            supplied groups, or alternatively returns `None`.
    """
    # Construct bearer dependency
    # Here we set `auto_error=False` so that unauthenticated requests can be
    # handled manually and we can return a `None` value.
    bearer = fastapi.Depends(fastapi.security.HTTPBearer(auto_error=False))

    # Construct the inner dependency function
    async def inner(
        http_auth: fastapi.security.HTTPAuthorizationCredentials = bearer,
    ) -> Optional[auth_schemas.User]:
        # Suppress any authentication exceptions
        with contextlib.suppress(fastapi.HTTPException):
            # Perform and return required authentication process
            return await require(*groups)(http_auth)

        # Return None if not authenticated
        return None

    # Return inner dependency function
    return inner


# Shortcuts
require_user = require()
require_requestor = require(auth_schemas.Group.DATA_REQUESTORS)
require_custodian = require(auth_schemas.Group.DATA_CUSTODIANS)
require_admin = require(auth_schemas.Group.ADMINISTRATORS)
require_admin_or_custodian = require(auth_schemas.Group.ADMINISTRATORS, auth_schemas.Group.DATA_CUSTODIANS)
maybe_user = maybe()

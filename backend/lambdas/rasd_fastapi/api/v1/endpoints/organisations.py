"""RASD FastAPI Organisations REST API Endpoints."""


# Standard
import uuid

# Third-Party
import boto3
import fastapi

# Local
from rasd_fastapi import utils
from rasd_fastapi.db import session
from rasd_fastapi.core import security
from rasd_fastapi.crud import organisations as org_crud
from rasd_fastapi.models import organisations as org_models
from rasd_fastapi.schemas import auth
from rasd_fastapi.schemas import organisations as org_schemas
from rasd_fastapi.schemas import pagination

# Typing
from typing import Optional


# Router
router = fastapi.APIRouter()


@router.get(r"", response_model=pagination.PaginatedResult[org_models.Organisation])
async def list_organisations(
    *,
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    active_only: bool = True,
    limit: Optional[int] = None,
    cursor: Optional[uuid.UUID] = None,
) -> pagination.PaginatedResult[org_models.Organisation]:
    """List Organisations endpoint for REST API.

    Args:
        db_session (boto3.Session): Dependency injection database session.
        active_only (bool): Show only active organisations.
        limit (Optional[int]): Optional pagination limit.
        cursor (Optional[uuid.UUID]): Optional pagination cursor.

    Returns:
        pagination.PaginatedResult[org_models.Organisation]: Retrieved page of
            Organisations.
    """
    # Scan Organisations and Return
    return org_crud.organisation.scan(
        db_session,
        filter=org_crud.organisation.ActiveOnly if active_only else None,
        limit=limit,
        cursor=cursor,
    )


@router.get(r"/{pk}", response_model=org_models.Organisation)
async def read_organisation(
    *,
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
) -> org_models.Organisation:
    """Read Organisation endpoint for REST API.

    Args:
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Organisation to read.

    Returns:
        org_models.Organisation: Retrieved Organisation.
    """
    # Retrieve and Return Organisation
    return utils.unwrap_or_404(
        value=org_crud.organisation.get(db_session, pk=pk),
    )


@router.post(r"", response_model=org_models.Organisation)
async def create_organisation(
    *,
    user: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    org_in: org_schemas.OrganisationCreate,
) -> org_models.Organisation:
    """Create Organisation endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        org_in (org_schemas.OrganisationUpdate): Create data.

    Returns:
        org_models.Organisation: Created Organisation.
    """
    # Handle Creation Errors
    # The uniqueness of the Organisation is checked, and the ABN is validated
    # by an external service upon creation, so we need to handle and wrap any
    # errors that occur.
    try:
        # Create Organisation
        obj = org_crud.organisation.create_unique(db_session, obj_in=org_in)

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    # Return
    return obj


@router.patch(r"/{pk}", response_model=org_models.Organisation)
async def update_organisation(
    *,
    user: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
    org_in: org_schemas.OrganisationUpdate,
) -> org_models.Organisation:
    """Update Organisation endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Organisation to read.
        org_in (org_schemas.OrganisationUpdate): Update data.

    Returns:
        org_models.Organisation: Updated Organisation.
    """
    # Retrieve Organisation
    org = utils.unwrap_or_404(
        value=org_crud.organisation.get(db_session, pk=pk),
    )

    # Update and Return Organisation
    return org_crud.organisation.update(db_session, db_obj=org, obj_in=org_in)

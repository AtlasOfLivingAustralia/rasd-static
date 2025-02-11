"""RASD FastAPI CRUD for Metadata."""


# Standard
import functools
import operator
import uuid

# Third-Party
import boto3
import boto3.dynamodb.conditions as con

# Local
from rasd_fastapi.core import settings
from rasd_fastapi.crud import base
from rasd_fastapi.models import organisations as org_models
from rasd_fastapi.models import metadata as metadata_models
from rasd_fastapi.models.metadata_vocabs import keywords
from rasd_fastapi.models.metadata_vocabs import locations
from rasd_fastapi.schemas import metadata as metadata_schemas

# Typing
from typing import Optional


class RASDMetadataCRUD(
    base.CRUDBase[
        metadata_models.RASDMetadata,
        metadata_schemas.RASDMetadataCreate,
        metadata_schemas.RASDMetadataUpdate,
        uuid.UUID,
    ],
):
    """Metadata CRUD Abstraction."""

    def create_with_org(
        self,
        db_session: boto3.Session,
        *,
        obj_in: metadata_schemas.RASDMetadataCreate,
        org: org_models.Organisation,
    ) -> metadata_models.RASDMetadata:
        """Creates a Metadata with an Organisation in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            obj_in (metadata_schemas.RASDMetadataCreate): Data to create item with.
            org (org_models.Organisation): Organisation to create Metadata for.

        Returns:
            metadata_models.RASDMetadata: Created Metadata in the database.
        """
        # Allow super class to handle the Creation
        return super().create(
            db_session,
            obj_in=obj_in,
            organisation_id=org.id,  # Extract Organisation ID
            custodian=org.name,      # Extract Organisation Name
        )

    def build_filter(
        self,
        active_only: bool = True,
        title: Optional[str] = None,
        abstract: Optional[str] = None,
        keywords: Optional[set[keywords.Keyword]] = None,
        locations: Optional[set[locations.Location]] = None,
        organisation_id: Optional[uuid.UUID] = None,
    ) -> Optional[con.ConditionBase]:
        """Builds the search filter for the Metadata table.

        Each of the provided values is combined into a single filter using a
        logical AND. That is, all of the supplied filter values must match in
        an underlying Metadata instance for the filter to return them.

        The interface that `boto3` provides for constructing DynamoDB filters
        does not cater very well for dynamic filter generation. As such, the
        syntax used to generate the filter below is slightly obscure. In order
        to be terse we utilise functional concepts like the `reduce` method to
        combine individual filters.

        Args:
            active_only (bool): Filter for `active` only metadata.
            title (Optional[str]): Filter results based on `title`.
            abstract (Optional[str]): Filter results based on.
            keywords (Optional[set[keywords.Keyword]]): Filter results based on `keywords`.
            locations (Optional[set[locations.Location]]): Filter results based on `locations`.
            organisation_id (Optional[uuid.UUID]): Filter results based on `organisation_id`.

        Returns:
            Optional[con.ConditionBase]: Possible built filter.
        """
        # Generate Filters
        # Here we construct all of the required filters in a list.
        # Based on the input data, the items in this list will either be an
        # individually constructed filter (if a value is supplied) or `None`.
        filters = [
            # `active` filter - `active` must equal `True`
            con.Attr("active").eq(True) if active_only else None,
            # `title` filter - `title_lower` must equal the provided string (case insensitive)
            con.Attr("title_lower").contains(title.lower()) if title else None,
            # `abstract` filter - `abstract_lower` must equal the provided string (case insensitive)
            con.Attr("abstract_lower").contains(abstract.lower()) if abstract else None,
            # `keywords` filter - `keywords` list must *contain* at least 1 of the provided keywords (i.e., logical OR)
            functools.reduce(operator.or_, [con.Attr("keywords").contains(k) for k in keywords]) if keywords else None,
            # `locations` filter - `locations` list must *contain* at least 1 of the provided locations (i.e., logical OR)  # noqa: E501
            functools.reduce(operator.or_, [con.Attr("locations").contains(loc) for loc in locations]) if locations else None,  # noqa: E501
            # `organisation_id` filter - `organisation_id` must equal the provided UUID
            con.Attr("organisation_id").eq(str(organisation_id)) if organisation_id else None
        ]

        # Next, we remove all of the `None`s from the filters list
        # This removes any of the filters that a value was not supplied for
        filters = [f for f in filters if f]

        # Finally, we reduce the list of filters to a single filter where all
        # of the individual filters must be true (i.e., logical AND).
        combined_filter = functools.reduce(operator.and_, filters) if filters else None

        # Return
        return combined_filter


# Instantiate Metadata CRUD Singleton
metadata = RASDMetadataCRUD(
    model=metadata_models.RASDMetadata,
    table=settings.SETTINGS.AWS_DYNAMODB_TABLE_METADATA,
    pk="id",
)

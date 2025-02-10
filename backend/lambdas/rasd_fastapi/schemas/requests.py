"""RASD FastAPI Data Access Request Schemas."""


# Standard
import datetime
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi.schemas import base
from rasd_fastapi.models.requests_vocabs import access
from rasd_fastapi.models.requests_vocabs import anzsic
from rasd_fastapi.models.requests_vocabs import anzsrc
from rasd_fastapi.models.requests_vocabs import area
from rasd_fastapi.models.requests_vocabs import frequency
from rasd_fastapi.models.requests_vocabs import purposes

# Typing
from typing import Optional


class DataAccessRequestCreate(base.BaseSchema):
    """DataAccessRequest Create Schema."""
    # Datasets (Selected by User)
    metadata_ids: list[uuid.UUID] = pydantic.Field(min_items=1, max_items=10)
    # Requestor Information (Provided by User)
    requestor_organisation_address: str
    requestor_organisation_indigenous_body: bool
    requestor_orcid: Optional[types.orcid.Orcid]
    # Request Information (Provided by User)
    project_title: str
    project_purpose: purposes.Purpose
    project_research: Optional[anzsrc.ResearchClassification]
    project_industry: Optional[anzsic.IndustryClassification]
    project_commercial: bool
    project_public_benefit_explanation: str
    data_requested: str
    data_relevance_explanation: str
    data_frequency: frequency.Frequency
    data_required_from: Optional[types.date.ISO8601Date]
    data_required_to: Optional[types.date.ISO8601Date]
    data_frequency_explanation: Optional[str]
    data_area: area.Area
    data_area_explanation: Optional[str]
    data_security_explanation: str
    data_access: access.Access
    data_access_explanation: str
    data_distribution_explanation: str
    data_accept_transformed: bool


class DataAccessRequestUpdate(base.BaseSchema):
    """Data Access Request Update Schema."""
    # DOI
    # This can only be updated by an Administrator
    doi: Optional[types.doi.DOI]


class DatasetRequestUpdate(base.BaseSchema):
    """Dataset Request Update Schema."""
    # Notes
    # This can only be updated by the Custodian
    notes: Optional[str]


class DatasetRequestSummary(base.BaseSchema):
    """Dataset Request Summary Schema."""
    # Unique Identifier
    id: types.rasd.RASDIdentifier # noqa: A003
    # Dataset Metadata Information
    metadata_title: str
    metadata_data_source_doi: Optional[types.doi.DOI]
    metadata_data_source_url: Optional[pydantic.HttpUrl]
    # Custodian Information
    custodian_name: str


class DataAccessRequestSummary(base.BaseSchema):
    """Data Access Request Summary Schema."""
    # Unique Identifier
    id: types.rasd.RASDIdentifier  # noqa: A003
    # Tracking Information
    doi: Optional[types.doi.DOI]
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime]
    # Dataset Requests Information
    dataset_requests: list[DatasetRequestSummary]
    # Data Access Request Information (Form)
    data_requested: str
    data_frequency: frequency.Frequency
    data_required_from: Optional[types.date.ISO8601Date]
    data_required_to: Optional[types.date.ISO8601Date]
    data_frequency_explanation: Optional[str]
    data_area: area.Area
    data_area_explanation: Optional[str]

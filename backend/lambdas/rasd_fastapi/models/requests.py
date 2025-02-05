"""RASD FastAPI Data Access Request Models."""


# Standard
import datetime
import enum
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi import utils
from rasd_fastapi.models import base
from rasd_fastapi.models.requests_vocabs import access
from rasd_fastapi.models.requests_vocabs import anzsic
from rasd_fastapi.models.requests_vocabs import anzsrc
from rasd_fastapi.models.requests_vocabs import area
from rasd_fastapi.models.requests_vocabs import frequency
from rasd_fastapi.models.requests_vocabs import purposes
from rasd_fastapi.schemas import audit as audit_schemas

# Typing
from typing import Any, Optional


class Status(str, enum.Enum):
    """Status Enumeration."""
    NEW = "New"
    ACKNOWLEDGED = "Acknowledged"
    APPROVED = "Approved"
    DECLINED = "Declined"
    DATA_AGREEMENT_SENT = "Data Agreement Sent"
    COMPLETE = "Complete"


class DatasetRequest(base.BaseModel):
    """Dataset Request (Child) Model."""
    # Unique Identifier
    id: types.rasd.RASDIdentifier  # noqa: A003
    # Request Status
    status: Status = Status.NEW
    # Dataset Metadata Information
    metadata_id: uuid.UUID
    metadata_title: str
    metadata_data_source_doi: Optional[types.doi.DOI]
    metadata_data_source_url: Optional[pydantic.HttpUrl]
    # Custodian Information
    custodian_id: uuid.UUID
    custodian_name: str
    custodian_email: pydantic.EmailStr
    # Audit Log
    audit: list[audit_schemas.AuditLogEntry]
    # Notes
    notes: Optional[str]


class DataAccessRequest(base.BaseModel):
    """Data Access Request (Parent) Model."""
    # Unique Identifier
    id: types.rasd.RASDIdentifier = pydantic.Field(default_factory=types.rasd.RASDIdentifier.generate)  # noqa: A003
    # Tracking Information
    created_at: datetime.datetime = pydantic.Field(default_factory=utils.utcnow)
    completed_at: Optional[datetime.datetime] = None
    doi: Optional[types.doi.DOI] = None
    # Dataset Requests Information
    dataset_requests: list[DatasetRequest]
    # Custodian Information (Duplicated for Querying)
    custodian_ids: list[uuid.UUID]
    # Requestor Information
    requestor_id: uuid.UUID
    requestor_given_name: str
    requestor_family_name: str
    requestor_email: pydantic.EmailStr
    requestor_organisation_id: uuid.UUID
    requestor_organisation_name: str
    requestor_organisation_email: pydantic.EmailStr
    # Data Access Request Information (Form)
    requestor_organisation_address: str
    requestor_organisation_indigenous_body: bool
    requestor_orcid: Optional[types.orcid.Orcid]
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

    @pydantic.validator("data_required_from", "data_required_to", always=True)
    def validate_data_required_from_to(cls, v: Optional[str], values: dict[str, Any]) -> Optional[str]:
        """Validates the `data_required_from` and `data_required_to` fields.

        This validator ensures that if a `data_frequency` of "Defined period"
        is selected, then the user *must* also provide both `data_required_to`
        and `data_required_from` values. Otherwise, the user *cannot* provide
        these values.

        Args:
            v (Optional[str]): Supplied value to be validated.
            values (dict[str, Any]): Values of the previously validated fields.

        Returns:
            Optional[str]: The validated value.
        """
        # Retrieve `data_frequency`
        data_frequency = values.get("data_frequency")

        # Check `data_frequency` value
        if data_frequency == frequency.Frequency.DEFINED_PERIOD:
            # Assert value
            assert v, (  # noqa: S101
                f"Both `data_required_from` and `data_required_to` "
                f"must be provided with `data_frequency` of {data_frequency}"
            )

        else:
            # Assert value
            assert not v, (  # noqa: S101
                f"Neither `data_required_from` and `data_required_to` "
                f"can be provided with `data_frequency` of {data_frequency}"
            )

        # Return
        return v

    @pydantic.validator("data_frequency_explanation", always=True)
    def validate_data_frequency_explanation(cls, v: Optional[str], values: dict[str, Any]) -> Optional[str]:
        """Validates the `data_frequency_explanation` field.

        This validator ensures that if a `data_frequency` of "Ongoing" is
        selected, then the user *must* provide a `data_frequency_explanation`
        value. Otherwise, the user *cannot* provide this value.

        Args:
            v (Optional[str]): Supplied value to be validated.
            values (dict[str, Any]): Values of the previously validated fields.

        Returns:
            Optional[str]: The validated value.
        """
        # Retrieve `data_frequency`
        data_frequency = values.get("data_frequency")

        # Check `data_frequency` value
        if data_frequency == frequency.Frequency.ONGOING:
            # Assert value
            assert v, (  # noqa: S101
                f"`data_frequency_explanation` must be provided with `data_frequency` of {data_frequency}"
            )

        else:
            # Assert value
            assert not v, (  # noqa: S101
                f"`data_frequency_explanation` cannot be provided with `data_frequency` of {data_frequency}"
            )

        # Return
        return v

    @pydantic.validator("data_area_explanation", always=True)
    def validate_data_area(cls, v: Optional[str], values: dict[str, Any]) -> Optional[str]:
        """Validates the `data_area_explanation` field.

        This validator ensures that if a `data_area` of "Specific Area" is
        selected, then the user *must* also provide a `data_area_explanation`
        value. Otherwise, the user *cannot* provide this value.

        Args:
            v (Optional[str]): Supplied value to be validated.
            values (dict[str, Any]): Values of the previously validated fields.

        Returns:
            Optional[str]: The validated value.
        """
        # Retrieve `data_area`
        data_area = values.get("data_area")

        # Check `data_area` value
        if data_area == area.Area.SPECIFIC_AREA:
            # Assert value
            assert v, (  # noqa: S101
                f"`data_area_explanation` must be provided with `data_area` of {data_area}"
            )

        else:
            # Assert value
            assert not v, (  # noqa: S101
                f"`data_area_explanation` cannot be provided with `data_area` of {data_area}"
            )

        # Return
        return v

    @pydantic.root_validator
    def validate_classification(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validates the `project_research` and `project_industry` fields.

        This validator ensures that *only one* of `project_research` and
        `project_industry` is provided.

        Args:
            values (dict[str, Any]): Pre-validated values for the model.

        Returns:
            dict[str, Any]: Validated values for the model.
        """
        # Retrieve `project_research` and `project_industry`
        project_research = values.get("project_research")
        project_industry = values.get("project_industry")

        # Assert `project_research` and `project_industry`
        assert (project_research is None) != (project_industry is None), (  # noqa: S101
            "Only one of `project_research` and `project_industry` can be provided"
        )

        # Return validated values
        return values

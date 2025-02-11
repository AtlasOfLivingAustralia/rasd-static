"""RASD FastAPI Audit Log Schemas."""


# Standard
import datetime
import enum

# Third-Party
import pydantic

# Local
from rasd_fastapi import utils
from rasd_fastapi.schemas import base


class Action(str, enum.Enum):
    """Action Enumeration."""
    # The actions below currently match the `models.request.Status` enum, so
    # they may appear redundant. However, this wasn't originally the case, as
    # the wording of each of the actions was different to the request statuses.
    # As such, this enum has been kept in order to provide future flexibility,
    # in case any new actions, statuses or requirements cause them to diverge.
    CREATED = "Created"
    ACKNOWLEDGED = "Acknowledged"
    APPROVED = "Approved"
    DECLINED = "Declined"
    DATA_AGREEMENT_SENT = "Data Agreement Sent"
    COMPLETE = "Complete"


class AuditLogEntry(base.BaseSchema):
    """Audit Log Entry Schema."""
    action: Action
    by: pydantic.EmailStr
    at: datetime.datetime = pydantic.Field(default_factory=utils.utcnow)

"""RASD FastAPI SES Functionality."""


# Third-Party
import boto3

# Local
from rasd_fastapi.core import settings

# Typing
from typing import TYPE_CHECKING

# Type-Checking
if TYPE_CHECKING:
    from mypy_boto3_sesv2.client import SESV2Client


def ses_client() -> "SESV2Client":
    """Constructs a configured and authenticated SESv2 client.

    Returns:
        SESV2Client: Configured and authenticated client.
    """
    # Instantiate and Return AWS Client
    return boto3.client(
        "sesv2",
        region_name=settings.SETTINGS.AWS_DEFAULT_REGION,
        aws_access_key_id=settings.SETTINGS.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SETTINGS.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.SETTINGS.AWS_SESSION_TOKEN,
    )

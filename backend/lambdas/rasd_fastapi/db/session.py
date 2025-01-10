"""RASD FastAPI Database Sessions."""


# Third-Party
import boto3

# Local
from rasd_fastapi.core import settings


def db_session() -> boto3.Session:
    """Constructs an authenticated boto3 session.

    Returns:
        boto3.Session: Authenticated boto3 session.
    """
    # Construct and Return Session
    return boto3.Session(
        region_name=settings.SETTINGS.AWS_DEFAULT_REGION,
        aws_access_key_id=settings.SETTINGS.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SETTINGS.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.SETTINGS.AWS_SESSION_TOKEN,
    )

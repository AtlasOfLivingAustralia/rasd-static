"""RASD FastAPI Health REST API Endpoints."""


# Third-Party
import fastapi

# Local
from rasd_fastapi.services import abn as abn_services
from rasd_fastapi.schemas import abn as abn_schemas


# Router
router = fastapi.APIRouter()


@router.get(r"/lookup/{abn}")
async def lookup_abn(abn: str) -> abn_schemas.AbnLookup:
    """Lookup ABN endpoint for REST API.

    Returns:
        abn_schemas.AbnLookup: ABN Lookup API response.
    """
    # Lookup ABN and Return Results
    return abn_services.lookup_abn(abn)

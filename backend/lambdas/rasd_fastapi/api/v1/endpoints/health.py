"""RASD FastAPI Health REST API Endpoints."""


# Third-Party
import fastapi


# Router
router = fastapi.APIRouter()


@router.get("")
async def health_check() -> fastapi.Response:
    """Health Check endpoint for REST API.

    Returns:
        fastapi.Response: Healthy response if API is alive.
    """
    # Generate Response and Return
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)

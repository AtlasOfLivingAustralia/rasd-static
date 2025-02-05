"""RASD FastAPI REST API v1."""


# Third-Party
import fastapi

# Local
from rasd_fastapi.api.v1.endpoints import abn
from rasd_fastapi.api.v1.endpoints import auth
from rasd_fastapi.api.v1.endpoints import health
from rasd_fastapi.api.v1.endpoints import metadata
from rasd_fastapi.api.v1.endpoints import organisations
from rasd_fastapi.api.v1.endpoints import registration
from rasd_fastapi.api.v1.endpoints import requests


# Router
router = fastapi.APIRouter()
router.include_router(abn.router, prefix="/abn", tags=["ABN"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(metadata.router, prefix="/metadata", tags=["Metadata"])
router.include_router(organisations.router, prefix="/organisations", tags=["Organisations"])
router.include_router(registration.router, prefix="/register", tags=["Registration"])
router.include_router(requests.router, prefix="/access-requests", tags=["Access Requests"])

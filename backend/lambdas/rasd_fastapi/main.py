"""RASD FastAPI Main Module."""


# Third-Party
import fastapi
import starlette.middleware.cors

# Local
from rasd_fastapi import utils
from rasd_fastapi.api import middleware
from rasd_fastapi.api.v1 import api
from rasd_fastapi.core import settings


# Instantiate Application
app = fastapi.FastAPI(
    title=settings.SETTINGS.TITLE,
    version=settings.SETTINGS.VERSION,
    docs_url=f"{settings.SETTINGS.API_PREFIX}/docs",
    redoc_url=f"{settings.SETTINGS.API_PREFIX}/redoc",
    openapi_url=f"{settings.SETTINGS.API_PREFIX}/openapi.json",
)

# Add Middleware
app.add_middleware(
    starlette.middleware.cors.CORSMiddleware,
    allow_origins=settings.SETTINGS.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    middleware.AWSAPIGatewayMiddleware,
)

# Add Routers
app.include_router(api.router, prefix=settings.SETTINGS.API_PREFIX)

# Add Redirects
utils.add_redirect(app, "/", app.docs_url)
utils.add_redirect(app, "/api", app.docs_url)
utils.add_redirect(app, "/api/v1", app.docs_url)

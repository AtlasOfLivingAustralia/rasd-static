"""RASD FastAPI Mangum Handler."""


# Third-Party
import mangum

# Local
from rasd_fastapi import main


# Instantiate Mangum Handler
handler = mangum.Mangum(main.app)

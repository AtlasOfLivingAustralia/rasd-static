"""RASD FastAPI REST API Middleware."""


# Third-Party
import fastapi
import fastapi.applications

# Typing
from typing import Awaitable, Callable, cast


# Constants
RequestResponseEndpoint = Callable[[fastapi.Request], Awaitable[fastapi.Response]]


class AWSAPIGatewayMiddleware(fastapi.applications.BaseHTTPMiddleware):
    """Handles FastAPI `root_path` dynamically from ASGI request data.

    Mangum injects the AWS event data into the request scope, which we can use
    to dynamically set the `root_path` on the `fastapi` ASGI app if required.

    This middleware provides correct functionality in the following cases:
        * API Local development
        * API behind an AWS API Gateway (w/ stage)
        * API behind an AWS API Gateway *with* a custom domain (w/ stage)

    See: https://github.com/jordaneremieff/mangum/issues/147
    """

    async def dispatch(
        self,
        request: fastapi.Request,
        call_next: RequestResponseEndpoint
    ) -> fastapi.Response:
        """Process the request and call the next middleware.

        Args:
            request (fastapi.Request): Intercepted request object.
            call_next (RequestResponseEndpoint): Middleware to call next.

        Returns:
            fastapi.Response: The response modified by the middleware.
        """
        # Cast `self.app` to an instance of `fastapi.FastAPI` to assist `mypy`
        # This is a no-op at runtime
        self.app = cast(fastapi.FastAPI, self.app)

        # Check for and retrieve `root_path` from request scope
        if root_path := request.scope.get("root_path"):
            # The `root_path` in the request scope scope is part of the ASGI
            # spec, and if it is provided then we assume it is set correctly.
            # See: https://asgi.readthedocs.io/en/latest/specs/www.html
            self.app.root_path = root_path

        # Check for and retrieve AWS Event from request scope
        elif aws_event := request.scope.get("aws.event"):
            # The `mangum` adapter injects the AWS API Gateway event into the
            # request scope. In this case, we know that we are behind an AWS
            # API Gateway. We retrieve the `stage`, `apiId` and `domainPrefix`
            # from the event's `requestContext` for further processing.
            stage = aws_event["requestContext"]["stage"]
            api_id = aws_event["requestContext"]["apiId"]
            domain_prefix = aws_event["requestContext"]["domainPrefix"]

            # If the stage is `$default`, then we don't need to do anything
            # because the AWS API Gateway will not prefix the URL with the
            # `stage`. We also need to check that we aren't behind a custom
            # domain, which will not be prefixed either. If we are behind the
            # default AWS API Gateway domain, then the `apiId` will match the
            # `domainPrefix` which is checked below.
            if stage != "$default" and api_id == domain_prefix:
                # Set `root_path` to AWS API Gateway `stage` in `requestContext`
                stage_path = f"/{stage}"
                self.app.root_path = stage_path
                request.scope["root_path"] = stage_path

        else:
            # Assume local development in this case, no changes required
            pass

        # Call Next
        response = await call_next(request)

        # Return
        return response

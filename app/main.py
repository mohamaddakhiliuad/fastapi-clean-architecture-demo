"""
MaxCopy Backend entrypoint.

Responsibilities:
- Create FastAPI application instance.
- Include API routers.
- Provide a basic health check endpoint.
"""

from fastapi import FastAPI

from app.api.v1.products import router as products_router


def create_app() -> FastAPI:
    """
    Application factory.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="MaxCopy Backend",
        version="0.1.0",
    )

    # Register API routers
    app.include_router(products_router, prefix="/api/v1")

    @app.get("/health", tags=["system"])
    def health_check():
        """
        Simple health check endpoint.
        """
        return {"status": "ok"}

    return app


app = create_app()

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from settings.config import settings

# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A simple expense tracker API",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns the status and basic information about the application.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "environment": settings.APP_ENV,
            "project": settings.PROJECT_NAME,
        },
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_PREFIX}/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.is_development,
    )

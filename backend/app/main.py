"""
FastAPI application for the Transcriber backend.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.v1.routes import router as api_router


app = FastAPI(
    title=settings.APP_NAME,
    description="Transcription API with speaker diarization",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.exception_handler(413)
async def request_too_large_handler(request, exc):
    """Handle 413 Request Entity Too Large."""
    return JSONResponse(
        status_code=413,
        content={"error": "File too large", "message": str(exc)}
    )


@app.exception_handler(400)
async def bad_request_handler(request, exc):
    """Handle 400 Bad Request."""
    return JSONResponse(
        status_code=400,
        content={"error": "Bad request", "message": str(exc)}
    )


# Include routers
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
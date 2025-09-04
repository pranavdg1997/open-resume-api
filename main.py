"""
OpenResume FastAPI Backend
A FastAPI wrapper for OpenResume's resume builder functionality
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from typing import Dict, Any
import os
from datetime import datetime

from models.resume_models import ResumeData, ResumeResponse
from services.pdf_generator import PDFGenerator
from services.config_manager import ConfigManager
from api.endpoints import router
from utils.validators import validate_resume_data
import constants

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=constants.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=constants.APP_TITLE,
    description=constants.APP_DESCRIPTION,
    version=constants.APP_VERSION,
    docs_url=constants.DOCS_URL,
    redoc_url=constants.REDOC_URL
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=constants.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=constants.CORS_ALLOW_METHODS,
    allow_headers=constants.CORS_ALLOW_HEADERS,
)

# Mount static files
app.mount("/static", StaticFiles(directory=constants.STATIC_DIR), name="static")

# Initialize services
config_manager = ConfigManager()
pdf_generator = PDFGenerator(config_manager)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info(f"Starting {constants.APP_TITLE}...")
    try:
        config_manager.load_config()
        logger.info(constants.CONFIG_LOADED_SUCCESS)
    except Exception as e:
        logger.error(f"{constants.CONFIG_LOAD_ERROR}: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info(f"Shutting down {constants.APP_TITLE}...")

# Include API routes
app.include_router(router, prefix=constants.API_PREFIX)

@app.get("/", response_class=HTMLResponse)
async def frontend():
    """Serve the frontend interface"""
    try:
        with open(constants.INDEX_HTML, "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(f"<h1>Frontend not found</h1><p>Please check {constants.INDEX_HTML}</p>")

@app.get("/api")
async def root():
    """API information endpoint"""
    return {
        "message": constants.APP_TITLE,
        "version": constants.APP_VERSION,
        "description": constants.APP_DESCRIPTION,
        "docs_url": constants.DOCS_URL,
        "endpoints": {
            "generate_resume": f"{constants.API_PREFIX}{constants.GENERATE_RESUME_ENDPOINT}",
            "health": f"{constants.API_PREFIX}{constants.HEALTH_ENDPOINT}",
            "config": f"{constants.API_PREFIX}{constants.CONFIG_ENDPOINT}"
        }
    }

@app.get("/validated_resume.json")
async def get_sample_data():
    """Serve comprehensive sample resume data for frontend"""
    try:
        return FileResponse(constants.COMPREHENSIVE_SAMPLE_FILE)
    except FileNotFoundError:
        # Fallback to original if comprehensive doesn't exist
        try:
            return FileResponse(constants.VALIDATED_SAMPLE_FILE)
        except FileNotFoundError:
            raise HTTPException(status_code=constants.HTTP_404_NOT_FOUND, detail=constants.SAMPLE_DATA_NOT_FOUND)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": constants.SERVICE_HEALTHY,
        "service": constants.APP_TITLE,
        "version": constants.APP_VERSION
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": str(datetime.now())
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=constants.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "status_code": constants.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", str(constants.DEFAULT_PORT)))
    host = os.getenv("HOST", constants.DEFAULT_HOST)
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

"""
OpenResume FastAPI Backend
A FastAPI wrapper for OpenResume's resume builder functionality
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from typing import Dict, Any
import os

from models.resume_models import ResumeData, ResumeResponse
from services.pdf_generator import PDFGenerator
from services.config_manager import ConfigManager
from api.endpoints import router
from utils.validators import validate_resume_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="OpenResume API",
    description="A FastAPI wrapper for OpenResume's resume builder functionality",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
config_manager = ConfigManager()
pdf_generator = PDFGenerator(config_manager)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting OpenResume API...")
    try:
        config_manager.load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down OpenResume API...")

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "OpenResume API",
        "version": "1.0.0",
        "description": "FastAPI wrapper for OpenResume resume builder",
        "docs_url": "/docs",
        "endpoints": {
            "generate_resume": "/api/v1/generate-resume",
            "health": "/api/v1/health",
            "config": "/api/v1/config"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "OpenResume API",
        "version": "1.0.0"
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
            "timestamp": str(pd.Timestamp.now())
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "status_code": 500
        }
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

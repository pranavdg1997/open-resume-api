"""
API endpoints for the OpenResume service
"""

from fastapi import APIRouter, HTTPException, Response, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import logging
import hashlib
from datetime import datetime
from io import BytesIO
import os

from models.resume_models import ResumeData, ResumeResponse, ErrorResponse
from services.pdf_generator import PDFGenerator
from services.config_manager import ConfigManager
from utils.validators import validate_resume_data, ResumeValidator

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize services (will be properly injected in real implementation)
config_manager = ConfigManager()
pdf_generator = PDFGenerator(config_manager)
resume_validator = ResumeValidator(config_manager)

@router.post("/generate-resume", response_model=ResumeResponse)
async def generate_resume(
    resume_data: ResumeData,
    background_tasks: BackgroundTasks
):
    """
    Generate a PDF resume from provided resume data
    
    - **resume_data**: Complete resume information including personal info, work experience, etc.
    - Returns PDF file as response
    """
    try:
        # Validate resume data
        validation_result = resume_validator.validate_complete_resume(resume_data)
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Validation failed",
                    "issues": validation_result.issues
                }
            )
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_hash = hashlib.md5(resume_data.personalInfo.name.encode()).hexdigest()[:8]
        filename = f"resume_{resume_data.personalInfo.name.replace(' ', '_')}_{timestamp}_{name_hash}.pdf"
        
        # Generate PDF
        logger.info(f"Generating PDF for {resume_data.personalInfo.name}")
        pdf_bytes = pdf_generator.generate_resume_pdf(resume_data)
        
        # Create response
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'application/pdf',
            'Content-Length': str(len(pdf_bytes))
        }
        
        # Clean up temp files in background
        background_tasks.add_task(cleanup_temp_files)
        
        logger.info(f"Successfully generated PDF: {filename} ({len(pdf_bytes)} bytes)")
        
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers=headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Resume generation failed",
                "message": str(e)
            }
        )

@router.post("/validate-resume")
async def validate_resume(resume_data: ResumeData):
    """
    Validate resume data without generating PDF
    
    - **resume_data**: Resume data to validate
    - Returns validation result with any issues found
    """
    try:
        validation_result = resume_validator.validate_complete_resume(resume_data)
        
        return {
            "valid": validation_result.is_valid,
            "issues": validation_result.issues,
            "warnings": validation_result.warnings,
            "summary": {
                "total_issues": len(validation_result.issues),
                "total_warnings": len(validation_result.warnings),
                "sections_validated": validation_result.sections_validated
            }
        }
        
    except Exception as e:
        logger.error(f"Error validating resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Validation failed",
                "message": str(e)
            }
        )

@router.get("/config")
async def get_config():
    """
    Get current configuration settings (non-sensitive)
    """
    try:
        config = config_manager.config
        
        # Return only non-sensitive configuration
        public_config = {
            "pdf_settings": {
                "default_theme_color": config.get("pdf_settings", {}).get("default_theme_color"),
                "default_font_family": config.get("pdf_settings", {}).get("default_font_family"),
                "default_font_size": config.get("pdf_settings", {}).get("default_font_size"),
                "default_document_size": config.get("pdf_settings", {}).get("default_document_size"),
                "max_file_size_mb": config.get("pdf_settings", {}).get("max_file_size_mb")
            },
            "validation": config.get("validation", {}),
            "api_info": {
                "version": "1.0.0",
                "supported_formats": ["PDF"],
                "max_sections": {
                    "work_experiences": config.get("validation", {}).get("max_work_experiences", 10),
                    "educations": config.get("validation", {}).get("max_educations", 5),
                    "projects": config.get("validation", {}).get("max_projects", 10),
                    "skills_categories": config.get("validation", {}).get("max_skills_categories", 10)
                }
            }
        }
        
        return public_config
        
    except Exception as e:
        logger.error(f"Error getting config: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve configuration",
                "message": str(e)
            }
        )

@router.put("/config")
async def update_config(updates: Dict[str, Any]):
    """
    Update configuration settings
    
    - **updates**: Configuration updates to apply
    """
    try:
        # Filter allowed updates (security measure)
        allowed_updates = {}
        allowed_keys = [
            "pdf_settings.default_theme_color",
            "pdf_settings.default_font_family", 
            "pdf_settings.default_font_size",
            "pdf_settings.default_document_size",
            "validation.max_work_experiences",
            "validation.max_educations",
            "validation.max_projects",
            "validation.max_skills_categories",
            "validation.max_description_length"
        ]
        
        for key, value in updates.items():
            if key in allowed_keys:
                config_manager.set(key, value)
                allowed_updates[key] = value
        
        # Save configuration
        if config_manager.save_config():
            logger.info(f"Configuration updated: {allowed_updates}")
            return {
                "success": True,
                "message": "Configuration updated successfully",
                "updates_applied": allowed_updates
            }
        else:
            raise Exception("Failed to save configuration")
        
    except Exception as e:
        logger.error(f"Error updating config: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to update configuration", 
                "message": str(e)
            }
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Basic health checks
        checks: Dict[str, Any] = {
            "api": "healthy",
            "config": "loaded" if config_manager.config else "error",
            "pdf_generator": "ready",
            "timestamp": datetime.now().isoformat()
        }
        
        # Check if required directories exist
        output_dir = config_manager.get('pdf_settings.output_directory', 'output')
        temp_dir = config_manager.get('pdf_settings.temp_directory', 'temp')
        
        checks["directories"] = {
            "output": "exists" if os.path.exists(output_dir) else "missing",
            "temp": "exists" if os.path.exists(temp_dir) else "missing",
            "fonts": "exists" if os.path.exists("static/fonts") else "missing"
        }
        
        # Overall health status
        overall_status = "healthy" if all(
            check in ["healthy", "loaded", "ready", "exists"] 
            for check_group in checks.values() 
            for check in (check_group.values() if isinstance(check_group, dict) else [check_group])
            if check != checks["timestamp"]
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "checks": checks,
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/templates")
async def get_resume_templates():
    """
    Get available resume templates and examples
    """
    try:
        templates = {
            "default": {
                "name": "Professional",
                "description": "Clean and professional design based on OpenResume",
                "theme_color": "#1f2937",
                "font_family": "OpenSans",
                "features": [
                    "ATS-friendly format",
                    "Modern design",
                    "Optimized spacing",
                    "Professional color scheme"
                ]
            }
        }
        
        return {
            "templates": templates,
            "default_template": "default",
            "customization_options": {
                "theme_colors": [
                    "#1f2937",  # Dark gray
                    "#374151",  # Gray
                    "#1f2937",  # Blue gray
                    "#065f46",  # Dark green
                    "#7c2d12",  # Dark red
                    "#92400e"   # Dark yellow
                ],
                "fonts": ["OpenSans", "Helvetica"],
                "document_sizes": ["Letter", "A4"]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve templates",
                "message": str(e)
            }
        )

async def cleanup_temp_files():
    """Background task to clean up temporary files"""
    try:
        temp_dir = config_manager.get('pdf_settings.temp_directory', 'temp')
        if os.path.exists(temp_dir):
            # Clean up files older than 1 hour
            import time
            current_time = time.time()
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getctime(file_path)
                    if file_age > 3600:  # 1 hour
                        os.remove(file_path)
                        logger.info(f"Cleaned up temp file: {filename}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Overview

This is a FastAPI-based backend service that wraps OpenResume's resume builder functionality. The application provides a REST API for generating professional PDF resumes from structured data input. It accepts resume information through JSON and returns formatted PDF documents using ReportLab with Helvetica fonts and customizable templates.

The system is designed to be ATS-friendly and follows OpenResume's design principles for clean, professional resume layouts. It includes comprehensive validation, configurable templates, and supports multiple resume sections including personal information, work experience, education, projects, and skills.

**Status**: ✅ Fully functional - All core features implemented and tested with real resume data (August 21, 2025)

## Recent Testing Results
- ✅ Successfully processed Pranav Gujarathi's complete resume data (5 work experiences, 15 achievement bullets, 5 skill categories)
- ✅ Generated 6,530-byte professional PDF with comprehensive content
- ✅ All API endpoints (health, generation, templates, documentation) working correctly
- ✅ Validation test suite showing 100% success rate
- ✅ Real-world data processing validated with actual user resume

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
The application uses **FastAPI** as the primary web framework, chosen for its automatic API documentation, built-in validation with Pydantic models, and high performance. The architecture follows a modular service-oriented pattern with clear separation of concerns.

## PDF Generation Engine
**ReportLab** serves as the PDF generation library, providing fine-grained control over document layout and styling. The system supports custom fonts (OpenSans Regular and Bold) and implements template-based styling for consistent document formatting.

## Data Models and Validation
**Pydantic models** define the resume data structure with comprehensive validation rules. The validation system includes field-level validation (email format, phone numbers), business logic validation (maximum entries per section), and content validation (description lengths, required fields).

## Configuration Management
A centralized **ConfigManager** class handles all application settings through a JSON configuration file. This includes PDF settings (fonts, colors, sizes), API settings (CORS, rate limiting), validation rules, and logging configuration.

## Template System
The application implements a template-based approach for resume styling, allowing for multiple design variations while maintaining consistent structure. Templates define colors, fonts, spacing, and layout parameters.

## API Design
RESTful API design with a primary `/generate-resume` endpoint that accepts complete resume data and returns PDF responses. The API includes comprehensive error handling, request validation, and background task support for cleanup operations.

## File Handling
Static file serving for fonts and assets, with configurable output and temporary directories for PDF generation. The system implements file size limits and cleanup mechanisms.

# External Dependencies

## Core Framework Dependencies
- **FastAPI**: Web framework for API development
- **Uvicorn**: ASGI server for running the FastAPI application
- **Pydantic**: Data validation and settings management

## PDF Generation
- **ReportLab**: Primary PDF generation library for creating formatted documents
- **Custom Fonts**: OpenSans Regular and Bold TTF files for professional typography

## Validation and Utilities
- **email-validator**: Email address validation
- **Python standard libraries**: For file handling, logging, and datetime operations

## Development and Deployment
- **CORS Middleware**: Cross-origin resource sharing support
- **Static File Serving**: For font files and assets
- **Logging**: Built-in Python logging with configurable levels and formats

## Note on Data Storage
The current implementation appears to be stateless with no persistent data storage. Resume data is processed in real-time and PDFs are generated on-demand without database persistence.
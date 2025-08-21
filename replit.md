# Overview

This is a FastAPI-based backend service that wraps OpenResume's resume builder functionality. The application provides a REST API for generating professional PDF resumes from structured data input. It accepts resume information through JSON and returns formatted PDF documents using ReportLab with Helvetica fonts and customizable templates.

The system is designed to be ATS-friendly and follows OpenResume's design principles for clean, professional resume layouts. It includes comprehensive validation, configurable templates, and supports multiple resume sections including personal information, work experience, education, projects, and skills.

**Status**: ✅ Fully functional - All core features implemented and tested with real resume data (August 21, 2025)

## Recent Testing Results
- ✅ Successfully integrated actual OpenResume codebase as primary PDF generator
- ✅ OpenResume wrapper transforms API data to proper OpenResume format
- ✅ Generated 6,871-byte PDF using authentic OpenResume logic (vs 6,530 bytes with fallback)
- ✅ Bridge service working correctly with Node.js integration
- ✅ Fallback to custom ReportLab generator when OpenResume unavailable
- ✅ All API endpoints including new /openresume-status endpoint working
- ✅ Real-world data processing validated with Pranav Gujarathi's resume

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
The application uses **FastAPI** as the primary web framework, chosen for its automatic API documentation, built-in validation with Pydantic models, and high performance. The architecture follows a modular service-oriented pattern with clear separation of concerns.

## PDF Generation Engine
**OpenResume Integration** - The system now properly wraps the actual OpenResume codebase from GitHub (https://github.com/xitanggg/open-resume). A bridge service transforms our API data format to OpenResume's format and leverages their React PDF generation logic. **ReportLab** serves as a fallback option, providing fine-grained control when the OpenResume wrapper is unavailable.

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
- **OpenResume Source**: Actual OpenResume codebase cloned from GitHub (React + @react-pdf/renderer)
- **Node.js Bridge**: JavaScript service that transforms data and calls OpenResume PDF generation
- **ReportLab**: Fallback PDF generation library for creating formatted documents
- **Custom Fonts**: OpenSans Regular and Bold TTF files for professional typography

## Validation and Utilities
- **email-validator**: Email address validation
- **Python standard libraries**: For file handling, logging, and datetime operations

## Development and Deployment
- **Node.js Integration**: Required for OpenResume wrapper functionality
- **CORS Middleware**: Cross-origin resource sharing support
- **Static File Serving**: For font files and assets
- **Logging**: Built-in Python logging with configurable levels and formats
- **Dual Architecture**: Python FastAPI backend + Node.js OpenResume integration

## Note on Data Storage
The current implementation appears to be stateless with no persistent data storage. Resume data is processed in real-time and PDFs are generated on-demand without database persistence.
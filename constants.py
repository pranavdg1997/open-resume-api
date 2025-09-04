"""
Application Constants
Centralized constants for file paths, directories, and configuration values
"""

import os

# ============================================================================
# DIRECTORY CONSTANTS
# ============================================================================

# Core directories
STATIC_DIR = "static"
TESTS_DIR = "tests"
OUTPUT_DIR = "output"
TEMP_DIR = "temp"
SERVICES_DIR = "services"
API_DIR = "api"
MODELS_DIR = "models"
UTILS_DIR = "utils"
TEMPLATES_DIR = "templates"

# External source directories
OPENRESUME_SOURCE_DIR = "openresume-source"

# Static subdirectories
FONTS_DIR = os.path.join(STATIC_DIR, "fonts")

# ============================================================================
# FILE CONSTANTS
# ============================================================================

# Configuration files
CONFIG_FILE = "config.json"
CONFIG_EXAMPLE_FILE = "config.example.json"

# Application entry point
MAIN_FILE = "main.py"

# JavaScript bridge files
OPENRESUME_BRIDGE_SCRIPT = "openresume_pdf_generator.js"
OPENRESUME_BRIDGE_FALLBACK = "openresume_bridge.js"

# Sample data files
COMPREHENSIVE_SAMPLE_FILE = os.path.join(TESTS_DIR, "comprehensive_sample_resume.json")
VALIDATED_SAMPLE_FILE = os.path.join(TESTS_DIR, "validated_resume.json")
TEST_SAMPLE_FILE = os.path.join(TESTS_DIR, "test_sample_data.json")

# Static files
INDEX_HTML = os.path.join(STATIC_DIR, "index.html")

# Font files
OPENSANS_REGULAR_FONT = os.path.join(FONTS_DIR, "OpenSans-Regular.ttf")
OPENSANS_BOLD_FONT = os.path.join(FONTS_DIR, "OpenSans-Bold.ttf")

# ============================================================================
# API CONSTANTS
# ============================================================================

# API configuration
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# API endpoints
HEALTH_ENDPOINT = "/health"
CONFIG_ENDPOINT = "/config"
GENERATE_RESUME_ENDPOINT = "/generate-resume"

# ============================================================================
# PDF GENERATION CONSTANTS
# ============================================================================

# PDF settings
DEFAULT_PDF_FONT_SIZE = 10
DEFAULT_PDF_MARGIN = 50
PDF_FILE_EXTENSION = ".pdf"

# Output file patterns
PDF_OUTPUT_PATTERN = "resume_{timestamp}.pdf"
TEMP_FILE_PATTERN = "temp_{timestamp}"

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================

# File size limits (in MB)
MAX_FILE_SIZE_MB = 10
MAX_PDF_SIZE_MB = 5

# Content limits
MAX_DESCRIPTION_LENGTH = 1000
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 100
MAX_PHONE_LENGTH = 20
MAX_SUMMARY_LENGTH = 500

# Validation ranges
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 16
MAX_GPA_VALUE = 4.0

# Date validation patterns
DATE_PATTERNS = [
    r'\w+ \d{4} - \w+ \d{4}',  # Jan 2020 - Dec 2021
    r'\w+ \d{4} - Present',     # Jan 2020 - Present
    r'\d{4} - \d{4}',          # 2020 - 2021
    r'\d{4} - Present'          # 2020 - Present
]

# Color validation pattern
COLOR_PATTERN = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

# Valid document sizes
VALID_DOCUMENT_SIZES = ["Letter", "A4"]

# Allowed configuration keys for updates
ALLOWED_CONFIG_KEYS = [
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

# ============================================================================
# SERVER CONSTANTS
# ============================================================================

# Server configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000
DEFAULT_TIMEOUT = 30

# CORS settings
CORS_ALLOW_ORIGINS = ["*"]
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# ============================================================================
# LOGGING CONSTANTS
# ============================================================================

# Log levels
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_WARNING = "WARNING"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# APPLICATION METADATA
# ============================================================================

# Application information
APP_TITLE = "OpenResume API"
APP_DESCRIPTION = "A FastAPI wrapper for OpenResume's resume builder functionality"
APP_VERSION = "1.0.0"

# Documentation URLs
DOCS_URL = "/docs"
REDOC_URL = "/redoc"

# ============================================================================
# ERROR MESSAGES
# ============================================================================

# File error messages
FILE_NOT_FOUND_ERROR = "File not found"
SAMPLE_DATA_NOT_FOUND = "Sample data not found"
CONFIG_LOAD_ERROR = "Failed to load configuration"

# Validation error messages
INVALID_EMAIL_ERROR = "Invalid email format"
INVALID_PHONE_ERROR = "Invalid phone number format"
REQUIRED_FIELD_ERROR = "Field is required"

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SERVICE_HEALTHY = "healthy"
CONFIG_LOADED_SUCCESS = "Configuration loaded successfully"
PDF_GENERATED_SUCCESS = "PDF generated successfully"

# ============================================================================
# HTTP STATUS CODES
# ============================================================================

HTTP_200_OK = 200
HTTP_404_NOT_FOUND = 404
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500
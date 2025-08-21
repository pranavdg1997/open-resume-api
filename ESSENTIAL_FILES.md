# Essential Files for OpenResume API Wrapper

## Core Application Files (Required)
- `main.py` - FastAPI application entry point
- `config.json` - Application configuration
- `pyproject.toml` - Python dependencies
- `uv.lock` - Lock file for dependencies

## API Layer
- `api/endpoints.py` - REST API endpoints
- `models/resume_models.py` - Pydantic data models

## Service Layer
- `services/config_manager.py` - Configuration management
- `services/openresume_wrapper.py` - OpenResume integration wrapper
- `services/pdf_generator.py` - PDF generation service (fallback)

## Template System
- `templates/resume_template.py` - Resume formatting templates

## Utilities
- `utils/validators.py` - Data validation utilities

## OpenResume Integration (Required)
- `openresume_bridge.js` - Node.js bridge to OpenResume
- `openresume-source/` - Actual OpenResume repository (cloned)
  - Key files: package.json, src/, next.config.js, etc.

## Documentation
- `README.md` - Project documentation with installation instructions
- `DEPENDENCIES.md` - Requirements reference (serves as requirements.txt)
- `replit.md` - Architecture and user preferences
- `ESSENTIAL_FILES.md` - File structure guide
- `.gitignore` - Git ignore patterns

## Infrastructure
- `.replit` - Replit configuration
- `static/` - Static assets (fonts)

## Git Commands for Clean Commit

```bash
# Add only essential files
git add main.py config.json pyproject.toml uv.lock
git add api/ models/ services/ templates/ utils/
git add openresume_bridge.js openresume-source/
git add README.md DEPENDENCIES.md replit.md ESSENTIAL_FILES.md .gitignore
git add static/ .replit

# Commit with meaningful message
git commit -m "feat: OpenResume API wrapper with authentic integration

- FastAPI backend wrapping actual OpenResume codebase
- Node.js bridge for data transformation and PDF generation
- ReportLab fallback when OpenResume unavailable
- Comprehensive validation and configuration management
- REST API with /generate-resume and /openresume-status endpoints"
```

## Size Optimization Notes
- Original repo ~56MB (mostly OpenResume source)
- Essential code files ~50KB
- Can be reduced by removing OpenResume .git, tests, docs if needed
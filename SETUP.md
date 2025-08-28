# Local Setup Guide

This guide helps you set up the OpenResume API on your local machine.

## Quick Setup

1. **Clone and install:**
   ```bash
   git clone <your-repo-url>
   cd openresume-api
   pip install fastapi uvicorn reportlab pydantic email-validator
   npm install @react-pdf/renderer react react-dom
   ```

2. **Configure:**
   ```bash
   cp config.example.json config.json
   # Edit config.json as needed
   ```

3. **Run:**
   ```bash
   python main.py
   # Server runs on http://localhost:5000
   ```

4. **Test:**
   ```bash
   curl -X POST http://localhost:5000/api/v1/generate-resume \
     -H "Content-Type: application/json" \
     -d @tests/test_sample_data.json \
     --output my_resume.pdf
   ```

## What's Included

- **Core API**: FastAPI backend with OpenResume integration
- **Test Suite**: Sample resumes and test files in `tests/` folder
- **Configuration**: Template config file and documentation
- **Dependencies**: All Python and Node.js packages specified

## What's Excluded (Replit-specific)

- `.replit` - Replit configuration
- `replit.md` - Replit project documentation  
- `uv.lock`, `pyproject.toml` - Replit package management
- `attached_assets/` - Temporary test files
- `openresume-source/` - Development OpenResume source

## File Structure

```
├── api/              # API endpoints
├── models/           # Data models
├── services/         # Business logic
├── utils/            # Utilities
├── templates/        # Resume templates
├── static/           # Static assets
├── tests/            # Test files and samples
├── config.example.json # Configuration template
└── main.py           # Application entry point
```
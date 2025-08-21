# OpenResume API

A FastAPI-based backend service that converts resume data into professional PDF documents, based on OpenResume's design principles.

## Features

✅ **Resume Generation**: Convert JSON resume data to professional PDF format  
✅ **ATS-Friendly**: Clean layouts optimized for Applicant Tracking Systems  
✅ **Comprehensive Validation**: Field validation and business logic checks  
✅ **Configurable Templates**: Customizable colors, fonts, and document settings  
✅ **REST API**: Complete RESTful interface with automatic documentation  
✅ **Health Monitoring**: Status endpoints for monitoring and debugging  

## Quick Start

### 1. Start the Server
```bash
python main.py
```
The server runs on `http://localhost:5000`

### 2. Generate a Resume
```bash
curl -X POST http://localhost:5000/api/v1/generate-resume \
  -H "Content-Type: application/json" \
  -d @test_resume.json \
  --output my_resume.pdf
```

### 3. View API Documentation
Visit `http://localhost:5000/docs` for interactive API documentation

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/generate-resume` | POST | Generate PDF from resume data |
| `/api/v1/health` | GET | Health check and system status |
| `/api/v1/templates` | GET | Available resume templates |
| `/docs` | GET | Interactive API documentation |

## Resume Data Format

```json
{
  "personalInfo": {
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "phone": "555-123-4567",
    "url": "https://johndoe.dev",
    "summary": "Experienced software engineer...",
    "location": "San Francisco, CA"
  },
  "workExperiences": [
    {
      "company": "Tech Corp",
      "jobTitle": "Senior Software Engineer",
      "date": "2022 - Present",
      "descriptions": ["Led development of microservices..."]
    }
  ],
  "educations": [...],
  "projects": [...],
  "skills": [...],
  "settings": {
    "themeColor": "#2563eb",
    "fontFamily": "Helvetica",
    "fontSize": "11",
    "documentSize": "Letter"
  }
}
```

## Configuration

The application uses `config.json` for settings:

- **PDF Settings**: Font preferences, document size, output directories
- **API Settings**: Rate limiting, CORS, request size limits
- **Validation Rules**: Field requirements, content limits
- **Logging**: Log levels and output format

## Testing

Run the validation test suite:
```bash
python test_api_validation.py
```

This verifies:
- API health and responsiveness
- PDF generation functionality
- Template endpoint availability
- Generated file integrity

## Architecture

- **FastAPI**: High-performance web framework with automatic API docs
- **ReportLab**: Professional PDF generation with precise layout control
- **Pydantic**: Data validation and serialization
- **Modular Design**: Separate services for PDF generation, configuration, and validation

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `reportlab` - PDF generation
- `pydantic` - Data validation
- `email-validator` - Email format validation

## Production Notes

- Server runs on port 5000 by default
- Uses standard Helvetica fonts for maximum compatibility
- Includes comprehensive error handling and logging
- Supports configurable rate limiting and CORS

## Success Metrics

As of August 21, 2025:
- ✅ All API endpoints functioning correctly
- ✅ PDF generation producing ~3KB professional documents
- ✅ 100% test pass rate on validation suite
- ✅ Interactive documentation available
- ✅ Error handling and logging implemented
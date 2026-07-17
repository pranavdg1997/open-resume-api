# OpenResume API Wrapper

FastAPI service for turning structured JSON resumes into ATS-friendly PDF resumes. The primary renderer is a local React PDF generator (`openresume_pdf_generator.js`) using `@react-pdf/renderer`; the Python ReportLab generator remains as a fallback path.

## What It Does

- Accepts resume JSON through a REST API.
- Validates input with Pydantic models.
- Generates a compact, single-column PDF designed for applicant tracking systems.
- Supports contact links, publication links, structured skills, work experience, education, projects, certifications, and custom sections.
- Uses ReportLab only if the primary Node/React renderer fails.

## Current PDF Layout

The primary PDF renderer is optimized for dense technical resumes:

- Compact font scale based on `settings.fontSize` with body text reduced by 2 points.
- Tight section and item spacing, especially in education.
- Plain text, single-column order for ATS compatibility.
- Publications render under `PUBLICATIONS AND ACHIEVEMENTS`.
- Publication titles become clickable links when a publication includes `url`.

## Requirements

- Python 3.11+
- Node.js 18+
- npm

## Install

```bash
pip install -r requirements.txt
npm install
cp config.example.json config.json
```

## Run The API

```bash
python main.py
```

The API runs on `http://localhost:5000` by default.

Interactive docs are available at:

```text
http://localhost:5000/docs
```

## Generate A Resume Through The API

```bash
curl -X POST http://localhost:5000/api/v1/generate-resume \
  -H "Content-Type: application/json" \
  -d @path/to/resume.json \
  --output resume.pdf
```

## Generate PDFs From Local JSON Files

Put JSON resumes in `.resumes/`, then run:

```bash
python scripts/generate_pdfs_from_json.py
```

Custom input/output directories:

```bash
python scripts/generate_pdfs_from_json.py \
  --input path/to/json-resumes \
  --output path/to/pdf-output
```

## Direct Node Renderer

For quick renderer-only checks:

```bash
node openresume_pdf_generator.js path/to/resume.json > resume.pdf
```

## Resume JSON Shape

Minimal example:

```json
{
  "personalInfo": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1 555 123 4567",
    "url": "https://johndoe.dev",
    "linkedin": "https://linkedin.com/in/johndoe",
    "location": "Austin, TX",
    "summary": "Experienced AI engineer..."
  },
  "workExperiences": [
    {
      "company": "Example Corp",
      "jobTitle": "Senior AI Engineer",
      "date": "2024 - Present",
      "location": "Remote",
      "descriptions": [
        "Built production LLM workflows with RAG and evaluation harnesses."
      ]
    }
  ],
  "educations": [
    {
      "school": "Example University",
      "degree": "MS, Computer Science",
      "date": "2020 - 2022",
      "descriptions": []
    }
  ],
  "skills": [
    {
      "category": "Engineering",
      "skills": ["Python", "Docker", "Kubernetes", "REST APIs"]
    }
  ],
  "publications": [
    {
      "name": "Example Publication",
      "date": "ACM 2024",
      "url": "https://example.com/paper",
      "descriptions": ["Best Paper Award."]
    }
  ],
  "settings": {
    "themeColor": "#1f2937",
    "fontFamily": "Helvetica",
    "fontSize": "11",
    "documentSize": "Letter"
  }
}
```

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/generate-resume` | POST | Generate a PDF from resume JSON |
| `/api/v1/validate-resume` | POST | Validate resume JSON without generating a PDF |
| `/api/v1/openresume-status` | GET | Check primary renderer integration status |
| `/api/v1/health` | GET | Health check |
| `/api/v1/templates` | GET | List template metadata |
| `/docs` | GET | FastAPI interactive documentation |

## Architecture

- `main.py`: FastAPI app entrypoint.
- `api/endpoints.py`: API routes and generation endpoint.
- `models/resume_models.py`: Pydantic resume schema.
- `services/openresume_wrapper.py`: Converts validated data and calls the Node renderer.
- `openresume_pdf_generator.js`: Primary React PDF renderer.
- `services/pdf_generator.py`: ReportLab fallback renderer.
- `scripts/generate_pdfs_from_json.py`: Batch local JSON-to-PDF utility.

## Docker

```bash
docker-compose up --build
```

Production compose overlay:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Notes

- Generated PDFs and temporary files are ignored by Git.
- `docs/superpowers/` is ignored because it contains local planning artifacts.
- `openresume-source/` is ignored; this wrapper uses the local bridge/generator scripts in this repo.

## Attribution

This project is inspired by and built around concepts from the open-source [OpenResume](https://github.com/xitanggg/open-resume) project by Xitang Zhao.

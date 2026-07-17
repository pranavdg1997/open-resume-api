# Local Setup

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm

## Install Dependencies

```bash
pip install -r requirements.txt
npm install
cp config.example.json config.json
```

## Start The API

```bash
python main.py
```

Open:

```text
http://localhost:5000/docs
```

## Generate A PDF Through The API

```bash
curl -X POST http://localhost:5000/api/v1/generate-resume \
  -H "Content-Type: application/json" \
  -d @path/to/resume.json \
  --output resume.pdf
```

## Generate PDFs Locally

Batch mode:

```bash
python scripts/generate_pdfs_from_json.py \
  --input .resumes \
  --output .output_resumes
```

Renderer-only mode:

```bash
node openresume_pdf_generator.js path/to/resume.json > resume.pdf
```

## Important Files

```text
api/endpoints.py                  API routes
models/resume_models.py           Resume schema
services/openresume_wrapper.py     Primary renderer wrapper
openresume_pdf_generator.js        React PDF renderer
services/pdf_generator.py          ReportLab fallback
scripts/generate_pdfs_from_json.py Batch generation helper
```

## Troubleshooting

- If the API cannot generate a PDF with the primary renderer, check `node --version` and run `npm install`.
- If validation fails, compare your JSON with the schema in `models/resume_models.py`.
- If a PDF is open in a viewer on Windows, writing to the same path can fail. Generate to a fresh filename or close the viewer first.

# Use JSON To Generate Resume PDF

Use this guide when an agent needs to generate a styled resume PDF from JSON in this repository without inspecting or changing renderer code.

## Core Rule

Do not customize code for normal PDF generation. Provide a valid resume JSON file, run the primary Node renderer, and write the returned bytes to a `.pdf` file.

The primary renderer is:

```text
openresume_pdf_generator.js
```

It produces an ATS-friendly A4 PDF with the current project styling.

## Required Input

Create or locate one resume JSON file. The expected top-level shape is:

```json
{
  "personalInfo": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1 555 123 4567",
    "location": "Austin, TX",
    "url": "https://janedoe.dev",
    "github": "https://github.com/janedoe",
    "linkedin": "https://linkedin.com/in/janedoe",
    "summary": "Short professional summary."
  },
  "workExperiences": [
    {
      "company": "Example Corp",
      "jobTitle": "Senior AI Engineer",
      "date": "January 2024 - Present",
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
      "gpa": "",
      "descriptions": []
    }
  ],
  "projects": [],
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
  "certifications": [],
  "custom": {
    "descriptions": []
  },
  "settings": {
    "fontSize": "11"
  }
}
```

Optional fields may be empty strings, empty arrays, or omitted when the generator already defaults them. Keep important contact and resume text in normal JSON text fields, not images or custom markup.

## Direct PDF Generation

From the repository root, run:

```powershell
node openresume_pdf_generator.js "path\to\resume.json" > "output\pdf\resume.pdf"
```

Example:

```powershell
New-Item -ItemType Directory -Force -Path "output\pdf" | Out-Null
node openresume_pdf_generator.js ".resumes\daksh_bi.json" > "output\pdf\daksh_bi.pdf"
```

On macOS/Linux:

```bash
mkdir -p output/pdf
node openresume_pdf_generator.js path/to/resume.json > output/pdf/resume.pdf
```

## Programmatic Generation

Use this when shell redirection is inconvenient:

```powershell
node -e "const fs=require('fs'); const {generateOpenResumePDF}=require('./openresume_pdf_generator'); const input=JSON.parse(fs.readFileSync('path/to/resume.json','utf8')); generateOpenResumePDF(input).then(b=>{fs.mkdirSync('output/pdf',{recursive:true}); fs.writeFileSync('output/pdf/resume.pdf', b); console.log('wrote output/pdf/resume.pdf', b.length);}).catch(e=>{console.error(e); process.exit(1);});"
```

## API Generation

If the FastAPI app is running, POST the same JSON:

```bash
curl -X POST http://localhost:5000/api/v1/generate-resume \
  -H "Content-Type: application/json" \
  -d @path/to/resume.json \
  --output output/pdf/resume.pdf
```

Direct Node generation is preferred for quick agent workflows because it avoids server startup and fallback behavior.

## Quick Verification

Run the project renderer tests:

```powershell
npm.cmd test
```

PowerShell may block `npm`; use `npm.cmd` on Windows.

Confirm basic PDF facts with Poppler when available:

```powershell
& "C:\Users\gujar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe" "output\pdf\resume.pdf"
```

Expected facts for the primary renderer:

- Page size is A4: `595.28 x 841.89 pts`.
- Creator/producer is `react-pdf`.
- PDF is not encrypted.

Render visual previews when layout matters:

```powershell
New-Item -ItemType Directory -Force -Path "temp\resume_pages" | Out-Null
& "C:\Users\gujar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe" -png -r 144 "output\pdf\resume.pdf" "temp\resume_pages\page"
```

Then inspect the generated `temp\resume_pages\page-1.png`, `page-2.png`, and so on.

## Do Not Customize

For routine resume generation, do not edit:

- `openresume_pdf_generator.js`
- `services/openresume_wrapper.py`
- `models/resume_models.py`
- `services/pdf_generator.py`

Only change code if the requested behavior cannot be expressed in JSON or if a verified renderer bug exists.

## Common Issues

`Cannot find module '@react-pdf/renderer'`

Run:

```powershell
npm install
```

`npm.ps1 cannot be loaded because running scripts is disabled`

Use:

```powershell
npm.cmd test
```

PDF output is empty or corrupt

Make sure you are redirecting stdout to a `.pdf` file and not mixing logs into stdout. Prefer the programmatic generation command if needed.

Missing location under jobs

Put `location` on each `workExperiences` item:

```json
{
  "company": "Example Corp",
  "jobTitle": "Senior AI Engineer",
  "date": "2024 - Present",
  "location": "Remote",
  "descriptions": []
}
```

Links do not appear as desired

Use full visible URLs in JSON fields such as `url`, `github`, `linkedin`, and publication `url`. The renderer keeps them as text-based links where supported.

## Minimal Agent Checklist

1. Confirm the input JSON exists.
2. Confirm it has `personalInfo.name` and `personalInfo.email`.
3. Run the direct Node command.
4. Save the PDF under `output/pdf/`.
5. Run `pdfinfo` or open/render the PDF if visual confirmation is needed.
6. Report the final PDF path to the user.

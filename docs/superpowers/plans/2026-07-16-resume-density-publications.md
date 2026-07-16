# Resume Density and Publications Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the primary React PDF resume output smaller and tighter, with compact education spacing and non-overlapping publication rows that support optional hyperlinks.

**Architecture:** Keep the existing API and generation flow intact. Add optional publication URL data support through the Pydantic model and wrapper, then update only `openresume_pdf_generator.js` styles and publication rendering for the primary generator.

**Tech Stack:** Python 3, Pydantic, FastAPI data models, Node.js, React, `@react-pdf/renderer`.

---

## File Structure

- Modify `models/resume_models.py`: add optional `url` to `Publication`.
- Modify `services/openresume_wrapper.py`: pass `Publication.url` into the transformed primary-generator payload.
- Modify `openresume_pdf_generator.js`: preserve direct-input publication URLs, shrink style constants by at least 2 points, add education-specific compact spacing, and render publications with a wrapping title/meta layout.
- No changes to `services/pdf_generator.py`; the ReportLab fallback is out of scope.
- No new permanent test framework files; verification uses Python and Node smoke commands because this repo currently has no pytest dependency.

## Task 1: Preserve Optional Publication URLs Through the Data Flow

**Files:**
- Modify: `models/resume_models.py`
- Modify: `services/openresume_wrapper.py`
- Modify: `openresume_pdf_generator.js`

- [ ] **Step 1: Run the failing publication URL model smoke check**

Run:

```powershell
python -c "from models.resume_models import ResumeData; data={'personalInfo': {'name': 'Link Test', 'email': 'link@example.com'}, 'publications': [{'name': 'Linked Paper', 'date': '2026', 'url': 'https://example.com/paper', 'descriptions': ['Awarded.']}], 'settings': {'fontSize': '11'}}; resume=ResumeData(**data); pub=resume.model_dump()['publications'][0]; assert pub.get('url') == 'https://example.com/paper', pub"
```

Expected: FAIL with an `AssertionError` showing that `url` is missing from the publication model dump.

- [ ] **Step 2: Add `url` to the Pydantic publication model**

In `models/resume_models.py`, replace the `Publication` class with:

```python
class Publication(BaseModel):
    """Publication entry"""
    name: str = Field(..., min_length=1, max_length=200, description="Publication title")
    date: str = Field(..., description="Publication date")
    url: Optional[str] = Field(None, description="Publication URL")
    descriptions: List[str] = Field(default_factory=list, description="Publication details")

    @validator('descriptions')
    def validate_descriptions(cls, v):
        return [desc.strip() for desc in v if desc.strip()]
```

- [ ] **Step 3: Pass publication URLs through the OpenResume wrapper**

In `services/openresume_wrapper.py`, update the publication mapping inside `transform_to_openresume_format` from:

```python
publications.append({
    "name": pub.name,
    "date": pub.date,
    "descriptions": pub.descriptions
})
```

to:

```python
publications.append({
    "name": pub.name,
    "date": pub.date,
    "url": getattr(pub, "url", None) or "",
    "descriptions": pub.descriptions
})
```

- [ ] **Step 4: Preserve publication URLs in direct Node generator input**

In `openresume_pdf_generator.js`, update the `publications` mapping from:

```javascript
publications: (resumeData.publications || []).map(pub => ({
  name: pub.name || '',
  date: pub.date || '',
  descriptions: pub.descriptions || []
})),
```

to:

```javascript
publications: (resumeData.publications || []).map(pub => ({
  name: pub.name || '',
  date: pub.date || '',
  url: pub.url || '',
  descriptions: pub.descriptions || []
})),
```

- [ ] **Step 5: Run the passing publication URL data-flow smoke check**

Run:

```powershell
python -c "from models.resume_models import ResumeData; from services.openresume_wrapper import OpenResumeWrapper; data={'personalInfo': {'name': 'Link Test', 'email': 'link@example.com'}, 'publications': [{'name': 'Linked Paper', 'date': '2026', 'url': 'https://example.com/paper', 'descriptions': ['Awarded.']}], 'settings': {'fontSize': '11'}}; resume=ResumeData(**data); assert resume.publications[0].url == 'https://example.com/paper'; wrapper=OpenResumeWrapper(object()); transformed=wrapper.transform_to_openresume_format(resume); assert transformed['publications'][0]['url'] == 'https://example.com/paper'; print('publication url preserved')"
```

Expected: PASS and prints `publication url preserved`.

- [ ] **Step 6: Commit the URL data-flow change**

Run:

```powershell
git add models/resume_models.py services/openresume_wrapper.py openresume_pdf_generator.js
git commit -m "feat: preserve publication links"
```

Expected: commit succeeds with only the three listed files staged.

## Task 2: Apply Compact Typography and Education Spacing

**Files:**
- Modify: `openresume_pdf_generator.js`

- [ ] **Step 1: Run the failing compact-style source smoke check**

Run:

```powershell
node -e "const fs=require('fs'); const src=fs.readFileSync('openresume_pdf_generator.js','utf8'); if(!src.includes('const requestedFontSize')) throw new Error('missing requestedFontSize compact scale'); if(!src.includes('educationItem')) throw new Error('missing education-specific spacing');"
```

Expected: FAIL with `missing requestedFontSize compact scale`.

- [ ] **Step 2: Add compact font-size constants before `StyleSheet.create`**

In `openresume_pdf_generator.js`, immediately before `const styles = StyleSheet.create({`, add:

```javascript
const requestedFontSize = Number(settings.fontSize) || 11;
const bodyFontSize = Math.max(8, requestedFontSize - 2);
const smallFontSize = Math.max(7.5, bodyFontSize - 0.5);
const nameFontSize = Math.max(18, requestedFontSize + 9);
const sectionFontSize = bodyFontSize + 2;
```

- [ ] **Step 3: Replace the style block with compact values**

In `openresume_pdf_generator.js`, update the existing style definitions inside `StyleSheet.create` so the listed styles match this code:

```javascript
page: {
  fontFamily: 'Helvetica',
  fontSize: bodyFontSize,
  paddingTop: 36,
  paddingBottom: 36,
  paddingLeft: 42,
  paddingRight: 42,
  backgroundColor: '#ffffff',
  lineHeight: 1.2
},
header: {
  borderBottomWidth: 1,
  borderBottomColor: '#1f2937',
  paddingBottom: 8,
  marginBottom: 10,
  alignItems: 'center'
},
name: {
  fontSize: nameFontSize,
  fontWeight: 'bold',
  color: '#1f2937',
  marginBottom: 6,
  letterSpacing: 0,
  textAlign: 'center'
},
contact: {
  fontSize: smallFontSize,
  color: '#4b5563',
  marginBottom: 2,
  textAlign: 'center'
},
contactLine: {
  flexDirection: 'row',
  justifyContent: 'center',
  flexWrap: 'wrap',
  marginBottom: 5,
  alignItems: 'center'
},
summary: {
  fontSize: bodyFontSize,
  lineHeight: 1.2,
  textAlign: 'justify',
  color: '#374151'
},
section: {
  marginBottom: 10
},
sectionTitle: {
  fontSize: sectionFontSize,
  fontWeight: 'bold',
  color: '#1f2937',
  marginBottom: 6,
  letterSpacing: 0,
  borderBottomWidth: 1,
  borderBottomColor: '#e5e7eb',
  paddingBottom: 2
},
experienceItem: {
  marginBottom: 8
},
educationItem: {
  marginBottom: 4
},
experienceHeader: {
  flexDirection: 'row',
  justifyContent: 'space-between',
  marginBottom: 2
},
jobTitle: {
  fontSize: bodyFontSize,
  fontWeight: 'bold',
  color: '#1f2937'
},
company: {
  fontSize: bodyFontSize,
  fontWeight: 'bold',
  color: '#1f2937'
},
date: {
  fontSize: smallFontSize,
  color: '#6b7280'
},
bullet: {
  fontSize: smallFontSize,
  lineHeight: 1.18,
  marginBottom: 2,
  marginLeft: 12,
  color: '#374151'
},
skillsText: {
  fontSize: smallFontSize,
  lineHeight: 1.18,
  marginBottom: 2
}
```

Keep any publication-specific styles added in Task 3 separate from this block.

- [ ] **Step 4: Use compact education spacing in the education section**

In the education section of `openresume_pdf_generator.js`, replace:

```javascript
React.createElement(View, { key: index, style: styles.experienceItem },
```

with:

```javascript
React.createElement(View, { key: index, style: styles.educationItem },
```

Only make this replacement in the education map. Work experience, projects, publications, and certifications should not use `educationItem`.

- [ ] **Step 5: Remove the extra top margin on summary**

In the header summary render, replace:

```javascript
React.createElement(Text, { style: { ...styles.summary, marginTop: 15 } }, openResumeData.profile.summary)
```

with:

```javascript
React.createElement(Text, { style: { ...styles.summary, marginTop: 5 } }, openResumeData.profile.summary)
```

- [ ] **Step 6: Run the passing compact-style source smoke check**

Run:

```powershell
node -e "const fs=require('fs'); const src=fs.readFileSync('openresume_pdf_generator.js','utf8'); if(!src.includes('const requestedFontSize')) throw new Error('missing requestedFontSize compact scale'); if(!src.includes('const bodyFontSize = Math.max(8, requestedFontSize - 2);')) throw new Error('body font is not reduced by 2 points'); if(!src.includes('educationItem')) throw new Error('missing education-specific spacing'); console.log('compact style source check passed');"
```

Expected: PASS and prints `compact style source check passed`.

- [ ] **Step 7: Generate the Natera sample PDF for visual review**

Run:

```powershell
node -e "const fs=require('fs'); const {generateOpenResumePDF}=require('./openresume_pdf_generator'); const input=JSON.parse(fs.readFileSync('C:/more ML/application_assistant/application_assistant/output/pdf/Pranav_Gujarathi_Resume_Natera_OpenResume.json','utf8')); generateOpenResumePDF(input).then(b=>{fs.writeFileSync('temp/natera-compact.pdf', b); console.log('wrote temp/natera-compact.pdf', b.length);}).catch(e=>{console.error(e); process.exit(1);});"
```

Expected: PASS and writes `temp/natera-compact.pdf`.

- [ ] **Step 8: Observe the generated page count**

Run:

```powershell
python -c "import re; data=open('temp/natera-compact.pdf','rb').read(); print('observed_pages', len(re.findall(rb'/Type\\s*/Page\\b', data)))"
```

Expected: prints `observed_pages` with the current page count. This value is informational and is not a hard failure gate.

- [ ] **Step 9: Commit the compact style change**

Run:

```powershell
git add openresume_pdf_generator.js
git commit -m "style: compact primary resume pdf layout"
```

Expected: commit succeeds with `openresume_pdf_generator.js` staged.

## Task 3: Render Publications Without Overlap and Support Clickable Titles

**Files:**
- Modify: `openresume_pdf_generator.js`

- [ ] **Step 1: Run the failing publication-rendering source smoke check**

Run:

```powershell
node -e "const fs=require('fs'); const src=fs.readFileSync('openresume_pdf_generator.js','utf8'); if(!src.includes('publicationItem')) throw new Error('missing publication-specific item style'); if(!src.includes('pub.url ?')) throw new Error('missing conditional publication link rendering');"
```

Expected: FAIL with `missing publication-specific item style`.

- [ ] **Step 2: Add publication-specific compact styles**

In `openresume_pdf_generator.js`, add these styles inside `StyleSheet.create`, after `skillsText`:

```javascript
publicationItem: {
  marginBottom: 6
},
publicationTitle: {
  fontSize: bodyFontSize,
  fontWeight: 'bold',
  color: '#1f2937',
  lineHeight: 1.18,
  marginBottom: 1
},
publicationMeta: {
  fontSize: smallFontSize,
  color: '#6b7280',
  lineHeight: 1.15,
  marginBottom: 2
}
```

Ensure the preceding `skillsText` style has a trailing comma before `publicationItem`.

- [ ] **Step 3: Replace the publications section render**

In `openresume_pdf_generator.js`, replace the current publications section block with:

```javascript
// Publications Section
openResumeData.publications && openResumeData.publications.length > 0 &&
  React.createElement(View, { style: styles.section },
    React.createElement(Text, { style: styles.sectionTitle }, 'PUBLICATIONS'),
    ...openResumeData.publications.map((pub, index) =>
      React.createElement(View, { key: index, style: styles.publicationItem },
        pub.url ?
          React.createElement(Link, {
            style: { ...styles.publicationTitle, color: '#2563eb', textDecoration: 'underline' },
            src: pub.url
          }, pub.name) :
          React.createElement(Text, { style: styles.publicationTitle }, pub.name),
        pub.date && React.createElement(Text, { style: styles.publicationMeta }, pub.date),
        ...pub.descriptions.map((desc, descIndex) =>
          React.createElement(Text, { key: descIndex, style: styles.bullet }, `• ${desc}`)
        )
      )
    )
  ),
```

This intentionally removes the horizontal title/date row for publications so long titles wrap before metadata and cannot overlap.

- [ ] **Step 4: Run the passing publication-rendering source smoke check**

Run:

```powershell
node -e "const fs=require('fs'); const src=fs.readFileSync('openresume_pdf_generator.js','utf8'); if(!src.includes('publicationItem')) throw new Error('missing publication-specific item style'); if(!src.includes('pub.url ?')) throw new Error('missing conditional publication link rendering'); if(src.includes('React.createElement(Text, { style: styles.jobTitle }, pub.name)')) throw new Error('old publication row rendering still present'); console.log('publication render source check passed');"
```

Expected: PASS and prints `publication render source check passed`.

- [ ] **Step 5: Generate a publication-link smoke PDF and confirm link target is embedded**

Run:

```powershell
node -e "const fs=require('fs'); const {generateOpenResumePDF}=require('./openresume_pdf_generator'); const resume={personalInfo:{name:'Publication Link Test',email:'link@example.com',summary:'Short summary.'}, publications:[{name:'A Very Long Publication Title That Needs To Wrap Without Overlapping The Venue Or Date Metadata', date:'ACM COMPASS 2026', url:'https://example.com/paper', descriptions:['Best paper finalist.']}], settings:{fontSize:'11'}}; generateOpenResumePDF(resume).then(b=>{fs.writeFileSync('temp/publication-link-smoke.pdf', b); if(!b.includes(Buffer.from('https://example.com/paper'))) throw new Error('link target missing from PDF bytes'); console.log('publication link smoke passed', b.length);}).catch(e=>{console.error(e); process.exit(1);});"
```

Expected: PASS, writes `temp/publication-link-smoke.pdf`, and prints `publication link smoke passed`.

- [ ] **Step 6: Regenerate the Natera sample PDF for final visual review**

Run:

```powershell
node -e "const fs=require('fs'); const {generateOpenResumePDF}=require('./openresume_pdf_generator'); const input=JSON.parse(fs.readFileSync('C:/more ML/application_assistant/application_assistant/output/pdf/Pranav_Gujarathi_Resume_Natera_OpenResume.json','utf8')); generateOpenResumePDF(input).then(b=>{fs.writeFileSync('temp/natera-compact-publications.pdf', b); console.log('wrote temp/natera-compact-publications.pdf', b.length);}).catch(e=>{console.error(e); process.exit(1);});"
```

Expected: PASS and writes `temp/natera-compact-publications.pdf`.

- [ ] **Step 7: Observe the final generated page count**

Run:

```powershell
python -c "import re; data=open('temp/natera-compact-publications.pdf','rb').read(); print('observed_pages', len(re.findall(rb'/Type\\s*/Page\\b', data)))"
```

Expected: prints `observed_pages` with the current page count. This value is informational and is not a hard failure gate.

- [ ] **Step 8: Commit the publication rendering change**

Run:

```powershell
git add openresume_pdf_generator.js
git commit -m "fix: prevent publication overlap in pdf"
```

Expected: commit succeeds with `openresume_pdf_generator.js` staged.

## Final Verification

- [ ] **Step 1: Confirm branch and working tree state**

Run:

```powershell
git status --short --branch
```

Expected: branch is `codex/resume-density-fit`. Existing unrelated dirty files from before this work may still appear, but implementation files touched by these tasks should either be committed or intentionally left unstaged for review.

- [ ] **Step 2: Generate the final Natera artifact for user inspection**

Run:

```powershell
node -e "const fs=require('fs'); const {generateOpenResumePDF}=require('./openresume_pdf_generator'); const input=JSON.parse(fs.readFileSync('C:/more ML/application_assistant/application_assistant/output/pdf/Pranav_Gujarathi_Resume_Natera_OpenResume.json','utf8')); generateOpenResumePDF(input).then(b=>{fs.writeFileSync('temp/Pranav_Gujarathi_Resume_Natera_compact.pdf', b); console.log('wrote temp/Pranav_Gujarathi_Resume_Natera_compact.pdf', b.length);}).catch(e=>{console.error(e); process.exit(1);});"
```

Expected: PASS and writes `temp/Pranav_Gujarathi_Resume_Natera_compact.pdf`.

- [ ] **Step 3: Report visual review points**

Open or render `temp/Pranav_Gujarathi_Resume_Natera_compact.pdf` and verify:

- Overall text is at least 2 points smaller than the old output.
- Education entries have compact vertical spacing.
- Skills remain structurally the same and are smaller overall.
- Publications do not overlap.
- Publication links work in the smoke PDF created at `temp/publication-link-smoke.pdf`.

# Resume Density and Publications Design

## Goal

Make the primary OpenResume/React PDF output more compact and readable for long resumes by reducing typography by at least 2 points, tightening education spacing, and fixing publication overlap while adding optional publication hyperlinks.

## Scope

This change applies only to the primary generator in `openresume_pdf_generator.js` and the data path needed to support publication links. The ReportLab fallback in `services/pdf_generator.py` is intentionally out of scope.

The sample resume for manual validation is:

`C:\more ML\application_assistant\application_assistant\output\pdf\Pranav_Gujarathi_Resume_Natera_OpenResume.json`

## Current Behavior

The current React PDF style preset is roomy:

- Page padding is 50 points top/bottom and 60 points left/right.
- The page uses `lineHeight: 1.6`.
- Sections use 25 points of bottom margin.
- Experience-like entries use 18 points of bottom margin.
- Education entries reuse the same large spacing as work experience entries.
- Publication rows use the same horizontal header layout as shorter work entries, so long publication titles can collide with the date or venue on the right.
- The publication model does not expose an optional URL field, so publication titles cannot be linked.

The Natera sample currently renders as a 3-page PDF in the primary generator.

## Requirements

- Reduce body-level font sizes by at least 2 points from the current 11-point default. With the sample's `settings.fontSize: "11"`, normal content should render at about 9 points.
- Reduce heading, name, contact, bullet, skills, date, and summary sizes proportionally while keeping them readable.
- Tighten global line heights and vertical margins.
- Keep the resume ATS-friendly: preserve single-column reading order, normal text elements, ordinary section headings, and text-based links.
- Do not guarantee a 2-page result in code. The implementation should make the basic density changes, then the generated PDF will be reviewed visually.
- Keep skills structurally as they are, only smaller and tighter with the rest of the document.
- Make education entries visibly more compact than work experience entries.
- Fix publication overlap by using a publication-specific layout that wraps long titles safely.
- Add optional publication hyperlink support without requiring existing JSON files to change.

## Design

### Primary Layout Density

Define a compact style scale in `openresume_pdf_generator.js` instead of continuing to hardcode the current roomy values throughout the `StyleSheet.create` call.

The compact preset should use values close to:

- Page padding: 36 points top/bottom, 42 points left/right.
- Base body font: 9 points when the input setting is 11.
- Name: about 20-21 points instead of 24.
- Section title: about 11 points instead of 13.
- Contact, summary, job/company, date, bullet, and skills text: about 8-9 points depending on role.
- Page line height: about 1.2 instead of 1.6.
- Summary/bullet/skills line height: about 1.15-1.25.
- Section margin bottom: about 10-12 points instead of 25.
- Experience item margin bottom: about 8-10 points instead of 18.

The implementation may keep this as constants near the style definition or a small helper that derives sizes from `settings.fontSize`. It should remain simple and predictable.

### Education Spacing

Education should no longer use the same large `experienceItem` spacing as work experience. Add or reuse a specific `educationItem` style with a smaller bottom margin, about 4-6 points. The education header should also use tighter bottom spacing because most education entries have no descriptions.

This keeps the three-degree block compact without changing the resume content.

### Skills

Skills keep the current rendering structure:

- Category label in bold.
- Comma-separated skills after the label.
- One text block per skill category.

Only font size, line height, and margin should shrink with the compact style preset.

### Publications

Publications should use a dedicated layout instead of the current experience-style row.

For each publication:

- Render the title as the primary text line.
- If `pub.url` exists, render the title with React PDF's `Link`; otherwise render plain text.
- Render date or venue metadata as a secondary line or compact trailing text that cannot collide with a long title.
- Render descriptions below the title/meta block using the compact bullet style.
- Use a small publication item margin, about 5-8 points.

This avoids overlap for long titles such as `Using Causality to Mine Sjogren's Syndrome related Factors from Medical Literature`.

### Publication URL Data Flow

Add an optional `url` field to the `Publication` Pydantic model in `models/resume_models.py`.

Pass that field through `services/openresume_wrapper.py` when transforming `ResumeData` to the generator's JSON shape.

Also update `openresume_pdf_generator.js` so direct generator usage preserves `pub.url` from input JSON.

Existing JSON without `url` remains valid and renders exactly as plain text.

## Verification

Use the Natera sample as the main acceptance artifact:

1. Generate a PDF from `C:\more ML\application_assistant\application_assistant\output\pdf\Pranav_Gujarathi_Resume_Natera_OpenResume.json`.
2. Confirm the output uses smaller typography overall.
3. Confirm education entries are more compact.
4. Confirm skills are smaller, with no structural redesign.
5. Confirm publication titles and metadata do not overlap.
6. Confirm publication URLs render as clickable links when a test input includes `url`.
7. Observe the page count, but do not fail implementation solely because the resume is still more than 2 pages.

## Non-Goals

- Do not modify ReportLab fallback layout.
- Do not edit or trim resume content.
- Do not introduce multi-column layout.
- Do not add an adaptive shrink-to-fit loop.
- Do not redesign skills beyond compact typography.

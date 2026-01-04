# Resume Generator

## Project Overview

A Python-based resume and cover letter generator that converts Markdown source files to HTML and PDF formats. Designed to run in Docker to avoid local dependency installation.

## Quick Start

```bash
docker compose up --build
```

This generates `Resume.pdf`, `Resume.html`, `CoverLetter.pdf`, and `CoverLetter.html` in the current directory.

---

## Project Structure

```
├── Resume.md              # Main resume content (Markdown)
├── CoverLetter.md         # Cover letter template with placeholders
├── CoverLetter.json       # Template variables for cover letter (gitignored)
├── CoverLetter.json.example  # Example template variables
├── resume.py              # Main Python script for rendering
├── style.css              # Styling for HTML/PDF output
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies (Markdown, pdfkit)
└── render.sh              # Alternative shell script for building
```

---

## How It Works

1. **Markdown Parsing**: `resume.py` reads `Resume.md` and `CoverLetter.md`
2. **Template Substitution**: Cover letter placeholders (`{company}`, `{position}`, etc.) are replaced with values from `CoverLetter.json`
3. **HTML Rendering**: Markdown is converted to HTML with `style.css` applied
4. **PDF Generation**: `wkhtmltopdf` converts the styled HTML to PDF

---

## Cover Letter Templating

The cover letter uses Python string formatting with a JSON template:

**CoverLetter.json:**
```json
{
    "company": "ACME Corp.",
    "position": "Senior DevOps Engineer",
    "interest_reason": "your innovative approach to technology",
    "related_experience": "cloud architecture and DevOps practices"
}
```

**Usage in CoverLetter.md:**
```markdown
Dear Hiring Manager at **{company}**,

I am writing to express my interest in the {position} role...
```

---

## Docker Configuration

### Docker Compose (Recommended)

The `docker-compose.yml` mounts the current directory as a volume, so generated files appear locally immediately:

```yaml
services:
  resume:
    build: .
    platform: linux/arm64  # Change to linux/amd64 for x86 systems
    volumes:
      - .:/app
```

### Platform Notes

- **Apple Silicon (M1/M2/M3)**: Use `linux/arm64` (default)
- **Intel/AMD x86_64**: Change platform to `linux/amd64`

---

## Editing Guidelines

### Resume.md

- Write content in standard Markdown
- Use `##` for major sections (Contact, Certifications, Experience, Skills)
- Use `###` for job titles with format: `Company - Title - Years`
- Use bullet points (`-`) for accomplishments
- HTML comments (`<!-- -->`) can hide content from output

### CoverLetter.md

- Placeholders use Python format string syntax: `{variable_name}`
- All placeholders must have corresponding keys in `CoverLetter.json`
- Copy `CoverLetter.json.example` to `CoverLetter.json` before building

### style.css

- Controls PDF and HTML appearance
- Changes apply to both resume and cover letter output

---

## Dependencies

- **Python 3**: Runtime environment
- **Markdown**: Python library for Markdown → HTML conversion
- **pdfkit**: Python wrapper for wkhtmltopdf
- **wkhtmltopdf**: Renders HTML to PDF (installed in Docker image)

---

## Output Files

| Source | HTML Output | PDF Output |
|--------|-------------|------------|
| Resume.md | Resume.html | Resume.pdf |
| CoverLetter.md | CoverLetter.html | CoverLetter.pdf |

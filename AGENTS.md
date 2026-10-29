# Resume Generator

## Project Overview

A Python-based resume and cover letter generator that converts Markdown source files to HTML and PDF formats. Includes automated ATS (Applicant Tracking System) scanning to ensure your resume is optimized for automated screening systems. Designed to run in Docker to avoid local dependency installation.

## Quick Start

```bash
docker compose up --build
```

This generates:
- `Resume.pdf` and `Resume.html`
- `CoverLetter.pdf` and `CoverLetter.html`
- `Resume_ats_report.txt` - ATS compatibility analysis

---

## ATS Scanning Feature

### Design Philosophy

**IMPORTANT FOR AI AGENTS**: The ATS scanning system is designed for **feedback and analysis**, NOT for automatically fixing the resume. The purpose is to provide insight into what different ATS systems and recruiters see when the resume is submitted.

**Key Design Principles:**
1. **Multiple ATS Implementations**: Support multiple ATS scanning engines to compare how different systems parse the resume
2. **Feedback-Oriented**: Generate detailed reports showing what each ATS system extracts
3. **Comparative Analysis**: Allow comparison between different ATS approaches (NLP-based, regex-based, ML-based)
4. **No Auto-Fix**: Do NOT implement automatic resume modifications - only provide recommendations
5. **Recruiter Perspective**: Help understand what recruiters see when they review ATS-parsed resumes

The goal is to answer: "What do recruiters see when I submit my resume to their ATS?"

### Current Implementation

The project includes automated ATS (Applicant Tracking System) compatibility scanning using open-source NLP tools. After generating your resume PDF, the system automatically analyzes it for:

- **Text extraction quality** - Ensures ATS systems can read your content
- **Contact information detection** - Verifies email, phone, LinkedIn, GitHub are parseable
- **Skills extraction** - Identifies technical skills and competencies (both explicit and NLP-detected)
- **Job title recognition** - Confirms experience section is properly formatted
- **Education parsing** - Validates degree information is detectable
- **Formatting issues** - Detects special characters, tables, or layouts that may confuse ATS
- **Overall compatibility score** - 0-100 score with specific recommendations

### Future ATS Implementations

To add more ATS scanning engines for comparative analysis:
1. Create new scanner classes in `ats_scanner.py` implementing the same interface
2. Each scanner should produce a standardized report format
3. Compare results across multiple scanners to see parsing differences
4. Examples: rule-based parser, ML-based extraction, commercial ATS simulation

### ATS Scanning Usage

**Default behavior** (automatic scan after generation):
```bash
docker compose up --build
```

**Scan only without regenerating PDFs**:
```bash
docker compose run resume python3 resume.py --ats-only
```

**Skip ATS scanning**:
```bash
docker compose run resume python3 resume.py --skip-ats
```

**Standalone ATS scanner**:
```bash
docker compose run resume python3 ats_scanner.py Resume.pdf
```

### Understanding Your ATS Report

The ATS report (`Resume_ats_report.txt`) includes:

1. **Scanner Type** - Identifies which ATS implementation was used (e.g., "NLP-Based (skillNer + spaCy)")

2. **ATS Compatibility Score** (0-100):
   - 80-100: Excellent - Highly ATS-compatible
   - 60-79: Good - Minor improvements recommended
   - 40-59: Fair - Some issues to address
   - 0-39: Needs improvement - Significant compatibility issues

3. **Contact Information** - Validates all contact details are parseable

4. **Skills Extracted** - Lists technical skills the ATS identified
   - Explicit skills from Skills section
   - NLP-detected skills from text

5. **Job Titles & Experience** - Shows detected job titles and roles

6. **Education** - Shows what this scanner can detect:
   - **NLP-Based Scanner**: Can detect universities (ORG entities) and dates, but CANNOT extract degree names
   - Reports honestly about its limitations
   - Different ATS implementations will have different capabilities

7. **Recommendations** - Specific suggestions based on what this scanner can detect

### Scanner Fidelity

**IMPORTANT**: Each scanner implementation only reports what it can **actually** detect using its underlying technology. This ensures you see what real ATS systems with similar approaches would extract.

**Current NLP-Based Scanner** (skillNer + spaCy) can detect:
- ✓ Contact information (regex patterns)
- ✓ Explicit skills from Skills section (regex parsing)
- ✓ Additional skills via NLP (skillNer)
- ✓ Job titles (regex patterns)
- ✓ Universities (spaCy ORG entity recognition)
- ✓ Dates (spaCy DATE entity recognition)

**Current NLP-Based Scanner CANNOT detect**:
- ✗ Degree names (Bachelor, Master, Ph.D.) - spaCy has no education entity types
- ✗ Fields of study - requires specialized parser
- ✗ GPA or honors - requires specialized parser

Future scanner implementations (rule-based, ML-based, commercial ATS simulators) will have different capabilities and limitations, allowing you to compare what different systems see.

### Performance Considerations

The ATS scanning process typically takes 60-90 seconds due to:

1. **skillNer initialization** (~50-70 seconds): Loads the SKILL_DB database and NLP models on first use
2. **spaCy text processing** (~10-15 seconds): Analyzes resume text for linguistic patterns
3. **Pattern matching** (~5-10 seconds): Extracts contact info, experience, education

**Optimization tips:**
- The skillNer library is optional; if removed, scanning completes in ~15 seconds but with reduced skill detection
- First-time Docker builds take longer due to downloading spaCy models (~500MB)
- Subsequent runs reuse cached models and dependencies
- The `--skip-ats` flag can be used if you only need PDF generation

**Resource requirements:**
- Memory: ~1-2GB during skillNer processing
- CPU: Single-threaded, benefits from faster processors
- Disk: ~1GB for spaCy models and dependencies

---

## Git Workflow

**IMPORTANT FOR AI AGENTS**: Never commit directly to `main`. All changes must be reviewed before they land on `main`.

When asked to commit or push changes:
1. Create a feature branch from `main` (e.g., `git checkout -b <short-description>`)
2. Commit the changes on that branch
3. Push the branch to `origin`
4. Open a Pull Request against `main` (e.g., `gh pr create --base main`)
5. Report the PR URL; do not merge it

Do not force-push to `main` or rewrite its history.

---

## Project Structure

```
├── Resume.md              # Main resume content (Markdown)
├── CoverLetter.md         # Cover letter template with placeholders
├── CoverLetter.json       # Template variables for cover letter (gitignored)
├── CoverLetter.json.example  # Example template variables
├── resume.py              # Main Python script for rendering and ATS scanning
├── ats_scanner.py         # ATS compatibility analyzer module
├── style.css              # Styling for HTML/PDF output
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── render.sh              # Alternative shell script for building
```

---

## How It Works

1. **Markdown Parsing**: `resume.py` reads `Resume.md` and `CoverLetter.md`
2. **Template Substitution**: Cover letter placeholders (`{company}`, `{position}`, etc.) are replaced with values from `CoverLetter.json`
3. **HTML Rendering**: Markdown is converted to HTML with `style.css` applied
4. **PDF Generation**: `wkhtmltopdf` converts the styled HTML to PDF
5. **ATS Scanning**: The resume PDF is analyzed for ATS compatibility using NLP and pattern recognition
6. **Report Generation**: Detailed ATS compatibility report is generated with recommendations

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
- **PyPDF2**: PDF text extraction for ATS scanning
- **spaCy**: NLP library for text analysis and entity recognition
- **skillNer**: Skill extraction from text using NLP
- **python-dateutil**: Date parsing utilities

---

## Output Files

| Source | HTML Output | PDF Output | ATS Report |
|--------|-------------|------------|------------|
| Resume.md | Resume.html | Resume.pdf | Resume_ats_report.txt |
| CoverLetter.md | CoverLetter.html | CoverLetter.pdf | - |

---

## Tips for ATS Optimization

Based on the ATS scanner's analysis, here are general tips:

1. **Use standard section headers**: "Experience", "Education", "Skills", "Certifications"
2. **Avoid special characters**: Use standard bullets (-, *, •) instead of fancy symbols
3. **Include contact info prominently**: Email, phone, LinkedIn, GitHub
4. **Use standard fonts**: Stick to common fonts like Arial, Calibri, Times New Roman
5. **Avoid tables and columns**: Use simple linear formatting
6. **Spell out acronyms**: First time mentioning (e.g., "Application Programming Interface (API)")
7. **Use standard job titles**: Include industry-recognized job titles
8. **Include keywords**: Use relevant technical terms and skills from job descriptions
9. **Avoid headers/footers**: Don't repeat information on each page
10. **Use standard date formats**: MM/YYYY or Month YYYY

The ATS scanner will analyze all these factors and provide specific feedback for your resume.

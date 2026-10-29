#!/usr/bin/env python3
'''
ATS Scanner - Analyzes resume PDFs for ATS compatibility

DESIGN PHILOSOPHY:
This tool is designed for FEEDBACK and ANALYSIS, not for automatically fixing resumes.
The purpose is to show what different ATS systems see when parsing your resume.

Goals:
- Provide insight into how recruiters/ATS systems parse your resume
- Support multiple ATS scanning implementations for comparative analysis
- Generate detailed reports showing what each ATS extracts
- NO automatic modifications - only provide recommendations

To add new ATS implementations:
1. Create a new scanner class with scan() method returning standardized Dict
2. Add it to the AVAILABLE_SCANNERS list
3. Each scanner should extract: contact info, skills, experience, education
4. Generate comparative reports to see parsing differences across ATS systems
'''
import logging
import re
import sys
from typing import Dict, List, Tuple
from collections import Counter

# pylint: disable=import-error
from pypdf import PdfReader # pyright: ignore[reportMissingImports]
import spacy # pyright: ignore[reportMissingImports]
from spacy.matcher import PhraseMatcher # pyright: ignore[reportMissingImports]

from skillNer.general_params import SKILL_DB # pyright: ignore[reportMissingImports]
from skillNer.skill_extractor_class import SkillExtractor # pyright: ignore[reportMissingImports]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Module-level NLP models (initialized on first use)
NLP_MODEL = None
SKILL_EXTRACTOR = None


def _init_models() -> Tuple:
    '''
    Initialize NLP models (lazy loading)
    '''
    global NLP_MODEL, SKILL_EXTRACTOR  # pylint: disable=global-statement

    if NLP_MODEL is None:
        # Load the small model (en_core_web_lg can be used for higher accuracy if installed)
        NLP_MODEL = spacy.load("en_core_web_sm")
        SKILL_EXTRACTOR = SkillExtractor(NLP_MODEL, SKILL_DB, PhraseMatcher)

    return NLP_MODEL, SKILL_EXTRACTOR


def extract_text_from_pdf(pdf_path: str) -> str:
    '''
    Extract text content from PDF
    '''
    logging.info("Extracting text from %s", pdf_path)
    text = ""

    with open(pdf_path, 'rb', encoding=None) as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text


def analyze_formatting(text: str) -> Dict:
    '''
    Analyze resume formatting for ATS compatibility
    '''
    issues = []
    warnings = []

    # Check for special characters that might confuse ATS
    special_chars = re.findall(r'[★☆•●○◆◇▪▫■□►▶◄◀]', text)
    if special_chars:
        issues.append(
            f"Found {len(special_chars)} special characters "
            "that may not parse correctly"
        )

    # Check for tables/columns (multiple spaces in a row)
    if re.search(r' {5,}', text):
        warnings.append(
            "Possible table/column formatting detected - "
            "may not parse correctly"
        )

    # Check for headers/footers repeated on pages
    lines = text.split('\n')
    line_counts = Counter(lines)
    repeated_lines = [
        line for line, count in line_counts.items()
        if count > 2 and len(line) > 10
    ]
    if repeated_lines:
        warnings.append(
            f"Found {len(repeated_lines)} repeated lines "
            "(possible headers/footers)"
        )

    return {
        'issues': issues,
        'warnings': warnings
    }


def extract_contact_info(text: str) -> Dict:
    '''
    Extract contact information
    '''
    contact = {}

    # Email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    contact['emails'] = emails

    # Phone numbers
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    contact['phones'] = [''.join(p) if isinstance(p, tuple) else p for p in phones]

    # LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
    contact['linkedin'] = linkedin

    # GitHub
    github_pattern = r'github\.com/[\w-]+'
    github = re.findall(github_pattern, text, re.IGNORECASE)
    contact['github'] = github

    return contact


def extract_explicit_skills(text: str) -> List[str]:
    '''
    Extract skills explicitly listed in Skills section
    '''
    explicit_skills = []

    # Find Skills section (case insensitive)
    skills_section_pattern = r'Skills.*?(?=Professional\s+Experience|Education|Certifications|\Z)'
    skills_match = re.search(skills_section_pattern, text, re.IGNORECASE | re.DOTALL)

    if skills_match:
        skills_text = skills_match.group()

        # Pattern 1: Markdown format **Category**: skill1, skill2
        skill_line_pattern = r'\*\*([^:]+)\*\*:\s*([^\n<]+)'
        for match in re.finditer(skill_line_pattern, skills_text):
            skills_content = match.group(2)
            individual_skills = [s.strip() for s in skills_content.split(',')]
            explicit_skills.extend(individual_skills)

        # Pattern 2: PDF format - Category followed by colon on next line, then skills
        # Handles: "Core DevOps Skills\n: Kubernetes, Helm, Ansible"
        pdf_pattern = r'([A-Z][A-Za-z\s&]+)\s*:\s*([^\n]+(?:\n(?!\s*[A-Z][A-Za-z\s&]+\s*:)[^\n]+)*)'
        for match in re.finditer(pdf_pattern, skills_text):
            category = match.group(1).strip()
            # Skip headers like "Technical Skills:" or "Soft Skills:"
            if category.lower() not in ['technical skills', 'soft skills', 'skills']:
                skills_content = match.group(2).strip()
                # Split by commas and clean up whitespace
                individual_skills = [
                    re.sub(r'\s+', ' ', s.strip())
                    for s in skills_content.split(',')
                    if s.strip()
                ]
                explicit_skills.extend(individual_skills)

    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in explicit_skills:
        if skill and skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)

    return unique_skills


def extract_skills(text: str) -> Dict:
    '''
    Extract technical skills and competencies
    '''
    nlp, skill_extractor = _init_models()
    skills = []
    skill_keywords = []

    # First, get explicitly listed skills from Skills section
    explicit_skills = extract_explicit_skills(text)

    # Use SkillNer for skill extraction if available
    annotations = skill_extractor.annotate(text)

    for result in annotations.get('results', {}).get('full_matches', []):
        skills.append({
            'skill': result['doc_node_value'],
            'type': result['skill_id']
        })

    # Also extract using simple NLP for additional skills
    processed_text = nlp(text)

    for chunk in processed_text.noun_chunks:
        # Keep it to reasonable skill names
        if len(chunk.text.split()) <= 3:
            skill_keywords.append(chunk.text)

    return {
        'explicit_skills': explicit_skills,
        'extracted_skills': skills,
        'skill_phrases': list(set(skill_keywords))[:50]
    }


def extract_experience(text: str) -> List[str]:
    '''
    Extract work experience and job titles
    '''
    # Look for common job title patterns
    job_titles = []
    title_patterns = [
        r'\b(?:Senior|Junior|Lead|Principal|Staff|Chief)\s+\w+\s+'
        r'(?:Engineer|Developer|Manager|Analyst|Architect|Designer)\b',
        r'\b(?:Software|DevOps|Data|Product|Project|Engineering|'
        r'Development)\s+(?:Engineer|Manager|Lead|Director)\b',
        r'\b(?:VP|Director|Manager|Coordinator|Specialist|'
        r'Consultant)\s+of\s+\w+\b'
    ]

    for pattern in title_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        job_titles.extend(matches)

    return list(set(job_titles))


def extract_education(text: str) -> Dict[str, List[str]]:
    '''
    Extract education information using NLP entity recognition.

    NOTE: spaCy does NOT have dedicated entity types for degrees/education.
    This function only extracts what spaCy can reliably identify:
    - Universities/Institutions (ORG entities)
    - Graduation dates (DATE entities)

    Degree names (Bachelor, Master, Ph.D.) are NOT reliably extracted by spaCy.
    Commercial ATS systems use specialized education parsers with degree databases.
    '''
    nlp, _ = _init_models()
    processed_text = nlp(text)

    universities = []
    dates = []

    # Extract organization and date entities from text
    for ent in processed_text.ents:
        if ent.label_ == 'ORG':
            # Filter to likely educational institutions
            org_text = ent.text.lower()
            if any(keyword in org_text for keyword in
                   ['university', 'college', 'institute', 'school', 'academy']):
                universities.append(ent.text)
        elif ent.label_ == 'DATE':
            # Look for dates near education-related text
            dates.append(ent.text)

    return {
        'universities': list(set(universities)),
        'dates': list(set(dates)),
        'degrees': []  # spaCy cannot reliably extract degree names
    }


def calculate_ats_score(analysis: Dict) -> Tuple[int, List[str]]:
    '''
    Calculate an ATS compatibility score (0-100)
    '''
    score = 100
    recommendations = []

    # Deduct points for issues
    formatting = analysis.get('formatting', {})
    issues = formatting.get('issues', [])
    warnings = formatting.get('warnings', [])

    score -= len(issues) * 10
    score -= len(warnings) * 5

    if issues:
        recommendations.extend(issues)
    if warnings:
        recommendations.extend(warnings)

    # Check for essential sections
    contact = analysis.get('contact', {})
    if not contact.get('emails'):
        score -= 15
        recommendations.append("Add email address for better ATS parsing")
    if not contact.get('phones'):
        score -= 10
        recommendations.append("Add phone number for better ATS parsing")

    skills = analysis.get('skills', {})
    # Check both explicit and NLP-detected skills
    explicit_skills = skills.get('explicit_skills', [])
    extracted_skills = skills.get('extracted_skills', [])

    if len(explicit_skills) < 5:
        score -= 10
        recommendations.append("Add more explicit technical skills in Skills section")
    if len(extracted_skills) < 5:
        score -= 5
        recommendations.append(
            "Include more skills in experience descriptions for better ATS detection"
        )

    # NOTE: Do not penalize for education detection - the NLP-based scanner
    # cannot reliably extract degree information. Commercial ATS systems
    # use specialized education parsers that we don't have.
    education = analysis.get('education', {})

    experience = analysis.get('experience', [])
    if not experience:
        score -= 5
        recommendations.append("Ensure job titles are clearly formatted")

    # Ensure score is within bounds
    score = max(0, min(100, score))

    return score, recommendations


# =============================================================================
# ATS SCANNER IMPLEMENTATION: NLP-Based (skillNer + spaCy)
# =============================================================================
# This is the primary ATS scanner implementation using NLP and pattern matching.
# Future implementations could include:
# - Rule-based parser (regex-only, no NLP)
# - ML-based extraction (trained models for resume parsing)
# - Commercial ATS simulation (mimicking Taleo, Workday, Greenhouse, etc.)
# =============================================================================

def scan(pdf_path: str) -> Dict:
    '''
    Perform comprehensive ATS scan of resume using NLP-based analysis

    This scanner uses:
    - skillNer for skill extraction
    - spaCy for NLP processing
    - Regex patterns for contact info and experience

    SCANNER CAPABILITIES:
    This NLP-based scanner can extract:
    ✓ Contact information (via regex patterns)
    ✓ Skills (via explicit Skills section parsing + NLP detection)
    ✓ Job titles (via regex patterns)
    ✓ Universities (via ORG entity recognition)
    ✓ Dates (via DATE entity recognition)

    This scanner CANNOT extract:
    ✗ Degree names (Bachelor, Master, Ph.D.) - spaCy has no education entity types
    ✗ Fields of study - requires specialized education parser
    ✗ GPA or honors - requires specialized parser

    Returns:
        Dict containing analysis results including score, extracted data, and recommendations
    '''
    logging.info("Starting ATS scan of %s", pdf_path)

    # Extract text
    text = extract_text_from_pdf(pdf_path)

    if not text:
        return {
            'error': 'Could not extract text from PDF',
            'score': 0
        }

    # Perform analysis
    analysis = {
        'scanner_type': 'NLP-Based (skillNer + spaCy)',
        'text_length': len(text),
        'word_count': len(text.split()),
        'formatting': analyze_formatting(text),
        'contact': extract_contact_info(text),
        'skills': extract_skills(text),
        'experience': extract_experience(text),
        'education': extract_education(text)
    }

    # Calculate score
    score, recommendations = calculate_ats_score(analysis)
    analysis['ats_score'] = score
    analysis['recommendations'] = recommendations

    return analysis


def _write_report_header(file_handle, score: int, scanner_type: str = "Unknown"):
    '''
    Write report header with score and scanner information
    '''
    file_handle.write("=" * 70 + "\n")
    file_handle.write("ATS COMPATIBILITY REPORT\n")
    file_handle.write("=" * 70 + "\n\n")
    file_handle.write(f"Scanner Type: {scanner_type}\n")
    file_handle.write(f"ATS COMPATIBILITY SCORE: {score}/100\n")

    if score >= 80:
        file_handle.write("Status: ✓ EXCELLENT - Resume is highly ATS-compatible\n\n")
    elif score >= 60:
        file_handle.write("Status: ⚠ GOOD - Resume should parse correctly with minor issues\n\n")
    elif score >= 40:
        file_handle.write("Status: ⚠ FAIR - Some improvements recommended\n\n")
    else:
        file_handle.write("Status: ✗ NEEDS IMPROVEMENT - Significant ATS compatibility issues\n\n")


def _write_report_skills(file_handle, skills: Dict):
    '''
    Write skills section to report
    '''
    explicit_skills = skills.get('explicit_skills', [])
    extracted_skills = skills.get('extracted_skills', [])
    skill_phrases = skills.get('skill_phrases', [])

    # Show explicit skills first - these are the most important
    if explicit_skills:
        file_handle.write(f"EXPLICIT SKILLS (from Skills section): {len(explicit_skills)} skills\n")
        # Group by category if possible
        file_handle.write("  Technical Skills:\n")
        for skill in explicit_skills:
            file_handle.write(f"    • {skill}\n")
        file_handle.write("\n")

    # Then show skills detected by NLP
    file_handle.write(f"NLP-DETECTED SKILLS: {len(extracted_skills)} skills identified\n")
    if extracted_skills:
        for skill in extracted_skills:
            file_handle.write(f"  - {skill.get('skill', '')}\n")
    else:
        file_handle.write("  (No skills detected via skillNer)\n")

    if skill_phrases:
        file_handle.write(f"\nADDITIONAL SKILL PHRASES: {len(skill_phrases)}\n")
        for phrase in skill_phrases[:30]:  # Limit phrases to 30
            file_handle.write(f"  - {phrase}\n")
        if len(skill_phrases) > 30:
            file_handle.write(f"  ... and {len(skill_phrases) - 30} more\n")
    file_handle.write("\n")


def _write_report_contact(file_handle, contact: Dict):
    '''
    Write contact information section to report
    '''
    file_handle.write("CONTACT INFORMATION DETECTED:\n")
    file_handle.write(f"  - Email: {', '.join(contact.get('emails', [])) or 'Not found'}\n")
    file_handle.write(f"  - Phone: {', '.join(contact.get('phones', [])) or 'Not found'}\n")
    file_handle.write(f"  - LinkedIn: {', '.join(contact.get('linkedin', [])) or 'Not found'}\n")
    file_handle.write(f"  - GitHub: {', '.join(contact.get('github', [])) or 'Not found'}\n\n")


def generate_report(analysis: Dict, output_file: str = "ats_report.txt"):
    '''
    Generate a human-readable ATS analysis report
    '''
    logging.info("Generating ATS report: %s", output_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        scanner_type = analysis.get('scanner_type', 'Unknown')
        _write_report_header(f, analysis.get('ats_score', 0), scanner_type)

        # Basic stats
        f.write("DOCUMENT STATISTICS:\n")
        f.write(f"  - Text Length: {analysis.get('text_length', 0)} characters\n")
        f.write(f"  - Word Count: {analysis.get('word_count', 0)} words\n\n")

        # Contact information
        _write_report_contact(f, analysis.get('contact', {}))

        # Skills
        _write_report_skills(f, analysis.get('skills', {}))

        # Experience
        experience = analysis.get('experience', [])
        f.write(f"JOB TITLES DETECTED: {len(experience)}\n")
        for title in experience[:10]:  # Show first 10
            f.write(f"  - {title}\n")
        if len(experience) > 10:
            f.write(f"  ... and {len(experience) - 10} more\n")
        f.write("\n")

        # Education
        education = analysis.get('education', {})
        universities = education.get('universities', [])
        dates = education.get('dates', [])

        f.write("\nEDUCATION INFORMATION:\n")
        f.write("  Universities/Institutions Detected: ")
        if universities:
            f.write(f"{len(universities)}\n")
            for uni in universities:
                f.write(f"    - {uni}\n")
        else:
            f.write("None\n")

        f.write("  Graduation Dates Detected: ")
        if dates:
            f.write(f"{len(dates)}\n")
            for date in dates:
                f.write(f"    - {date}\n")
        else:
            f.write("None\n")

        f.write("  Degree Names: NOT DETECTED\n")
        f.write("    Note: This NLP-based scanner cannot reliably extract degree names.\n")
        f.write("    spaCy does not have dedicated entity types for educational degrees.\n")
        f.write("    Commercial ATS systems use specialized education parsers.\n")
        f.write("\n")

        # Formatting issues
        formatting = analysis.get('formatting', {})
        if formatting.get('issues'):
            f.write("FORMATTING ISSUES:\n")
            for issue in formatting['issues']:
                f.write(f"  ✗ {issue}\n")
            f.write("\n")

        if formatting.get('warnings'):
            f.write("FORMATTING WARNINGS:\n")
            for warning in formatting['warnings']:
                f.write(f"  ⚠ {warning}\n")
            f.write("\n")

        # Recommendations
        if analysis.get('recommendations'):
            f.write("RECOMMENDATIONS FOR IMPROVEMENT:\n")
            for i, rec in enumerate(analysis['recommendations'], 1):
                f.write(f"  {i}. {rec}\n")
            f.write("\n")

        f.write("=" * 70 + "\n")
        f.write("Report generated by ATS Scanner\n")
        f.write("=" * 70 + "\n")

    logging.info("ATS report saved to %s", output_file)


def main():
    '''
    Main function for standalone usage
    '''
    if len(sys.argv) < 2:
        print("Usage: python ats_scanner.py <pdf_file>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    analysis = scan(pdf_file)
    generate_report(analysis)

    score = analysis.get('ats_score', 0)
    print(f"\nATS Compatibility Score: {score}/100")
    print("Full report saved to: ats_report.txt")


if __name__ == '__main__':
    main()


# =============================================================================
# FUTURE ATS IMPLEMENTATIONS
# =============================================================================
#
# To add additional ATS scanners for comparative analysis, implement new
# scanner functions following this pattern:
#
# def scan_rule_based(pdf_path: str) -> Dict:
#     '''
#     Rule-based ATS scanner using only regex patterns (no NLP)
#     Simulates basic keyword-matching ATS systems
#     '''
#     text = extract_text_from_pdf(pdf_path)
#     # Implement rule-based extraction logic
#     return {
#         'scanner_type': 'Rule-Based (Regex Only)',
#         'ats_score': score,
#         'contact': {...},
#         'skills': {...},
#         'experience': [...],
#         'education': [...],
#         'recommendations': [...]
#     }
#
# def scan_ml_based(pdf_path: str) -> Dict:
#     '''
#     ML-based ATS scanner using trained models
#     Could use pre-trained resume parsing models or custom trained models
#     '''
#     # Implement ML-based extraction
#     pass
#
# def scan_commercial_ats_simulator(pdf_path: str, ats_type: str = 'taleo') -> Dict:
#     '''
#     Simulate specific commercial ATS systems
#     ats_type options: 'taleo', 'workday', 'greenhouse', 'lever', etc.
#     '''
#     # Implement ATS-specific parsing logic
#     pass
#
# Then update main() or create a comparative_scan() function to run multiple
# scanners and generate comparison reports showing differences in parsing.
#
# =============================================================================

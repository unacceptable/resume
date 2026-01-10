#!/usr/bin/env python3
'''
ATS Scanner - Analyzes resume PDFs for ATS compatibility
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


def extract_skills(text: str) -> Dict:
    '''
    Extract technical skills and competencies
    '''
    nlp, skill_extractor = _init_models()
    skills = []
    skill_keywords = []

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


def extract_education(text: str) -> List[str]:
    '''
    Extract education information
    '''
    education = []

    # Degree patterns
    degree_patterns = [
        r'(?:Bachelor|Master|Ph\.?D\.?|Doctor|Associate)(?:\'s)?\s+'
        r'(?:of\s+)?(?:Science|Arts|Engineering|Business|Computer Science)',
        r'(?:B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?|MBA|Ph\.?D\.?)'
        r'(?:\s+in\s+[\w\s]+)?'
    ]

    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        education.extend(matches)

    return list(set(education))


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
    if len(skills.get('extracted_skills', [])) < 5:
        score -= 10
        recommendations.append("Add more specific technical skills")

    education = analysis.get('education', [])
    if not education:
        score -= 5
        recommendations.append("Ensure education section is clearly formatted")

    experience = analysis.get('experience', [])
    if not experience:
        score -= 5
        recommendations.append("Ensure job titles are clearly formatted")

    # Ensure score is within bounds
    score = max(0, min(100, score))

    return score, recommendations


def scan(pdf_path: str) -> Dict:
    '''
    Perform comprehensive ATS scan of resume

    Returns:
        Dictionary containing analysis results and ATS score
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


def _write_report_header(file_handle, score: int):
    '''
    Write report header with score
    '''
    file_handle.write("=" * 70 + "\n")
    file_handle.write("ATS COMPATIBILITY REPORT\n")
    file_handle.write("=" * 70 + "\n\n")
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
    extracted_skills = skills.get('extracted_skills', [])
    skill_phrases = skills.get('skill_phrases', [])

    file_handle.write(f"SKILLS EXTRACTED: {len(extracted_skills)} skills identified\n")
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
        _write_report_header(f, analysis.get('ats_score', 0))

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
        education = analysis.get('education', [])
        f.write(f"EDUCATION DETECTED: {len(education)}\n")
        for edu in education:
            f.write(f"  - {edu}\n")
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

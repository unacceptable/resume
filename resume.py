#!/usr/bin/env python3
'''
Render my resume
'''
import logging
import os
import json
import sys
from typing import Optional, Dict

import markdown
import pdfkit
import ats_scanner

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    '''
    Main Function
    '''
    # Check for command line arguments
    run_ats_only = '--ats-only' in sys.argv
    skip_ats = '--skip-ats' in sys.argv

    files = {
        'Resume.md': None,
        'CoverLetter.md': 'CoverLetter.json'
    }

    # If ATS-only mode, just scan existing PDFs
    if run_ats_only:
        logging.info("Running ATS scan only (skipping PDF generation)")
        for file in files:
            pdf_filename = file.replace('.md', '.pdf')
            if os.path.exists(pdf_filename):
                run_ats_scan(pdf_filename)
            else:
                logging.warning("PDF not found: %s", pdf_filename)
        return

    for file, template_file in files.items():
        logging.debug('Processing file: %s with %s', file, template_file)

        template_map = None

        if template_file:
            with open(template_file, 'r', encoding='utf-8') as f:
                logging.info('Loading template from %s', template_file)
                template_map = json.load(f)

        md   = get_contents(filename=file, template=template_map)
        body = markdown.markdown(md, extensions=['tables'])
        html = render_html(body=body)

        pdf_filename = file.replace('.md', '.pdf')
        create_pdf(contents=html, filename=pdf_filename)

        html_filename = file.replace('.md', '.html')

        with open(html_filename, mode='w', encoding='utf-8') as website:
            logging.info('Creating file %s (for website).', website.name)
            website.write(html)

        website.close()

        # Run ATS scan on the generated resume PDF
        if not skip_ats and file == 'Resume.md':
            run_ats_scan(pdf_filename)


def get_contents(filename: str, template: Optional[Dict[str, str]]) -> str:
    '''
    Get the contents of a file
    '''
    logging.info('Getting contents for %s', filename)

    with open(filename, mode='r', encoding='utf-8') as f:
        contents = f.read()

    if template:
        logging.info('Applying template to %s', filename)
        contents = contents.format(**template)

    logging.debug('Contents (for %s): %s', filename, contents)

    return contents


def render_html(body: str, head: str = '', css_filename: str = 'style.css') -> str:
    '''
    Renders HTML
    '''
    logging.info('Rendering HTML')
    css_html = f'<link rel="stylesheet" href="{os.getcwd()}/{css_filename}">'

    head += css_html

    html = f'''
    <!DOCTYPE html>
    <html>
        <head>{head}</head>
        <body>{body}</body>
    </html>
    '''

    logging.debug(html)

    return html


def run_ats_scan(pdf_filename: str) -> None:
    '''
    Run ATS compatibility scan on a PDF file
    '''
    logging.info("Running ATS scan on %s", pdf_filename)

    try:
        analysis = ats_scanner.scan(pdf_filename)

        # Generate report
        report_filename = pdf_filename.replace('.pdf', '_ats_report.txt')
        ats_scanner.generate_report(analysis, report_filename)

        # Print summary
        score = analysis.get('ats_score', 0)
        logging.info("ATS Compatibility Score: %s/100", score)

        if score >= 80:
            logging.info("✓ Resume is highly ATS-compatible")
        elif score >= 60:
            logging.info("⚠ Resume should parse correctly with minor improvements needed")
        else:
            logging.warning("⚠ Resume has ATS compatibility issues - see report for details")

        recommendations = analysis.get('recommendations', [])
        if recommendations:
            logging.info("Found %s recommendations - see %s", len(recommendations), report_filename)

    except Exception as e: # pylint: disable=broad-except
        logging.error("Error running ATS scan: %s", e)


def create_pdf(contents: str, filename: str) -> None:
    '''
    Creates a PDF from html contents
    '''
    options = {'enable-local-file-access': None}

    logging.info('Creating PDF: %s', filename)

    pdfkit.from_string(contents, filename, options=options)


if __name__ == '__main__':
    main()

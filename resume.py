#!/usr/bin/env python3
'''
    Render my resume
'''
import logging
import os
import json

import markdown
import pdfkit

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    '''
    Main Function
    '''
    files = {
        'Resume.md': None,
        'CoverLetter.md': 'CoverLetter.json'
    }

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

        create_pdf(contents=html, filename=file.replace('.md', '.pdf'))

        html_filename = file.replace('.md', '.html')

        with open(html_filename, mode='w', encoding='utf-8') as website:
            logging.info('Creating file %s (for website).', website.name)
            website.write(html)

        website.close()


def get_contents(filename: str, template: map) -> str:
    '''
    Get the contents of a file
    '''
    logging.info('Getting contents for %s', filename)
    with open(filename, mode='r', encoding='utf-8') as f:
        contents = f.read()
    f.close()

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


def create_pdf(contents: str, filename: str) -> None:
    '''
    Creates a PDF from html contents
    '''
    options = {'enable-local-file-access': None}

    logging.info('Creating PDF: %s', filename)

    pdfkit.from_string(contents, filename, options=options)


if __name__ == '__main__':
    main()

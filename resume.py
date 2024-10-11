#!/usr/bin/env python3
# pylint: disable=invalid-name

'''
    Render my resume
'''
import logging
import os
import markdown
import pdfkit

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    '''
        Does all the things
    '''
    md   = get_contents('Resume.md')
    body = markdown.markdown(md, extensions=['tables'])
    html = render_html(body=body)

    create_pdf(contents=html)

    with open('resume.html', mode='w', encoding='utf-8') as website:
        logging.info('Creating file %s (for website).', website.name)
        website.write(html)

    website.close()


def get_contents(filename):
    '''
        return file contents
    '''
    logging.info('Getting contents for %s', filename)
    with open(filename, mode='r', encoding='utf-8') as f:
        contents = f.read()
    f.close()

    logging.debug('Contents (for %s): %s', filename, contents)

    return contents


def render_html(body, head='', css_filename='style.css'):
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


def create_pdf(contents, filename='Resume.pdf'):
    '''
        Creates a PDF
    '''
    options = {'enable-local-file-access': None}

    logging.info('Creating PDF: %s', filename)

    pdfkit.from_string(contents, filename, options=options)


if __name__ == '__main__':
    main()

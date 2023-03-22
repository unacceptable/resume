#!/usr/bin/env python3
# pylint: disable=invalid-name

'''
    Render my resume
'''
import os
import markdown
import pdfkit

def main():
    '''
        Does all the things
    '''
    md   = get_contents('Resume.md')
    body = markdown.markdown(md, extensions=['tables'])
    html = render_html(body=body)

    create_pdf(contents=html)

    with open('resume.html', mode='w') as website:
        website.write(html)

    website.close()


def get_contents(filename):
    '''
        return file contents
    '''
    with open(filename) as f:
        contents = f.read()
    f.close()

    return contents


def render_html(body, head='', css_filename='style.css'):
    '''
        Renders HTML
    '''
    css_html = '''
    <link rel="stylesheet" href="{path}/{name}">
    '''.format(
        path=os.getcwd(),
        name=css_filename
    )

    head += css_html

    html = '''
    <!DOCTYPE html>
    <html>
        <head>{head}</head>
        <body>{body}</body>
    </html>
    '''.format(
        head=head,
        body=body
    )

    print(html)

    return html


def create_pdf(filename='Resume.pdf', contents=''):
    '''
        Creates a PDF
    '''
    options = {'enable-local-file-access': None}
    pdfkit.from_string(contents, filename, options=options)


if __name__ == '__main__':
    main()

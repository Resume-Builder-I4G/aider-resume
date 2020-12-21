from flask import current_app as app
from PIL import Image
import pdfkit
import os, secrets

def save_pic(picture) -> str:
    if picture.mimetype.split('/')[0] != 'image':
        return {
            'error':  'Invalid data',
            'message': 'Please upload an image'
        }
    filename = secrets.token_hex(8) +os.path.splitext(picture.filename)[1]
    while filename in os.listdir(os.path.join(app.root_path, 'static', 'avatars')):
        filename = secrets.token_hex(8) +os.path.splitext(picture.filename)[1]
    file_path = os.path.join(app.root_path, 'static', 'avatars', filename)
    picture = Image.open(picture)
    picture.thumbnail((150, 150))
    picture.save(file_path)
    return filename

def html_to_pdf(html_string, *css):
    options =options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        '--load-error-handling': 'ignore',
        '--load-media-error-handling': 'ignore'
    } 
    config=pdfkit.configuration(wkhtmltopdf = app.config['PDF_TO_HTML'])
    pdf=pdfkit.from_string(html_string, False,
                        configuration=config, css=list(css),
                        options=options)
    return pdf
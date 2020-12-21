from app import mail
from flask import current_app as app, render_template
from flask_mail import Message
from threading import Thread

def send_async_email(app:app, msg:Message):
    with app.app_context():
        mail.send(msg)

def send_mail(recipients, subject, template, attachment=None, **kwargs):
    msg = Message(subject=subject, 
                recipients=recipients,
                sender=app.config['MAIL_USERNAME'])
    msg.body = render_template(template + '.txt', **kwargs)    
    msg.html = render_template(template + '.html', **kwargs)
    if attachment:
        msg.attachments = [attachment]
    mail.send(msg)
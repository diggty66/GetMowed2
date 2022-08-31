from flask import current_app
from flask_mail import Message
from GetMowed2 import app, mail


def send_email(to, subject, template):
    app=current_app
    with app.app_context():
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)

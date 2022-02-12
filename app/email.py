from threading import Thread

from flask import current_app
from flask_mail import Message

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body, sender):
    msg = Message(subject, recipients, text_body, html_body, sender)
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()

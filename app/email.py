from threading import Thread

from flask import render_template
from flask_mail import Message

from app import app, mail


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        subject='[Microblog] Reset Your Password',
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt', user=user, token=token
        ),
        html_body=render_template(
            'email/reset_password.html', user=user, token=token
        ),
        sender=app.config['ADMINS'][0]
    )


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body, sender):
    msg = Message(subject, recipients, text_body, html_body, sender)
    Thread(target=send_async_email, args=(app, msg)).start()

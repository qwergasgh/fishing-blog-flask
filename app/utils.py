from flask_mail import Message
from app import mail, app
from threading import Thread
from flask import render_template


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_email_start, args=(app, msg)).start()


def send_email_start(app, msg):
    with app.app_context():
        mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Reset Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reser_password_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password_email.html',
                                         user=user, token=token))


def get_avatar(avatar):
    if avatar is None:
        avatar = 'avatars/user_avatar.png'
    else:
        avatar = avatar.split('static')[1].replace('/', '', 1)
    return avatar

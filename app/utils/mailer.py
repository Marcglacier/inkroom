# utils/mailer.py
from flask_mail import Message
from app.extensions import mail

def send_email(to: str, subject: str, body: str):
    msg = Message(subject=subject, recipients=[to], body=body)
    mail.send(msg)

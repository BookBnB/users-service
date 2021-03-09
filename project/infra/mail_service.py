from flask import current_app
from flask_mail import Mail, Message


class MailService:
    def send_mail(self, subject, recipient, sender, content):
        mail = Mail(current_app)
        msg = Message(subject=subject,
                    sender=sender,
                    recipients=[recipient],
                    body=content)
        mail.send(msg)

from os import getenv

import smtplib
from email.message import EmailMessage
import ssl

class NotificationService():

    def __init__(self) -> None:
        self.email_sender = getenv('MAIL_SENDER')

    def new_lead_notification(self, email):
        self.notify(f'New application received from {email}', email)

    def notify(self, content, email):
        subject = "New Lead Application"
        try:
            em = EmailMessage()
            em['From'] = self.email_sender
            em['To'] = "raphalinns@gmail.com"
            em['Subject'] = subject
            em.set_content(content)
        
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.email_sender, getenv('MAIL_PASS_CODE'))
                server.send_message(em)
        except Exception as error:
            print('An exception occurred: {}'.format(error))

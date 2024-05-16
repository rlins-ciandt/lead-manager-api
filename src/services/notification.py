from os import getenv

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

class NotificationService():

    def __init__(self):
        self.sender_email = "fake@gmail.com"


    def new_lead_notification(self, email):
        self.notify(f'New application received from {email}')

    def notify(self, content):
        mailchimp = MailchimpTransactional.Client(getenv('MAILCHIMP_API_KEY'))
        try:
            message = {
                "from_email": "app@app.com",
                "subject": "New Lead Notification",
                "text": content,
                "to": [
                {
                    "email": self.sender_email,
                    "type": "to"
                }
                ]
            }
            mailchimp.messages.send({"message": message})
        except ApiClientError as error:
            print('An exception occurred: {}'.format(error.text))

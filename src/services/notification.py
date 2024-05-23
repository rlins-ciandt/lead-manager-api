from os import getenv


import yagmail


class NotificationService():

    def __init__(self) -> None:
        self.email_sender = getenv('MAIL_SENDER')
        self.yag = yagmail.SMTP(self.email_sender, getenv('MAIL_PASS_CODE'))

    def new_lead_notification(self, email):
        self.notify("New Lead Application", f'New application received from {email}')

    def notify(self, subject, content):
        try:
            self.yag.send("raphalinns@gmail.com", subject , content)
        except Exception as error:
            print('An exception occurred: {}'.format(error))

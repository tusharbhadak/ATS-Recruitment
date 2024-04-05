from django.core.mail import EmailMessage
from rest_framework.views import exception_handler

import threading

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        error_messages = {
            400: "Bad request",
            401: "Unauthorized request",
            403: "Forbidden",
            404: "Not found",
            500: "Internal server error"
        }

        if response.status_code in error_messages:
            response.data = {
                'status': 0,
                'errors': [error_messages[response.status_code]],
                'exception': str(exc)
            }
        else:
            data = response.data
            response.data = {}
            errors = []
            for field, value in data.items():
                errors.append("{} : {}".format(field, " ".join(value)))

            response.data['errors'] = errors
            response.data['status'] = False
            response.data['exception'] = str(exc)

    return response




class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()

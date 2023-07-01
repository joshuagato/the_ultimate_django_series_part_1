from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from django.http import HttpResponse
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers

def calculate():
    x = 1
    y = 2
    return x

def say_hello(request):
    # return HttpResponse('Hello World')
    # x = calculate()
    try:
        notify_customers.delay('Hello World')
        # message = BaseEmailMessage(
        #     template_name='emails/hello.html',
        #     context={'name': 'Joshua'}
        # )
        # message.send(['jonas@joshgato.com'])

        # send_mail('subject', 'message', 'info@joshgato.com', ['bob@joshgato.com'])

        # mail_admins('subject', 'message', html_message='html message')

        # message = EmailMessage('subject', 'message', 'from@joshgato.com', ['john@joshgato.com'])
        # message.attach_file('playground/static/images/dog.jpg')
        # message.send()
    except BadHeaderError:
        pass
    return render(request, 'index.html', {'name': 'Joshua'})
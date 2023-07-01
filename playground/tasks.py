from time import sleep
from celery import shared_task
# from storefront.celery import celery


# @celery.task #With this approach the playground app will be dependent on the storefront app
@shared_task
def notify_customers(message):
    print('Sending 10k emails...')
    print(message)

    sleep(10)
    print('Emails were successfully sent!')

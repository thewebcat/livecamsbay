from livecamsbay import celery
from main.func import build_absolute_uri
from email_sender.models import EmailSender
#from custom_auth.func import get_companies, get_masters


@celery.app.task(name='sent_emails')
def sent_emails(emails, data, template):
    new_email = EmailSender()
    new_email.create_message_from_template(template, data).send_to(emails)


# @celery.app.task
# def sent_emails_to_performers_by_publish_order(order):
#     users = get_companies() | get_masters()
#     private_url = build_absolute_uri(order.private_url)
#     public_url = build_absolute_uri(order.public_url)
#     new_email = EmailSender()
#     order_title = order.title
#
#     for user in users.values('email', 'profile__name'):
#         context = {
#             'name': user['profile__name'],
#             'private_url': private_url,
#             'public_url': public_url,
#             'order_title': order_title
#         }
#         new_email.create_message_from_template('mail_to_performers_by_publish_order', context)
#         new_email.send_to(user['email'])

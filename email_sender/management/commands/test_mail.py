# -*- coding: UTF-8 -*-
import os
import sys

from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from common.tokens import user_is_active_token_generator
from custom_auth.models import User

from email_sender.models import EmailSender
from orders.models import Order
from tickets.emails import get_tickets_url

reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--to', type=str)
        parser.add_argument('--mail', type=str)

    @transaction.atomic()
    def handle(self, *args, **options):
        to = options['to']
        mail = options['mail']

        if mail == 'all':
            emails_templates_path = os.path.join(settings.BASE_DIR, 'email_sender/templates/emails')
            # print os.walk(emails_templates_path)
            for path, dirs, files in os.walk(emails_templates_path):
                for fi in files:
                    self.send(to, fi.split('.')[0])
        else:
            self.send(to, mail)

    def send(self, email, template_name):
        print template_name, email
        email_sender = EmailSender()
        email_sender.create_message_from_template(
            template_name=template_name,
            data=self.get_test_data(email=email))
        email_sender.send_to(email_addresses=email)

    def get_test_data(self, email):
        user = User.objects.get(email=email)
        order = Order.objects.first()
        return {
            'site_url': 'http://127.0.0.1:8000/',
            'recover_pass_key': 'jkhfqid6serui23r68',
            'input_password_key_url': 'http://example.com/forget_password/',
            'password_key_url': 'http://example.com/forget_password/?key=jkhfqid6serui23r68',
            'activate_url': 'http://example.com/activate/?key=jkhfqid6serui23r68',
            'domain': '127.0.0.1:8000',
            'protocol': 'http',
            'relative_url': reverse('authorization:activate',
                                    kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token': user_is_active_token_generator.make_token(user)}),
            'support': reverse('feedback:feedback'),
            'site_name': 'Amigostone',

            'content_name': 'content_name',
            'content_type': 'content_type',
            'content_link': 'http://example.com/content_link',

            'private_url': order.absolute_private_url,
            'public_url': order.absolute_public_url,

            'ticket_message': 'ticket_message',
            'tickets_url': get_tickets_url(),
            'recall_link': 'recall_link',

            'order_name': order.title,
            'order_link': order.absolute_private_url,
            'order_title': 'order_title',

            'name': user.profile.name,

            'email': email,
            'password': 'password',
        }

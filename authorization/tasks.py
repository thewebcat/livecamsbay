from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from livecamsbay import celery
from livecamsbay import settings
from main.func import build_absolute_uri
from main.tokens import user_is_active_token_generator
from email_sender.models import EmailSender


@celery.app.task(name='sent_email')
def sent_email(user):
    token_generator = user_is_active_token_generator

    activate_relative_url = reverse(
        'authorization:activate',
        kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user)}
    )

    context = {
        'name': user.profile.name,
        'activate_url': build_absolute_uri(activate_relative_url),
    }

    new_email = EmailSender()
    emails = [
        user.email,
        settings.ADMIN_EMAILS['editor'],
    ]
    new_email.create_message_from_template('affirmative_registration', context).send_to(emails)

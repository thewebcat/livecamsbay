from django.core.management import BaseCommand
from email_sender.email_actions import EMAIL_ACTIONS
from email_sender.models import EmailSetting


class Command(BaseCommand):
    def handle(self, *args, **options):
        print EMAIL_ACTIONS
        for name, desc in EMAIL_ACTIONS.items():
            defaults = {'description': desc, 'group': 1}
            EmailSetting.objects.update_or_create(action=name, defaults=defaults)

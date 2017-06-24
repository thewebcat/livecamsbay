# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

from accounts.models import Profile
from email_sender.models import EmailSetting


class Command(BaseCommand):
    def handle(self, *args, **options):
        settings = EmailSetting.objects.all()
        profiles = Profile.objects.all()
        for s in settings:
            s.profiles.add(*profiles)

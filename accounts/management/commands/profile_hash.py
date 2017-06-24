# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

from accounts.models import Profile, ProfileHash


class Command(BaseCommand):
    def handle(self, *args, **options):

        profiles = Profile.objects.all()
        for profile in profiles:
            if hasattr(profile, 'profilehash'):
                print profile.profilehash
            else:
                ProfileHash(profile=profile).save()

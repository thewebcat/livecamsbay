# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

from accounts.models import Profile, ProfileGrades


class Command(BaseCommand):
    def handle(self, *args, **options):

        profiles = Profile.objects.exclude(role__in=Profile.ROLE_USER)
        for profile in profiles:
            if not hasattr(profile, 'profilegrades'):
                profilegrades = ProfileGrades(profile=profile)
                profilegrades.save()
                profilegrades.get_gems()

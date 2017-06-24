# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

from accounts.tasks import recalculate_position


class Command(BaseCommand):
    def handle(self, *args, **options):
        recalculate_position()

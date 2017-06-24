# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

from custom_auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        if len(args) == 0:
            print "use command: \"./manage.py remove_user email\""
            return

        email = args[0]
        user = User.objects.get(email=email)
        for order in user.order_set.all():
            order.orderimage_set.all().delete()

        user.order_set.all().delete()

        user.delete()

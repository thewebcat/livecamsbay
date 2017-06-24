# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class Email(models.Model):
    """
    Все емаил которые добровольно оформили подписку
    """
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.email

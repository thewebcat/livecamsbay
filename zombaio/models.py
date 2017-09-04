# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Subscription(models.Model):
    user = models.OneToOneField('accounts.Profile')
    

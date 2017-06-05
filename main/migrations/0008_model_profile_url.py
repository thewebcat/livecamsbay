# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20170526_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='profile_url',
            field=models.CharField(max_length=200, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u043f\u0440\u043e\u0444\u0438\u043b\u044c', blank=True),
        ),
    ]

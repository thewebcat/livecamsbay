# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_model_profile_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='chat_url',
            field=models.CharField(max_length=200, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0447\u0430\u0442', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-13 15:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('call_orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='callorder',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-16 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170904_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='camservice',
            name='affiliate_url',
            field=models.CharField(default='o', max_length=255, verbose_name='\u041f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u0430\u044f \u0441\u0441\u044b\u043b\u043a\u0430'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='camservice',
            name='description',
            field=models.TextField(default='o'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='camservice',
            name='prefix',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='\u041f\u0440\u0435\u0444\u0438\u043a\u0441'),
        ),
    ]
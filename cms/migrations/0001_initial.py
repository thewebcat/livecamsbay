# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-04 00:08
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, '\u043d\u0435 \u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d'), (1, '\u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d'), (2, '\u0443\u0434\u0430\u043b\u0435\u043d'), (3, '\u043f\u0435\u0440\u0435\u043d\u0435\u0441\u0435\u043d \u0432 \u0447\u0435\u0440\u043d\u043e\u0432\u0438\u043a')], default=3, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441')),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', ckeditor.fields.RichTextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

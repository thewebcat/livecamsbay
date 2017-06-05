# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_model_chat_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='CamSnapshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('snapshot_url', models.CharField(max_length=255, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430', blank=True)),
                ('model', models.ForeignKey(verbose_name='\u041c\u043e\u0434\u0435\u043b\u044c', blank=True, to='main.Model', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-13 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='User name')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone number')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('status', models.CharField(choices=[(b'CL', b'Call later'), (b'AW', b'Not responding')], max_length=10, verbose_name='Status')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('processing_date', models.DateTimeField(blank=True, null=True, verbose_name='Processing date')),
                ('finishing_date', models.DateTimeField(blank=True, null=True, verbose_name='Finishing date')),
            ],
        ),
    ]

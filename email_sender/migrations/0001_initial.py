# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-13 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[(b'co', '\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438'), (b'pe', '\u0444\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='EmailSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.PositiveSmallIntegerField(choices=[(1, b'\xd0\x97\xd0\xb0\xd0\xba\xd0\xb0\xd0\xb7'), (2, b'\xd0\xa2\xd0\xb8\xd0\xba\xd0\xb5\xd1\x82\xd1\x8b'), (3, b'\xd0\x9a\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82'), (4, b'\xd0\xa0\xd0\xb5\xd0\xb9\xd1\x82\xd0\xb8\xd0\xbd\xd0\xb3\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x8f \xd1\x81\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xb0'), (5, b'\xd0\xa0\xd0\xb5\xd0\xba\xd0\xbb\xd0\xb0\xd0\xbc\xd0\xbd\xd0\xb0\xd1\x8f \xd1\x81\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xb0'), (6, b'\xd0\x9e\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xb0\xd0\xba\xd0\xba\xd0\xb0\xd1\x83\xd0\xbd\xd1\x82\xd0\xb0'), (7, b'\xd0\xa1\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f \xd0\xb2 \xd0\xba\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb4\xd0\xb0\xd1\x80\xd0\xb5'), (8, b'\xd0\x94\xd0\xbe\xd0\xba\xd1\x83\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xbe\xd0\xbe\xd0\xb1\xd0\xbe\xd1\x80\xd0\xbe\xd1\x82')])),
                ('action', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('changeable', models.BooleanField(default=True)),
                ('profiles', models.ManyToManyField(related_name='email_settings', to='accounts.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='emailgroup',
            name='settings',
            field=models.ManyToManyField(related_name='email_groups', to='email_sender.EmailSetting'),
        ),
    ]

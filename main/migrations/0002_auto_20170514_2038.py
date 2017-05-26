# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-14 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CamService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('url', models.CharField(max_length=100, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('api_url', models.CharField(max_length=255, verbose_name='\u0410\u043f\u0438 url')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='model',
            name='online_time',
            field=models.PositiveIntegerField(default=0, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043e\u043d\u043b\u0430\u0439\u043d'),
        ),
        migrations.AddField(
            model_name='model',
            name='profile_image',
            field=models.CharField(blank=True, max_length=100, verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u043f\u0440\u043e\u0444\u0438\u043b\u044f'),
        ),
        migrations.AddField(
            model_name='model',
            name='cam_service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.CamService', verbose_name='Cam \u0441\u0435\u0440\u0432\u0438\u0441'),
            preserve_default=False,
        ),
    ]

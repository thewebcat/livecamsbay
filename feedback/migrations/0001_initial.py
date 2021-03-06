# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-18 14:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Contact')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone')),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('company', models.CharField(blank=True, max_length=255, null=True, verbose_name='Company')),
                ('question', models.TextField(verbose_name='Question')),
                ('comment', models.TextField(default=None, verbose_name='Comment')),
                ('creation_date', models.DateTimeField(auto_now_add=True, default=None, verbose_name='Creation date')),
                ('finishing_date', models.DateTimeField(blank=True, null=True, verbose_name='Finishing date')),
                # ('moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moderator', to=settings.AUTH_USER_MODEL)),
                ('processing_date', models.DateTimeField(blank=True, null=True, verbose_name='Processing date')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': '\u041e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0432\u044f\u0437\u044c'},
        ),
        # migrations.RemoveField(
        #     model_name='feedback',
        #     name='moderator',
        # ),
        migrations.AlterField(
            model_name='feedback',
            name='comment',
            field=models.TextField(verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='finishing_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u0424\u0418\u041e'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='processing_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='question',
            field=models.TextField(verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441'),
        ),
    ]

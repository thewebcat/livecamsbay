# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_model_display_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='model',
            old_name='avalible',
            new_name='available',
        ),
        migrations.AlterIndexTogether(
            name='model',
            index_together=set([('name', 'available', 'views_count')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name': 'Branch', 'verbose_name_plural': 'Branches'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'City', 'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='storeadmin',
            options={'verbose_name': 'Store Administrator', 'verbose_name_plural': 'Store Administrators'},
        ),
    ]

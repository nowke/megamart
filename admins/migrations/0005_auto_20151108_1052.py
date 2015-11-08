# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0004_auto_20151107_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeadmin',
            name='branch',
            field=models.OneToOneField(to='admins.Branch'),
        ),
    ]

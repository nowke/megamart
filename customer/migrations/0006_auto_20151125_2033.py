# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20151120_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='megamartuser',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]

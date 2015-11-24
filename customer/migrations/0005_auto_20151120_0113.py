# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20151115_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderset',
            name='bill_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

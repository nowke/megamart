# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20151115_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderset',
            name='bill_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_megamartuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderset',
            name='bill_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='orderset',
            name='bill_date',
            field=models.DateTimeField(null=True),
        ),
    ]

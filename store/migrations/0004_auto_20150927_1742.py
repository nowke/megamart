# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20150927_1735'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productset',
            options={'verbose_name': 'Product Set', 'verbose_name_plural': 'Product Sets'},
        ),
    ]

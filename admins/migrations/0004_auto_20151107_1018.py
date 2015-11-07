# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_branch_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.TextField(default=b'', max_length=256),
        ),
    ]

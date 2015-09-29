# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_productset_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productset',
            name='branch',
            field=models.ForeignKey(to='admins.Branch'),
        ),
    ]

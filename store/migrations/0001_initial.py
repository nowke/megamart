# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('expiry_date', models.DateField()),
                ('min_quantity_retain', models.FloatField()),
                ('product', models.ForeignKey(to='product_manager.Product')),
            ],
        ),
    ]
